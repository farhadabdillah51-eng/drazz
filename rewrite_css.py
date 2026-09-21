import os

base = 'd:/WEBCERITAA/cerita-nusantara/static/css'

style = """/* style.css - Design System */
:root {
    --bg-primary: #070B17;
    --bg-secondary: #0D1326;
    --bg-card: rgba(13,19,38,0.8);
    --text-primary: #F8FAFC;
    --text-secondary: #94A3B8;
    --purple: #7C3AED;
    --purple-dim: rgba(124,58,237,0.2);
    --cyan: #22D3EE;
    --cyan-dim: rgba(34,211,238,0.15);
    --gold: #F5C76B;
    --green: #34D399;
    --red: #EF4444;
    --glass-bg: rgba(13,19,38,0.6);
    --glass-border: rgba(255,255,255,0.08);
    --glass-blur: 20px;
    --radius: 16px;
    --radius-sm: 10px;
    --radius-xs: 6px;
    --shadow: 0 8px 32px rgba(0,0,0,0.3);
    --transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
}
[data-theme="light"] {
    --bg-primary: #F1F5F9;
    --bg-secondary: #E2E8F0;
    --bg-card: rgba(255,255,255,0.85);
    --text-primary: #0F172A;
    --text-secondary: #64748B;
    --glass-bg: rgba(255,255,255,0.7);
    --glass-border: rgba(0,0,0,0.08);
    --shadow: 0 8px 32px rgba(0,0,0,0.1);
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    min-height: 100vh;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    overflow-x: hidden;
}
#app { min-height: 100vh; }
a { color: var(--cyan); text-decoration: none; transition: var(--transition); }
a:hover { color: var(--gold); }
h1, h2, h3, h4, h5, h6 { font-family: 'Playfair Display', serif; line-height: 1.2; }
img { max-width: 100%; display: block; }
button { cursor: pointer; font-family: inherit; }
input, textarea, select { font-family: inherit; }
.glass {
    background: var(--glass-bg);
    backdrop-filter: blur(var(--glass-blur));
    -webkit-backdrop-filter: blur(var(--glass-blur));
    border: 1px solid var(--glass-border);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
}
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 12px 24px;
    border-radius: var(--radius-sm);
    font-weight: 600;
    font-size: 0.95rem;
    border: none;
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}
.btn::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.1), transparent);
    opacity: 0;
    transition: var(--transition);
}
.btn:hover::before { opacity: 1; }
.btn-primary {
    background: linear-gradient(135deg, var(--purple), #9333EA);
    color: #fff;
    box-shadow: 0 4px 16px rgba(124,58,237,0.4);
}
.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(124,58,237,0.5);
}
.btn-secondary {
    background: var(--glass-bg);
    color: var(--text-primary);
    border: 1px solid var(--glass-border);
}
.btn-secondary:hover {
    border-color: var(--purple);
    background: var(--purple-dim);
}
.btn-danger { background: var(--red); color: #fff; }
.btn-success { background: var(--green); color: #fff; }
.btn-full { width: 100%; }
.btn-sm { padding: 8px 16px; font-size: 0.85rem; }
.btn-icon { font-size: 1.1em; }
.form-group {
    margin-bottom: 16px;
    display: flex;
    flex-direction: column;
    gap: 6px;
}
.form-group label {
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--text-secondary);
}
.form-group input,
.form-group textarea,
.form-group select {
    padding: 12px 16px;
    background: rgba(255,255,255,0.05);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-xs);
    color: var(--text-primary);
    font-size: 0.95rem;
    transition: var(--transition);
    outline: none;
}
.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
    border-color: var(--purple);
    box-shadow: 0 0 0 3px var(--purple-dim);
    background: rgba(255,255,255,0.08);
}
.form-group textarea { min-height: 120px; resize: vertical; }
.form-group select {
    appearance: none;
    background-repeat: no-repeat;
    background-position: right 12px center;
    padding-right: 36px;
}
#toast-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 10000;
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.toast {
    padding: 14px 20px;
    border-radius: var(--radius-sm);
    color: #fff;
    font-weight: 500;
    font-size: 0.9rem;
    animation: slideIn 0.3s ease, fadeOut 0.3s ease 2.7s;
    max-width: 400px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    display: flex;
    align-items: center;
    gap: 10px;
}
.toast-success { background: linear-gradient(135deg, #059669, #10B981); }
.toast-error { background: linear-gradient(135deg, #DC2626, #EF4444); }
.toast-info { background: linear-gradient(135deg, #2563EB, #3B82F6); }
@keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}
@keyframes fadeOut {
    to { opacity: 0; transform: translateX(50px); }
}
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.7);
    z-index: 9000;
    display: flex;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(4px);
}
.modal-overlay.hidden { display: none; }
.modal-content {
    max-width: 600px;
    width: 90%;
    max-height: 80vh;
    overflow-y: auto;
    padding: 32px;
}
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--glass-border); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--purple); }
@media (max-width: 768px) {
    .btn { padding: 10px 18px; font-size: 0.88rem; }
    .modal-content { padding: 24px; width: 95%; }
}
"""

