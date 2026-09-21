import os
import sqlite3
import json
import uuid
import secrets
from datetime import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import (
    Flask, request, jsonify, session, send_from_directory,
    render_template, g
)

# ──────────────────────────────────────────────
# APP CONFIG
# ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')

DB_PATH = os.path.join(BASE_DIR, 'database', 'cerita_nusantara.db')

ALLOWED_IMAGE_EXT = {'jpg', 'jpeg', 'png', 'webp'}
ALLOWED_VIDEO_EXT = {'mp4', 'webm'}
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@ceritanusantara.id')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Admin123!')

# ──────────────────────────────────────────────
# DATABASE
# ──────────────────────────────────────────────
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys=ON")
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA foreign_keys=ON")
    db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS stories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            region TEXT,
            category TEXT,
            content TEXT,
            cover TEXT,
            video TEXT,
            author_id INTEGER,
            user_id INTEGER,
            status TEXT DEFAULT 'pending',
            rejection_reason TEXT,
            is_interactive INTEGER DEFAULT 0,
            characters TEXT,
            moral_value TEXT,
            local_language TEXT,
            reading_duration TEXT,
            views INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (author_id) REFERENCES users(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS story_scenes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            story_id INTEGER NOT NULL,
            scene_number INTEGER NOT NULL,
            title TEXT,
            text TEXT,
            image TEXT,
            next_scene INTEGER,
            is_ending INTEGER DEFAULT 0,
            ending_type TEXT,
            FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS story_choices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scene_id INTEGER NOT NULL,
            choice_text TEXT NOT NULL,
            next_scene INTEGER,
            choice_letter TEXT,
            FOREIGN KEY (scene_id) REFERENCES story_scenes(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            story_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT,
            option_d TEXT,
            correct_answer TEXT NOT NULL,
            explanation TEXT,
            FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            story_id INTEGER NOT NULL,
            current_scene INTEGER DEFAULT 1,
            choices_made TEXT,
            completed INTEGER DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (story_id) REFERENCES stories(id),
            UNIQUE(user_id, story_id)
        );
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            story_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (story_id) REFERENCES stories(id),
            UNIQUE(user_id, story_id)
        );
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            story_id INTEGER NOT NULL,
            score INTEGER,
            correct INTEGER,
            wrong INTEGER,
            total INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (story_id) REFERENCES stories(id)
        );
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            message TEXT,
            is_read INTEGER DEFAULT 0,
            type TEXT DEFAULT 'info',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    ''')
    db.commit()
    cur = db.execute("SELECT id FROM users WHERE username = ?", (ADMIN_USERNAME,))
    if cur.fetchone() is None:
        db.execute(
            "INSERT INTO users (name,username,email,password_hash,role,status) VALUES (?,?,?,?, 'admin','active')",
            ('Administrator', ADMIN_USERNAME, ADMIN_EMAIL, generate_password_hash(ADMIN_PASSWORD))
        )
        db.commit()
    db.close()

# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────
def allowed_file(fn, s): return '.' in fn and fn.rsplit('.',1)[1].lower() in s

def save_upload(f, sub, exts):
    if not f or f.filename == '': return None
    if not allowed_file(f.filename, exts): return None
    ext = f.filename.rsplit('.',1)[1].lower()
    name = f"{uuid.uuid4().hex}.{ext}"
    d = os.path.join(app.config['UPLOAD_FOLDER'], sub)
    os.makedirs(d, exist_ok=True)
    f.save(os.path.join(d, name))
    return f"{sub}/{name}"

def login_required(f):
    @wraps(f)
    def d(*a, **kw):
        if 'user_id' not in session: return jsonify({'error':'Login required'}), 401
        return f(*a, **kw)
    return d

def admin_required(f):
    @wraps(f)
    def d(*a, **kw):
        if 'user_id' not in session: return jsonify({'error':'Login required'}), 401
        if session.get('role') != 'admin': return jsonify({'error':'Access denied'}), 403
        return f(*a, **kw)
    return d

def create_notif(uid, title, msg, ntype='info'):
    db = get_db()
    db.execute("INSERT INTO notifications (user_id,title,message,type) VALUES (?,?,?,?)", (uid,title,msg,ntype))
    db.commit()

# ──────────────────────────────────────────────
# PAGE ROUTE
# ──────────────────────────────────────────────
@app.route('/')
def index(): return render_template('index.html')

@app.route('/uploads/<path:filename>')
def uploaded_file(filename): return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ──────────────────────────────────────────────
# AUTH
# ──────────────────────────────────────────────
@app.route('/api/auth/register', methods=['POST'])
def register():
    d = request.get_json()
    if not d: return jsonify({'error':'Data tidak valid'}), 400
    name = (d.get('name') or '').strip()
    username = (d.get('username') or '').strip()
    email = (d.get('email') or '').strip()
    pw = d.get('password') or ''
    cpw = d.get('confirm_password') or ''
    if not name or not username or not email or not pw:
        return jsonify({'error':'Semua field wajib diisi'}), 400
    if len(pw) < 8: return jsonify({'error':'Password minimal 8 karakter'}), 400
    if pw != cpw: return jsonify({'error':'Password tidak cocok'}), 400
    db = get_db()
    if db.execute("SELECT id FROM users WHERE username=?",(username,)).fetchone():
        return jsonify({'error':'Username sudah digunakan'}), 400
    if db.execute("SELECT id FROM users WHERE email=?",(email,)).fetchone():
        return jsonify({'error':'Email sudah terdaftar'}), 400
    db.execute("INSERT INTO users (name,username,email,password_hash,role,status) VALUES (?,?,?,?, 'user','active')",
               (name, username, email, generate_password_hash(pw)))
    db.commit()
    return jsonify({'message':'Registrasi berhasil'}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    d = request.get_json()
    if not d: return jsonify({'error':'Data tidak valid'}), 400
    lid = (d.get('username') or d.get('email') or '').strip()
    pw = d.get('password') or ''
    if not lid or not pw: return jsonify({'error':'Field wajib diisi'}), 400
    db = get_db()
    u = db.execute("SELECT * FROM users WHERE username=? OR email=?", (lid, lid)).fetchone()
    if not u or not check_password_hash(u['password_hash'], pw):
        return jsonify({'error':'Username/email atau password salah'}), 401
    if u['status'] == 'deactivated':
        return jsonify({'error':'Akun dinonaktifkan'}), 403
    session['user_id'] = u['id']
    session['role'] = u['role']
    session['username'] = u['username']
    return jsonify({'message':'Login berhasil', 'user': {
        'id':u['id'],'name':u['name'],'username':u['username'],
        'email':u['email'],'role':u['role'],'created_at':u['created_at']
    }})

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message':'Logout berhasil'})

@app.route('/api/auth/me')
@login_required
def get_me():
    u = get_db().execute("SELECT * FROM users WHERE id=?",(session['user_id'],)).fetchone()
    if not u: return jsonify({'error':'Tidak ditemukan'}), 404
    return jsonify({'id':u['id'],'name':u['name'],'username':u['username'],
                    'email':u['email'],'role':u['role'],'status':u['status'],'created_at':u['created_at']})

@app.route('/api/auth/profile', methods=['PUT'])
@login_required
def update_profile():
    d = request.get_json()
    db = get_db()
    u = db.execute("SELECT * FROM users WHERE id=?",(session['user_id'],)).fetchone()
    name = (d.get('name') or u['name']).strip()
    email = (d.get('email') or u['email']).strip()
    if email != u['email'] and db.execute("SELECT id FROM users WHERE email=? AND id!=?",(email,u['id'])).fetchone():
        return jsonify({'error':'Email sudah digunakan'}), 400
    db.execute("UPDATE users SET name=?,email=? WHERE id=?", (name,email,u['id']))
    db.commit()
    return jsonify({'message':'Profil diperbarui'})

# ──────────────────────────────────────────────
# STORIES
# ──────────────────────────────────────────────
@app.route('/api/stories')
def get_stories():
    db = get_db()
    status = request.args.get('status','approved')
    region = request.args.get('region')
    category = request.args.get('category')
    search = request.args.get('search')
    sort = request.args.get('sort','newest')
    user_id = request.args.get('user_id')
    q = "SELECT s.*, u.name as author_name FROM stories s LEFT JOIN users u ON s.user_id=u.id WHERE 1=1"
    p = []
    if user_id:
        q += " AND s.user_id=?"; p.append(int(user_id))
    elif status:
        q += " AND s.status=?"; p.append(status)
    if region: q += " AND s.region=?"; p.append(region)
    if category: q += " AND s.category=?"; p.append(category)
    if search:
        q += " AND (s.title LIKE ? OR s.region LIKE ? OR s.category LIKE ? OR s.description LIKE ?)"
        sv = f"%{search}%"; p.extend([sv,sv,sv,sv])
    if sort == 'popular': q += " ORDER BY s.views DESC"
    elif sort == 'oldest': q += " ORDER BY s.created_at ASC"
    else: q += " ORDER BY s.created_at DESC"
    rows = db.execute(q, p).fetchall()
    out = []
    for r in rows:
        it = dict(r)
        it['scene_count'] = db.execute("SELECT COUNT(*) c FROM story_scenes WHERE story_id=?",(r['id'],)).fetchone()['c']
        it['quiz_count'] = db.execute("SELECT COUNT(*) c FROM quizzes WHERE story_id=?",(r['id'],)).fetchone()['c']
        out.append(it)
    return jsonify(out)

@app.route('/api/stories/<int:sid>')
def get_story(sid):
    db = get_db()
    s = db.execute("SELECT s.*, u.name as author_name FROM stories s LEFT JOIN users u ON s.user_id=u.id WHERE s.id=?",(sid,)).fetchone()
    if not s: return jsonify({'error':'Tidak ditemukan'}), 404
    db.execute("UPDATE stories SET views=views+1 WHERE id=?",(sid,)); db.commit()
    r = dict(s)
    r['scenes'] = [dict(x) for x in db.execute("SELECT * FROM story_scenes WHERE story_id=? ORDER BY scene_number",(sid,)).fetchall()]
    for sc in r['scenes']:
        sc['choices'] = [dict(c) for c in db.execute("SELECT * FROM story_choices WHERE scene_id=?",(sc['id'],)).fetchall()]
    r['quizzes'] = [dict(q) for q in db.execute("SELECT * FROM quizzes WHERE story_id=?",(sid,)).fetchall()]
    return jsonify(r)

@app.route('/api/stories', methods=['POST'])
@login_required
def create_story():
    title = request.form.get('title','').strip()
    if not title: return jsonify({'error':'Judul wajib'}), 400
    db = get_db()
    cover = save_upload(request.files.get('cover'), 'stories', ALLOWED_IMAGE_EXT)
    video = save_upload(request.files.get('video'), 'videos', ALLOWED_VIDEO_EXT)
    try: scenes = json.loads(request.form.get('scenes','[]'))
    except: scenes = []
    try: quizzes = json.loads(request.form.get('quizzes','[]'))
    except: quizzes = []
    cur = db.execute(
        "INSERT INTO stories (title,description,region,category,content,cover,video,user_id,author_id,status,is_interactive,characters,moral_value,local_language,reading_duration) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (title, request.form.get('description',''), request.form.get('region',''), request.form.get('category',''),
         request.form.get('content',''), cover, video, session['user_id'], session['user_id'], 'pending',
         int(request.form.get('is_interactive',0)), request.form.get('characters',''),
         request.form.get('moral_value',''), request.form.get('local_language',''), request.form.get('reading_duration','5 menit'))
    )
    sid = cur.lastrowid
    for i, sc in enumerate(scenes):
        sc_id = db.execute("INSERT INTO story_scenes (story_id,scene_number,title,text,image,next_scene,is_ending,ending_type) VALUES (?,?,?,?,?,?,?,?)",
            (sid, i+1, sc.get('title',f'Scene {i+1}'), sc.get('text',''), sc.get('image'), sc.get('next_scene'), sc.get('is_ending',0), sc.get('ending_type'))
        ).lastrowid
        for ch in sc.get('choices',[]):
            db.execute("INSERT INTO story_choices (scene_id,choice_text,next_scene,choice_letter) VALUES (?,?,?,?)",
                (sc_id, ch.get('text',''), ch.get('next_scene'), ch.get('letter','')))
    for q in quizzes:
        db.execute("INSERT INTO quizzes (story_id,question,option_a,option_b,option_c,option_d,correct_answer,explanation) VALUES (?,?,?,?,?,?,?,?)",
            (sid, q.get('question',''), q.get('option_a',''), q.get('option_b',''), q.get('option_c',''), q.get('option_d',''), q.get('correct_answer',''), q.get('explanation','')))
    db.commit()
    un = db.execute("SELECT username FROM users WHERE id=?",(session['user_id'],)).fetchone()['username']
    for a in db.execute("SELECT id FROM users WHERE role='admin'").fetchall():
        create_notif(a['id'], 'Pengajuan Cerita Baru', f'Cerita baru dari {un}: "{title}" menunggu persetujuan.', 'story_submission')
    return jsonify({'message':'Cerita berhasil dikirim','story_id':sid}), 201

@app.route('/api/stories/<int:sid>', methods=['PUT'])
@login_required
def update_story(sid):
    db = get_db()
    s = db.execute("SELECT * FROM stories WHERE id=?",(sid,)).fetchone()
    if not s: return jsonify({'error':'Tidak ditemukan'}), 404
    if s['user_id'] != session['user_id'] and session.get('role') != 'admin':
        return jsonify({'error':'Akses ditolak'}), 403
    if request.content_type and 'multipart' in request.content_type:
        t = request.form.get('title', s['title'])
        desc = request.form.get('description', s['description'])
        reg = request.form.get('region', s['region'])
        cat = request.form.get('category', s['category'])
        cont = request.form.get('content', s['content'])
        chars = request.form.get('characters', s['characters'])
        mv = request.form.get('moral_value', s['moral_value'])
        ll = request.form.get('local_language', s['local_language'])
        rd = request.form.get('reading_duration', s['reading_duration'])
        ii = int(request.form.get('is_interactive', s['is_interactive']))
        cov = s['cover']
        if 'cover' in request.files and request.files['cover'].filename:
            cov = save_upload(request.files['cover'], 'stories', ALLOWED_IMAGE_EXT) or cov
        vid = s['video']
        if 'video' in request.files and request.files['video'].filename:
            vid = save_upload(request.files['video'], 'videos', ALLOWED_VIDEO_EXT) or vid
    else:
        d = request.get_json() or {}
        t=d.get('title',s['title']); desc=d.get('description',s['description'])
        reg=d.get('region',s['region']); cat=d.get('category',s['category'])
        cont=d.get('content',s['content']); chars=d.get('characters',s['characters'])
        mv=d.get('moral_value',s['moral_value']); ll=d.get('local_language',s['local_language'])
        rd=d.get('reading_duration',s['reading_duration']); ii=d.get('is_interactive',s['is_interactive'])
        cov=s['cover']; vid=s['video']
    db.execute("UPDATE stories SET title=?,description=?,region=?,category=?,content=?,cover=?,video=?,is_interactive=?,characters=?,moral_value=?,local_language=?,reading_duration=?,updated_at=CURRENT_TIMESTAMP WHERE id=?",
        (t,desc,reg,cat,cont,cov,vid,ii,chars,mv,ll,rd,sid))
    if s['status']=='rejected':
        db.execute("UPDATE stories SET status='pending',rejection_reason=NULL WHERE id=?",(sid,))
    db.commit()
    return jsonify({'message':'Cerita diperbarui'})

@app.route('/api/stories/<int:sid>', methods=['DELETE'])
@login_required
def delete_story(sid):
    db = get_db()
    s = db.execute("SELECT * FROM stories WHERE id=?",(sid,)).fetchone()
    if not s: return jsonify({'error':'Tidak ditemukan'}), 404
    if s['user_id']!=session['user_id'] and session.get('role')!='admin':
        return jsonify({'error':'Akses ditolak'}), 403
    for t in ['story_choices','story_scenes','quizzes','favorites','progress','quiz_results']:
        col = 'story_id' if t != 'story_choices' else 'scene_id'
        if t == 'story_choices':
            db.execute(f"DELETE FROM {t} WHERE scene_id IN (SELECT id FROM story_scenes WHERE story_id=?)",(sid,))
        else:
            db.execute(f"DELETE FROM {t} WHERE story_id=?",(sid,))
    db.execute("DELETE FROM stories WHERE id=?",(sid,))
    db.commit()
    return jsonify({'message':'Cerita dihapus'})

# ──────────────────────────────────────────────
# MODERATION
# ──────────────────────────────────────────────
@app.route('/api/admin/stories/pending')
@admin_required
def admin_pending():
    rows = get_db().execute("SELECT s.*, u.name as author_name, u.username as author_username FROM stories s LEFT JOIN users u ON s.user_id=u.id WHERE s.status='pending' ORDER BY s.created_at DESC").fetchall()
    return jsonify([dict(r) for r in rows])

@app.route('/api/admin/stories/all')
@admin_required
def admin_all_stories():
    rows = get_db().execute("SELECT s.*, u.name as author_name, u.username as author_username FROM stories s LEFT JOIN users u ON s.user_id=u.id ORDER BY s.created_at DESC").fetchall()
    return jsonify([dict(r) for r in rows])

@app.route('/api/admin/stories/<int:sid>/approve', methods=['POST'])
@admin_required
def approve_story(sid):
    db = get_db()
    s = db.execute("SELECT * FROM stories WHERE id=?",(sid,)).fetchone()
    if not s: return jsonify({'error':'Tidak ditemukan'}), 404
    db.execute("UPDATE stories SET status='approved',updated_at=CURRENT_TIMESTAMP WHERE id=?",(sid,)); db.commit()
    create_notif(s['user_id'],'Cerita Disetujui',f'Cerita "{s["title"]}" telah disetujui dan tersedia untuk publik.','story_approved')
    return jsonify({'message':'Cerita disetujui'})

@app.route('/api/admin/stories/<int:sid>/reject', methods=['POST'])
@admin_required
def reject_story(sid):
    db = get_db()
    s = db.execute("SELECT * FROM stories WHERE id=?",(sid,)).fetchone()
    if not s: return jsonify({'error':'Tidak ditemukan'}), 404
    reason = (request.get_json() or {}).get('reason','Tidak memenuhi standar.')
    db.execute("UPDATE stories SET status='rejected',rejection_reason=?,updated_at=CURRENT_TIMESTAMP WHERE id=?",(reason,sid)); db.commit()
    create_notif(s['user_id'],'Cerita Perlu Diperbaiki',f'Cerita "{s["title"]}" ditolak. Alasan: {reason}','story_rejected')
    return jsonify({'message':'Cerita ditolak'})

# ──────────────────────────────────────────────
# QUIZ
# ──────────────────────────────────────────────
@app.route('/api/stories/<int:sid>/quiz')
def get_quiz(sid):
    return jsonify([dict(q) for q in get_db().execute("SELECT * FROM quizzes WHERE story_id=?",(sid,)).fetchall()])

@app.route('/api/quiz/submit', methods=['POST'])
@login_required
def submit_quiz():
    d = request.get_json()
    if not d: return jsonify({'error':'Data tidak valid'}), 400
    db = get_db()
    qs = db.execute("SELECT * FROM quizzes WHERE story_id=?",(d['story_id'],)).fetchall()
    correct = sum(1 for q in qs if d.get('answers',{}).get(str(q['id']),'').upper() == q['correct_answer'].upper())
    total = len(qs); wrong = total - correct
    score = round((correct/total)*100) if total else 0
    db.execute("INSERT INTO quiz_results (user_id,story_id,score,correct,wrong,total) VALUES (?,?,?,?,?,?)",
               (session['user_id'],d['story_id'],score,correct,wrong,total))
    db.commit()
    return jsonify({'score':score,'correct':correct,'wrong':wrong,'total':total})

@app.route('/api/quiz/results')
@login_required
def quiz_results():
    rows = get_db().execute("SELECT qr.*, s.title as story_title FROM quiz_results qr JOIN stories s ON qr.story_id=s.id WHERE qr.user_id=? ORDER BY qr.created_at DESC",(session['user_id'],)).fetchall()
    return jsonify([dict(r) for r in rows])

# ──────────────────────────────────────────────
# PROGRESS
# ──────────────────────────────────────────────
@app.route('/api/progress')
@login_required
def get_progress():
    rows = get_db().execute("SELECT p.*, s.title as story_title, s.cover FROM progress p JOIN stories s ON p.story_id=s.id WHERE p.user_id=?",(session['user_id'],)).fetchall()
    return jsonify([dict(r) for r in rows])

@app.route('/api/progress', methods=['POST'])
@login_required
def save_progress():
    d = request.get_json()
    db = get_db()
    ex = db.execute("SELECT id FROM progress WHERE user_id=? AND story_id=?",(session['user_id'],d['story_id'])).fetchone()
    cm = json.dumps(d.get('choices_made',[]))
    if ex:
        db.execute("UPDATE progress SET current_scene=?,choices_made=?,completed=?,updated_at=CURRENT_TIMESTAMP WHERE id=?",
                   (d.get('current_scene',1), cm, d.get('completed',0), ex['id']))
    else:
        db.execute("INSERT INTO progress (user_id,story_id,current_scene,choices_made,completed) VALUES (?,?,?,?,?)",
                   (session['user_id'],d['story_id'],d.get('current_scene',1),cm,d.get('completed',0)))
    db.commit()
    return jsonify({'message':'Progress tersimpan'})

# ──────────────────────────────────────────────
# FAVORITES
# ──────────────────────────────────────────────
@app.route('/api/favorites')
@login_required
def get_favorites():
    rows = get_db().execute("SELECT f.*, s.title, s.cover, s.region, s.category, s.description, s.reading_duration, s.views FROM favorites f JOIN stories s ON f.story_id=s.id WHERE f.user_id=? ORDER BY f.created_at DESC",(session['user_id'],)).fetchall()
    return jsonify([dict(r) for r in rows])

@app.route('/api/favorites/<int:sid>', methods=['POST'])
@login_required
def add_fav(sid):
    db = get_db()
    if db.execute("SELECT id FROM favorites WHERE user_id=? AND story_id=?",(session['user_id'],sid)).fetchone():
        return jsonify({'message':'Sudah difavoritkan'})
    db.execute("INSERT INTO favorites (user_id,story_id) VALUES (?,?)",(session['user_id'],sid)); db.commit()
    return jsonify({'message':'Ditambahkan ke favorit'}), 201

@app.route('/api/favorites/<int:sid>', methods=['DELETE'])
@login_required
def remove_fav(sid):
    get_db().execute("DELETE FROM favorites WHERE user_id=? AND story_id=?",(session['user_id'],sid)); get_db().commit()
    return jsonify({'message':'Dihapus dari favorit'})

@app.route('/api/favorites/check/<int:sid>')
@login_required
def check_fav(sid):
    ex = get_db().execute("SELECT id FROM favorites WHERE user_id=? AND story_id=?",(session['user_id'],sid)).fetchone()
    return jsonify({'is_favorite': ex is not None})

# ──────────────────────────────────────────────
# NOTIFICATIONS
# ──────────────────────────────────────────────
@app.route('/api/notifications')
@login_required
def get_notifs():
    db = get_db()
    ns = db.execute("SELECT * FROM notifications WHERE user_id=? ORDER BY created_at DESC LIMIT 50",(session['user_id'],)).fetchall()
    ur = db.execute("SELECT COUNT(*) c FROM notifications WHERE user_id=? AND is_read=0",(session['user_id'],)).fetchone()
    return jsonify({'notifications':[dict(n) for n in ns],'unread_count':ur['c']})

@app.route('/api/notifications/<int:nid>/read', methods=['POST'])
@login_required
def mark_read(nid):
    get_db().execute("UPDATE notifications SET is_read=1 WHERE id=? AND user_id=?",(nid,session['user_id'])); get_db().commit()
    return jsonify({'message':'OK'})

@app.route('/api/notifications/read-all', methods=['POST'])
@login_required
def mark_all_read():
    get_db().execute("UPDATE notifications SET is_read=1 WHERE user_id=?",(session['user_id'],)); get_db().commit()
    return jsonify({'message':'OK'})

# ──────────────────────────────────────────────
# ADMIN
# ──────────────────────────────────────────────
@app.route('/api/admin/stats')
@admin_required
def admin_stats():
    db = get_db()
    return jsonify({
        'total_stories': db.execute("SELECT COUNT(*) c FROM stories").fetchone()['c'],
        'approved': db.execute("SELECT COUNT(*) c FROM stories WHERE status='approved'").fetchone()['c'],
        'pending': db.execute("SELECT COUNT(*) c FROM stories WHERE status='pending'").fetchone()['c'],
        'rejected': db.execute("SELECT COUNT(*) c FROM stories WHERE status='rejected'").fetchone()['c'],
        'total_users': db.execute("SELECT COUNT(*) c FROM users WHERE role='user'").fetchone()['c'],
        'total_videos': db.execute("SELECT COUNT(*) c FROM stories WHERE video IS NOT NULL AND video!=''").fetchone()['c'],
        'total_quizzes': db.execute("SELECT COUNT(*) c FROM quizzes").fetchone()['c'],
    })

@app.route('/api/admin/users')
@admin_required
def admin_users():
    rows = get_db().execute("SELECT id,name,username,email,role,status,created_at FROM users ORDER BY created_at DESC").fetchall()
    out = []
    for u in rows:
        it = dict(u)
        it['story_count'] = get_db().execute("SELECT COUNT(*) c FROM stories WHERE user_id=?",(u['id'],)).fetchone()['c']
        out.append(it)
    return jsonify(out)

@app.route('/api/admin/users/<int:uid>', methods=['PUT'])
@admin_required
def admin_update_user(uid):
    d = request.get_json(); db = get_db()
    u = db.execute("SELECT * FROM users WHERE id=?",(uid,)).fetchone()
    if not u: return jsonify({'error':'Tidak ditemukan'}), 404
    db.execute("UPDATE users SET status=? WHERE id=?",(d.get('status',u['status']),uid)); db.commit()
    return jsonify({'message':'User diperbarui'})

@app.route('/api/admin/quizzes')
@admin_required
def admin_quizzes():
    rows = get_db().execute("SELECT q.*, s.title as story_title FROM quizzes q JOIN stories s ON q.story_id=s.id ORDER BY q.story_id").fetchall()
    return jsonify([dict(r) for r in rows])

@app.route('/api/admin/quizzes', methods=['POST'])
@admin_required
def admin_add_quiz():
    d = request.get_json(); db = get_db()
    db.execute("INSERT INTO quizzes (story_id,question,option_a,option_b,option_c,option_d,correct_answer,explanation) VALUES (?,?,?,?,?,?,?,?)",
        (d['story_id'],d['question'],d['option_a'],d['option_b'],d.get('option_c',''),d.get('option_d',''),d['correct_answer'],d.get('explanation','')))
    db.commit()
    return jsonify({'message':'Pertanyaan ditambahkan'}), 201

@app.route('/api/admin/quizzes/<int:qid>', methods=['PUT'])
@admin_required
def admin_update_quiz(qid):
    d = request.get_json(); db = get_db()
    db.execute("UPDATE quizzes SET question=?,option_a=?,option_b=?,option_c=?,option_d=?,correct_answer=?,explanation=? WHERE id=?",
        (d['question'],d['option_a'],d['option_b'],d.get('option_c',''),d.get('option_d',''),d['correct_answer'],d.get('explanation',''),qid))
    db.commit()
    return jsonify({'message':'Diperbarui'})

@app.route('/api/admin/quizzes/<int:qid>', methods=['DELETE'])
@admin_required
def admin_del_quiz(qid):
    get_db().execute("DELETE FROM quizzes WHERE id=?",(qid,)); get_db().commit()
    return jsonify({'message':'Dihapus'})

@app.route('/api/categories')
def get_categories():
    return jsonify([c['category'] for c in get_db().execute("SELECT DISTINCT category FROM stories WHERE category IS NOT NULL AND category!=''").fetchall()])

@app.route('/api/regions')
def get_regions():
    return jsonify([r['region'] for r in get_db().execute("SELECT DISTINCT region FROM stories WHERE region IS NOT NULL AND region!=''").fetchall()])

@app.route('/api/user/stats')
@login_required
def user_stats():
    db = get_db(); uid = session['user_id']
    return jsonify({
        'stories_read': db.execute("SELECT COUNT(*) c FROM progress WHERE user_id=? AND completed=1",(uid,)).fetchone()['c'],
        'favorites': db.execute("SELECT COUNT(*) c FROM favorites WHERE user_id=?",(uid,)).fetchone()['c'],
        'quizzes_completed': db.execute("SELECT COUNT(*) c FROM quiz_results WHERE user_id=?",(uid,)).fetchone()['c'],
        'stories_uploaded': db.execute("SELECT COUNT(*) c FROM stories WHERE user_id=?",(uid,)).fetchone()['c'],
    })

# ──────────────────────────────────────────────
# SEED DEMO DATA
# ──────────────────────────────────────────────
def seed_demo_data():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    if db.execute("SELECT COUNT(*) c FROM stories").fetchone()['c'] > 0:
        db.close(); return
    uid = db.execute("INSERT INTO users (name,username,email,password_hash,role,status) VALUES (?,?,?,?,'user','active')",
        ('Budi Nusantara','budi_nus','budi@demo.id',generate_password_hash('Budi1234'))).lastrowid
    db.commit()

    stories_data = [
        ('Malin Kundang','Kisah seorang anak durhaka yang dikutuk menjadi batu.','Sumatera Barat','Legenda',
         'Cerita rakyat Minangkabua tentang seorang anak durhaka.','Malin Kundang, Ibu Malin Kundang',
         'Hormati orang tua.','Bahasa Minangkabau','8 menit',1523,1),
        ('Legenda Danau Toba','Asal-usul Danau Toba dari kisah cinta manusia dan ikan.','Sumatera Utara','Legenda',
         'Cerita rakyat tentang asal-usul Danau Toba.','Toba, Putri Ikan',
         'Jangan melanggar sumpah.','Bahasa Batak','7 menit',987,0),
        ('Timun Mas','Kisah gadis dari timun emas yang melarikan diri dari raksasa.','Jawa Tengah','Legenda',
         'Cerita rakyat Jawa tentang Timun Mas.','Timun Mas, Mbok Rondha, Raksasa',
         'Keberanian mengalahkan kekuatan.','Bahasa Jawa','8 menit',1245,1),
        ('Sangkuriang','Kisah cinta terlarang yang menghasilkan Tangkuban Perahu.','Jawa Barat','Legenda',
         'Cerita rakyat Sunda tentang asal-usul Tangkuban Perahu.','Sangkuriang, Dayang Sumbi',
         'Jangan memaksakan kehendak.','Bahasa Sunda','9 menit',1100,1),
        ('Bawang Merah dan Bawang Putih','Dua saudari berbeda sifat, kebaikan selalu menang.','Riau','Cerita Rakyat',
         'Cerita rakyat Melayu tentang dua saudari.','Bawang Putih, Bawang Merah, Ibu Tiri',
         'Kebaikan selalu menang.','Bahasa Melayu','7 menit',876,0),
        ('Keong Mas','Putri cantik dikutuk menjadi keong emas.','Jawa Timur','Legenda',
         'Cerita rakyat Jawa tentang Danau Labuan.','Tutuala, Dewi Galuh, Ratna Bundo',
         'Jangan iri hati.','Bahasa Jawa','7 menit',756,0),
    ]

    story_ids = []
    for sd in stories_data:
        cur = db.execute(
            "INSERT INTO stories (title,description,region,category,content,user_id,author_id,status,is_interactive,characters,moral_value,local_language,reading_duration,views) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (*sd, uid, uid, 'approved')
        )
        story_ids.append(cur.lastrowid)
    db.commit()

    # ── MALIN KUNDANG SCENES ──
    s = story_ids[0]
    sc = [
        ('Kehidupan Sederhana','Di desa kecil pesisir Sumatera Barat, hiduplah seorang ibu miskin dengan anaknya Malin Kundang. Mereka hidup dalam kesederhanaan. Setiap hari ibunya bekerja keras memenuhi kebutuhan hidup. Malin Kundang tumbuh rajin membantu ibunya namun kemiskinan tetap menghimpit.',0,None),
        ('Keberangkatan','Suatu hari Malin Kundang memutuskan merantau mencari kekayaan. Dengan air mata ibunya memberkatinya. "Anakku, pergilah dengan hati baik. Ingat pesan ibumu, jangan sombong dan jangan lupa darimana asalmu."',0,None),
        ('Kesuksesan di Rantau','Bertahun-tahun Malin Kundang merantau. Usahanya membuahkan hasil menjadi saudagar kaya raya dengan kapal besar. Ia menikahi gadis bangsawan. Kekayaan membuatnya berubah dan lupa akan ibunya.',0,None),
        ('Pertemuan di Pelabuhan','Kapal Malin Kundang bersandar dekat kampung halaman. Sang ibu berlari ke pelabuhan. Namun Malin Kundang menolak dan mengusirnya: "Enyah! Aku tidak mengenalmu! Ibu saya wanita bangsawan, bukan gembel!"',None,0,None),
        ('Pilihan Malin Kundang','Sang ibu terpukul. "Ya Tuhan, ampunilah dosa anakku. Jika ia tidak mau mengakuiku, kutuklah dia menjadi batu!" Apa yang seharusnya Malin Kundang lakukan?',0,None),
        ('Penyesalan','Malin Kundang berlutut memohon maaf. "Ibu, maafkan aku!" Sia memeluk ibunya dengan penuh kasih sayang. Ia meninggalkan kekayaan dan merawat ibunya.',1,'alternative'),
        ('Kutukan Batu','Malin Kundang tetap membuang muka. Badai dahsyat menghantam. Tubuhnya berubah menjadi batu. Hingga kini batu Malin Kundang terlihat di Pantai Air Manis, Padang. Pengingat untuk tidak durhaka.',1,'original'),
    ]
    sc_ids = []
    for i,(title,text,isc,endt) in enumerate(sc):
        sc_ids.append(db.execute("INSERT INTO story_scenes (story_id,scene_number,title,text,is_ending,ending_type) VALUES (?,?,?,?,?,?)",(s,i+1,title,text,isc,endt)).lastrowid)
    # Choices at scene 5
    db.execute("INSERT INTO story_choices (scene_id,choice_text,next_scene,choice_letter) VALUES (?,?,?,?)",(sc_ids[4],'Memohon maaf dan mengakui ibunya',sc_ids[0],'A'))
    db.execute("INSERT INTO story_choices (scene_id,choice_text,next_scene,choice_letter) VALUES (?,?,?,?)",(sc_ids[4],'Tetap menolak dan pergi',sc_ids[6],'B'))

    quiz_malin = [
        ('Siapakah tokoh utama cerita Malin Kundang?','Malin Kundang','Ibunya','Saudagar','Nelayan','A','Tokoh utama adalah Malin Kundang.'),
        ('Apa yang dilakukan Malin Kundang di pelabuhan?','Memeluk ibunya','Mengusir ibunya','Memberi uang','Berlari','B','Malin Kundang mengusir ibunya karena malu.'),
        ('Apa akibat perbuatan durhakanya?','Menjadi kaya','Menjadi batu','Menjadi raja','Pulang kampung','B','Ia dikutuk menjadi batu oleh doa ibunya.'),
        ('Di mana batu Malin Kundang?','Pantai Kuta','Pantai Air Manis, Padang','Pantai Parangtritis','Pantai Anyer','B','Di Pantai Air Manis, Padang, Sumatera Barat.'),
        ('Apa nilai moral cerita ini?','Jadilah kaya','Hormati orang tua','Jangan merantau','Jangan berlayar','B','Hormati dan sayangi orang tua.'),
    ]
    for q in quiz_malin:
        db.execute("INSERT INTO quizzes (story_id,question,option_a,option_b,option_c,option_d,correct_answer,explanation) VALUES (?,?,?,?,?,?,?,?)",(s,*q))

    # ── DANAU TOBA SCENES ──
    s = story_ids[1]
    sc_toba = [
        ('Toba dan Ikan Ajaib','Di tanah Batak, hiduplah pemuda bernama Toba. Suatu hari ia memancing dan mendapat ikan bersisik emas. Ketika hendak dimasak, ikan berubah menjadi wanita cantik. Toba menikahinya dan mereka bahagia.',0,None),
        ('Melanggar Sumpah','Toba bersumpah tidak akan memberitahu asal-usul istrinya. Namun saat anaknya bertengkar, anak berteriak "Ibuku keturunan ikan!" Toba memukul anaknya. Anak menangis menemui ibunya.',0,None),
        ('Danau Toba Terbentuk','Istri Toba mengetahui sumpah dilanggar. Dengan air mata ia memisahkan mereka. Tanah retak, air bah muncul. Terbentuklah danau luas yang kini dikenal sebagai Danau Toba.',1,'original'),
    ]
    for i,(t,tx,isc,endt) in enumerate(sc_toba):
        db.execute("INSERT INTO story_scenes (story_id,scene_number,title,text,is_ending,ending_type) VALUES (?,?,?,?,?,?)",(s,i+1,t,tx,isc,endt))
    for q in [
        ('Siapa nama pemuda?','Toba','Sangkuriang','Malin Kundang','Bawang','B','Toba, pemuda petani.'),
        ('Bagaimana pertemuannya?','Di pasar','Ikan berubah jadi wanita','Diperkenalkan tetua','Di hutan','B','Ikan ajaib berubah menjadi wanita cantik.'),
        ('Apa sumpah yang dilanggar?','Tidak menikah','Tidak memberitahu asal istrinya','Tidak berpindah','Tidak memancing','B','Rahasia asal-usul istri.'),
        ('Siapa penyebab pelanggaran?','Toba sendiri','Anaknya','Tetangganya','Istrinya','B','Anak tanpa sengaja membocorkan rahasia.'),
        ('Apa yang terbentuk?','Gunung','Danau Toba','Laut','Sungai','B','Danau Toba dari retakan tanah.'),
    ]:
        db.execute("INSERT INTO quizzes (story_id,question,option_a,option_b,option_c,option_d,correct_answer,explanation) VALUES (?,?,?,?,?,?,?,?)",(s,*q))

    # ── TIMUN MAS SCENES ──
    s = story_ids[2]
    sc_tm = [
        ('Timun Emas','Mbok Rondha hidup sendirian menginginkan anak. Raksasa memberinya timun emas dengan syarat anaknya harus diserahkan di usia 16 tahun. Mbok Rondha menyetujui dan menanam timun itu.',0,None),
        ('Kelahiran Timun Mas','Timun emas berbuah dan dari dalamnya terlahir bayi perempuan cantik. Mbok Rondha menamainya Timun Mas dan membesarkannya dengan penuh kasih sayang.',0,None),
        ('Ancaman Raksasa','Waktu 16 tahun hampir tiba. Pertapa memberi Timun Mas empat benda ajaib: air putih, garam, jarum, dan benang untuk melawan raksasa.',0,None),
        ('Timun Mas vs Raksasa','Raksasa mengejar. Timun Mas melempar air → sungai. Garam → lautan. Jarum → hutan bambu. Benang → ladang mentimun. Raksasa makan mentimun dan tertidur.',0,None),
        ('Akhir Cerita','Raksasa dikubur hidup-hidup. Timun Mas dan Mbok Rondha hidup bahagia. Pengingat tentang keberanian dan cinta kasih seorang ibu.',1,'original'),
    ]
    for i,(t,tx,isc,endt) in enumerate(sc_tm):
        db.execute("INSERT INTO story_scenes (story_id,scene_number,title,text,is_ending,ending_type) VALUES (?,?,?,?,?,?)",(s,i+1,t,tx,isc,endt))
    for q in [
        ('Siapa ibu Timun Mas?','Mbok Ati','Mbok Rondha','Mbok Sri','Mbok Darmi','B','Mbok Rondha mengangkatnya.'),
        ('Dari apa Timun Mas lahir?','Telur emas','Timun emas','Batu ajaib','Bunga','B','Buah timun emas.'),
        ('Benda ajaib apa saja?','Pedang perisai','Air,garam,jarum,benang','Tongkat topi','Panah busur','B','Empat benda ajaib.'),
        ('Apa jadi raksasa?','Terbang','Makan mentimun lalu tertidur','Kabur','Mati','B','Tertidur karena makan mentimun.'),
        ('Nilai moral?','Jangan tanam timun','Keberanian & cinta kasih','Jangan bicara raksasa','Selalu berlari','B','Keberanian mengalahkan kekuatan.'),
    ]:
        db.execute("INSERT INTO quizzes (story_id,question,option_a,option_b,option_c,option_d,correct_answer,explanation) VALUES (?,?,?,?,?,?,?,?)",(s,*q))

    # ── SANGKURIANG SCENES ──
    s = story_ids[3]
    for i,(t,tx,isc,endt) in enumerate([
        ('Sangkuriang dan Tumang','Di Pasundan, Sangkuriang berburu dengan anjing Tumang yang sebenarnya ayahnya. Tumang terluka parah. Sangkuriang membawanya pulang.',0,None),
        ('Kutukan Dayang Sumbi','Dayang Sumbi marah mengetahui Tumang terbunuh. Ia memukul kepala Sangkuriang. "Semoga kita tidak pernah bertemu lagi!" Sangkuriang pergi.',0,None),
        ('Pertemuan Kembali','Bertahun-tahun kemudian, Sangkuriang tumbuh gagah. Ia bertemu wanita cantik yang ternyata Dayang Sumbi ibunya sendiri. Mereka jatuh cinta tanpa saling mengenali.',0,None),
        ('Tantangan Membuat Danau dan Perahu','Dayang Sumbi menyadari ini anaknya. Ia memberi tantangan: buat danau dan perahu dalam satu malam. Sangkuriang menerima dan hampir berhasil.',0,None),
        ('Tangkuban Perahu','Dayang Sumbi memohon para dewa. Langit diterawang merah seperti fajar. Sangkuriang mengira sudah pagi, menendang perahu. Perahu terbalik menjadi gunung Tangkuban Perahu.',1,'original'),
    ]):
        db.execute("INSERT INTO story_scenes (story_id,scene_number,title,text,is_ending,ending_type) VALUES (?,?,?,?,?,?)",(s,i+1,t,tx,isc,endt))
    for q in [
        ('Siapa tokoh utama?','Malin Kundang','Sangkuriang','Toba','Timun Mas','B','Sangkuriang anak Dayang Sumbi.'),
        ('Siapa Tumang?','Anjing peliharaan','Ayah yang berubah wujud','Kuda','Harimau','B','Ayah Sangkuriang berubah wujud.'),
        ('Syarat menikah?','Uang emas','Buat danau dan perahu semalam','Bunuh raksasa','Bangun istana','B','Tantangan dalam satu malam.'),
        ('Apa jadi perahu?','Berlayar','Terbalik jadi gunung','Hilang','Meledak','B','Menjadi Tangkuban Perahu.'),
        ('Lokasi Tangkuban Perahu?','Jakarta','Bandung, Jawa Barat','Yogyakarta','Surabaya','B','Bandung, Jawa Barat.'),
    ]:
        db.execute("INSERT INTO quizzes (story_id,question,option_a,option_b,option_c,option_d,correct_answer,explanation) VALUES (?,?,?,?,?,?,?,?)",(s,*q))

    # ── BAWANG SCENES ──
    s = story_ids[4]
    for i,(t,tx,isc,endt) in enumerate([
        ('Dua Saudari','Bawang Putih baik hati dan rajin. Bawang Merah malas dan jahat. Ibu tiri selalu menyuruh Bawang Putih bekerja keras.',0,None),
        ('Pencarian Ikan','Bawang Putih menangkap ikan cantik. Di jalan ikan terjatuh. Peri mengembalikan ikan dan memberi gaun cantik serta perhiasan emas.',0,None),
        ('Iri Hati','Ibu tiri merampas hadiah untuk Bawang Merah. Bawang Merah ke sungai tapi malas dan tidak mendapat apa-apa.',0,None),
        ('Kemalangan','Bawang Merah membunuh ibunya tanpa sengaja. Mayat dibuang ke sungai. Pangeran menemukan mayat itu.',0,None),
        ('Kebaikan Selalu Menang','Bawang Putih muncul dari peti. Pangeran menikahinya. Bawang Merah menyesal dan memohon maaf. Kebaikan menang.',1,'original'),
    ]):
        db.execute("INSERT INTO story_scenes (story_id,scene_number,title,text,is_ending,ending_type) VALUES (?,?,?,?,?,?)",(s,i+1,t,tx,isc,endt))
    for q in [
        ('Siapa yang baik hati?','Bawang Merah','Bawang Putih','Ibu tiri','Pangeran','B','Bawang Putih baik hati dan rajin.'),
        ('Siapa yang jahat?','Bawang Putih','Ayahnya','Ibu tiri & Bawang Merah','Pangeran','C','Ibu tiri dan Bawang Merah.'),
        ('Apa hadiah peri?','Uang tunai','Gaun & perhiasan emas','Kuda','Pedang','B','Gaun cantik & perhiasan emas.'),
        ('Siapa menikah Bawang Putih?','Bawang Merah','Ibu tiri','Pangeran tampan','Nelayan','C','Pangeran tampan.'),
        ('Nilai moral?','Kekuatan penting','Kebaikan selalu menang','Kekayaan segalanya','Jangan punya saudara','B','Kebaikan selalu dibalas kebaikan.'),
    ]:
        db.execute("INSERT INTO quizzes (story_id,question,option_a,option_b,option_c,option_d,correct_answer,explanation) VALUES (?,?,?,?,?,?,?,?)",(s,*q))

    # ── KEONG MAS SCENES ──
    s = story_ids[5]
    for i,(t,tx,isc,endt) in enumerate([
        ('Tutuala dan Dewi Galuh','Dua putri raja: Tutuala baik hati, Dewi Galuh sombong. Ibu Dewi Galuh selalu menjatuhkan Tutuala.',0,None),
        ('Kutukan Keong Emas','Dewi Galuh mengutuk Tutuala menjadi keong emas dan melemparnya ke sungai.',0,None),
        ('Penemuan Ratna Bundo','Ratna Bundo menemukan keong emas. Keajaiban terjadi, Tutuala muncul dari keong. Ratna Bundo merawatnya.',0,None),
        ('Pengembalian Bentuk','Kebaikan Ratna Bundo memutuskan kutukan. Tutuala kembali menjadi manusia selamanya. Suaminya menemukannya.',0,None),
        ('Balasan Keadilan','Dewi Galuh dikutuk jadi katak. Air mata Tutuala membentuk Danau Labuan di Mojokerto.',1,'original'),
    ]):
        db.execute("INSERT INTO story_scenes (story_id,scene_number,title,text,is_ending,ending_type) VALUES (?,?,?,?,?,?)",(s,i+1,t,tx,isc,endt))
    for q in [
        ('Siapa dikutuk keong?','Dewi Galuh','Tutuala','Ratna Bundo','Ibu Tutuala','B','Tutuala jadi keong emas.'),
        ('Siapa menemukan keong?','Pangeran','Ratna Bundo','Burung','Nelayan','B','Ratna Bundo perempuan tua baik hati.'),
        ('Apa jadi Dewi Galuh?','Menyesal','Katak','Bahagia','Ratu','B','Dikutuk jadi katak.'),
        ('Apa terbentuk dari air mata?','Gunung','Danau Labuan','Laut','Sungai','B','Danau Labuan, Mojokerto.'),
        ('Nilai moral?','Jangan iri hati','Jangan mandi','Jangan percaya orang tua','Jangan jadi keong','A','Jangan serakah dan iri hati.'),
    ]:
        db.execute("INSERT INTO quizzes (story_id,question,option_a,option_b,option_c,option_d,correct_answer,explanation) VALUES (?,?,?,?,?,?,?,?)",(s,*q))

    db.commit(); db.close()
    print("[OK] Demo data seeded!")

# ──────────────────────────────────────────────
if __name__ == '__main__':
    for sub in ['stories','images','videos']:
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], sub), exist_ok=True)
    init_db()
    seed_demo_data()
    print("[OK] Cerita Nusantara running at http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