with open(os.path.join(base, 'style.css'), 'w', encoding='utf-8') as f:
    f.write(style.strip())
print(f'OK style.css {len(style)} chars')

auth = """/* auth.css - Login & Register */
.auth-page { display: flex; min-height: 100vh; background: var(--bg-primary); }
.auth-visual {
    flex: 1; position: relative; display: flex; align-items: center; justify-content: center;
    overflow: hidden; background: linear-gradient(135deg, #0D1326 0%, #1a0a3e 50%, #0D1326 100%);
}
.auth-visual-bg { position: absolute; inset: 0; overflow: hidden; }
.floating-island { position: absolute; font-size: 3rem; animation: float 6s ease-in-out infinite; opacity: 0.4; }
.floating-island.i1 { top: 20%; left: 20%; animation-delay: 0s; }
.floating-island.i2 { top: 50%; right: 20%; animation-delay: 2s; }
.floating-island.i3 { bottom: 20%; left: 40%; animation-delay: 4s; }
@keyframes float { 0%, 100% { transform: translateY(0) rotate(0deg); } 50% { transform: translateY(-20px) rotate(5deg); } }
.auth-visual-content { position: relative; z-index: 2; text-align: center; padding: 40px; }
.auth-logo-big { margin-bottom: 24px; }
.auth-logo-big .logo-icon { font-size: 4rem; display: block; margin-bottom: 16px; }
.auth-logo-big h1 { font-family: 'Playfair Display', serif; font-size: 3rem; font-weight: 800; color: var(--text-primary); line-height: 1.1; }
.auth-logo-big h1 .accent {
    background: linear-gradient(135deg, var(--purple), var(--cyan));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.auth-tagline { color: var(--text-secondary); font-size: 1.05rem; max-width: 400px; margin: 0 auto; line-height: 1.7; }
.auth-form-area { flex: 1; display: flex; align-items: center; justify-content: center; padding: 40px; }
.auth-form-card { width: 100%; max-width: 420px; padding: 40px; }
.auth-form-header { margin-bottom: 32px; }
.auth-form-header h2 { font-family: 'Playfair Display', serif; font-size: 1.8rem; margin-bottom: 8px; }
.auth-form-header p { color: var(--text-secondary); font-size: 0.95rem; }
.auth-form-card form { display: flex; flex-direction: column; }
.auth-links { display: flex; justify-content: space-between; align-items: center; margin: 16px 0; font-size: 0.85rem; }
.auth-divider { text-align: center; margin: 20px 0; color: var(--text-secondary); font-size: 0.85rem; position: relative; }
.auth-divider::before, .auth-divider::after { content: ''; position: absolute; top: 50%; width: 40%; height: 1px; background: var(--glass-border); }
.auth-divider::before { left: 0; }
.auth-divider::after { right: 0; }
.auth-footer { text-align: center; margin-top: 24px; font-size: 0.9rem; color: var(--text-secondary); }
.register-card { max-width: 480px; }
@media (max-width: 768px) {
    .auth-page { flex-direction: column; }
    .auth-visual { min-height: 40vh; padding: 40px 20px; }
    .auth-logo-big h1 { font-size: 2rem; }
    .auth-form-area { padding: 24px 20px; }
    .auth-form-card { padding: 24px; }
}
"""

with open(os.path.join(base, 'auth.css'), 'w', encoding='utf-8') as f:
    f.write(auth.strip())
print(f'OK auth.css {len(auth)} chars')

user = """/* user.css - User Dashboard */
.page-container { max-width: 1200px; margin: 0 auto; padding: 24px; }
.page-header { margin-bottom: 32px; }
.page-header h1 { font-size: 2rem; margin-bottom: 8px; }
.page-header p { color: var(--text-secondary); }
.navbar {
    background: rgba(7,11,23,0.95); backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--glass-border); padding: 12px 24px;
    display: flex; align-items: center; justify-content: space-between;
    position: sticky; top: 0; z-index: 100;
}
.navbar-brand {
    display: flex; align-items: center; gap: 10px;
    font-family: 'Playfair Display', serif; font-size: 1.3rem; font-weight: 700; color: var(--text-primary);
}
.navbar-brand .brand-accent {
    background: linear-gradient(135deg, var(--purple), var(--cyan));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.navbar-nav { display: flex; align-items: center; gap: 8px; }
.nav-link {
    padding: 8px 16px; border-radius: var(--radius-xs); color: var(--text-secondary);
    font-size: 0.9rem; font-weight: 500; transition: var(--transition); cursor: pointer; border: none; background: none;
}
.nav-link:hover, .nav-link.active { color: var(--text-primary); background: var(--purple-dim); }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 32px; }
.stat-card { padding: 24px; text-align: center; position: relative; overflow: hidden; }
.stat-card::before {
    content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
    background: radial-gradient(circle, var(--purple-dim), transparent 70%); opacity: 0; transition: var(--transition);
}
.stat-card:hover::before { opacity: 1; }
.stat-card .stat-icon { font-size: 2rem; margin-bottom: 8px; }
.stat-card .stat-value { font-size: 2rem; font-weight: 700; color: var(--purple); }
.stat-card .stat-label { font-size: 0.85rem; color: var(--text-secondary); margin-top: 4px; }
.story-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
.story-card {
    background: var(--glass-bg); border: 1px solid var(--glass-border); border-radius: var(--radius);
    overflow: hidden; transition: var(--transition); cursor: pointer;
}
.story-card:hover { transform: translateY(-4px); border-color: var(--purple); box-shadow: 0 8px 32px rgba(124,58,237,0.2); }
.story-card .card-cover { width: 100%; height: 180px; object-fit: cover; background: linear-gradient(135deg, var(--bg-secondary), var(--bg-card)); }
.story-card .card-body { padding: 20px; }
.story-card .card-category {
    display: inline-block; padding: 4px 10px; background: var(--purple-dim); color: var(--purple);
    border-radius: 20px; font-size: 0.75rem; font-weight: 600; margin-bottom: 10px;
}
.story-card .card-title { font-family: 'Playfair Display', serif; font-size: 1.15rem; margin-bottom: 8px; color: var(--text-primary); }
.story-card .card-excerpt {
    font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6; margin-bottom: 16px;
    display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;
}
.story-card .card-meta { display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; color: var(--text-secondary); }
.story-card .card-meta .fav-btn { background: none; border: none; font-size: 1.2rem; cursor: pointer; transition: var(--transition); }
.story-card .card-meta .fav-btn:hover { transform: scale(1.2); }
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.section-header h2 { font-size: 1.5rem; }
.empty-state { text-align: center; padding: 60px 20px; color: var(--text-secondary); }
.empty-state .empty-icon { font-size: 4rem; margin-bottom: 16px; opacity: 0.5; }
.empty-state h3 { font-size: 1.3rem; margin-bottom: 8px; color: var(--text-primary); }
.search-bar { display: flex; gap: 12px; margin-bottom: 24px; }
.search-bar input {
    flex: 1; padding: 12px 16px; background: rgba(255,255,255,0.05); border: 1px solid var(--glass-border);
    border-radius: var(--radius-sm); color: var(--text-primary); font-size: 0.95rem; outline: none; transition: var(--transition);
}
.search-bar input:focus { border-color: var(--purple); box-shadow: 0 0 0 3px var(--purple-dim); }
.category-pills { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; }
.pill {
    padding: 6px 16px; border-radius: 20px; font-size: 0.82rem; font-weight: 500;
    border: 1px solid var(--glass-border); background: transparent; color: var(--text-secondary);
    cursor: pointer; transition: var(--transition);
}
.pill:hover, .pill.active { background: var(--purple-dim); border-color: var(--purple); color: var(--purple); }
.profile-card { max-width: 600px; margin: 0 auto; padding: 32px; }
.profile-avatar {
    width: 80px; height: 80px; border-radius: 50%;
    background: linear-gradient(135deg, var(--purple), var(--cyan));
    display: flex; align-items: center; justify-content: center; font-size: 2rem; margin: 0 auto 20px;
}
.profile-card h2 { text-align: center; margin-bottom: 24px; }
@media (max-width: 768px) {
    .navbar { flex-wrap: wrap; gap: 8px; padding: 12px 16px; }
    .navbar-nav { gap: 4px; }
    .story-grid { grid-template-columns: 1fr; }
    .stats-grid { grid-template-columns: repeat(2, 1fr); }
}
"""

with open(os.path.join(base, 'user.css'), 'w', encoding='utf-8') as f:
    f.write(user.strip())
print(f'OK user.css {len(user)} chars')

admin = """/* admin.css - Admin Dashboard */
.admin-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px; flex-wrap: wrap; gap: 16px; }
.admin-header h1 { font-size: 2rem; }
.admin-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 32px; }
.admin-stat { padding: 24px; text-align: center; position: relative; overflow: hidden; }
.admin-stat::after {
    content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, var(--purple), var(--cyan)); opacity: 0; transition: var(--transition);
}
.admin-stat:hover::after { opacity: 1; }
.admin-stat .stat-number {
    font-size: 2.5rem; font-weight: 800;
    background: linear-gradient(135deg, var(--purple), var(--cyan));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.admin-stat .stat-label { font-size: 0.85rem; color: var(--text-secondary); margin-top: 4px; }
.admin-table-wrapper { overflow-x: auto; }
.admin-table { width: 100%; border-collapse: collapse; }
.admin-table th, .admin-table td { padding: 14px 16px; text-align: left; border-bottom: 1px solid var(--glass-border); }
.admin-table th { color: var(--text-secondary); font-size: 0.82rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
.admin-table td { font-size: 0.9rem; }
.admin-table tr:hover td { background: rgba(124,58,237,0.05); }
.badge { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
.badge-approved { background: rgba(52,211,153,0.15); color: var(--green); }
.badge-pending { background: rgba(245,199,107,0.15); color: var(--gold); }
.badge-rejected { background: rgba(239,68,68,0.15); color: var(--red); }
.badge-admin { background: var(--purple-dim); color: var(--purple); }
.action-btns { display: flex; gap: 6px; }
.action-btns .btn { padding: 6px 12px; font-size: 0.8rem; }
.admin-tabs { display: flex; gap: 4px; margin-bottom: 24px; border-bottom: 1px solid var(--glass-border); padding-bottom: 0; }
.admin-tab {
    padding: 10px 20px; font-size: 0.9rem; font-weight: 500; color: var(--text-secondary);
    background: none; border: none; border-bottom: 2px solid transparent;
    cursor: pointer; transition: var(--transition); margin-bottom: -1px;
}
.admin-tab:hover { color: var(--text-primary); }
.admin-tab.active { color: var(--purple); border-bottom-color: var(--purple); }
.glow-card { position: relative; overflow: hidden; }
.glow-card::before {
    content: ''; position: absolute; top: -2px; left: -2px; right: -2px; bottom: -2px;
    background: linear-gradient(45deg, var(--purple), var(--cyan), var(--gold), var(--purple));
    border-radius: calc(var(--radius) + 2px); z-index: -1; opacity: 0; transition: var(--transition);
    background-size: 300% 300%; animation: glowRotate 4s linear infinite;
}
.glow-card:hover::before { opacity: 1; }
@keyframes glowRotate {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@media (max-width: 768px) {
    .admin-stats { grid-template-columns: repeat(2, 1fr); }
    .admin-table th:nth-child(n+4), .admin-table td:nth-child(n+4) { display: none; }
}
"""

with open(os.path.join(base, 'admin.css'), 'w', encoding='utf-8') as f:
    f.write(admin.strip())
print(f'OK admin.css {len(admin)} chars')

# Verify
for fname in sorted(os.listdir(base)):
    fpath = os.path.join(base, fname)
    sz = os.path.getsize(fpath)
    print(f'  {fname}: {sz} bytes')
