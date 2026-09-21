import os

# Read story.js
story_path = 'd:/WEBCERITAA/cerita-nusantara/static/js/story.js'
with open(story_path, 'r', encoding='utf-8') as f:
    story_content = f.read()

# New renderSubmitPage with SVG icons
old_submit = story_content.split('renderSubmitPage() {')[1].split('},')[0]
print(f'Found old submit page: {len(old_submit)} chars')

new_submit = ''' renderSubmitPage() {
        const svg = {
            info: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
            edit: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>',
            camera: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>',
            branch: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="6" y1="3" x2="6" y2="15"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/></svg>',
            eye: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>',
            check: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
            send: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>',
            user: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
            map: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg>',
            book: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
            tag: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg>',
            heart: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>',
            clock: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
            file: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><polyline points="13 2 13 9 20 9"/></svg>',
            plus: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>',
        };
        return `<div class="submit-story-page">
        ${User.renderUserNavbar()}
        <div class="user-content">
            <div class="container">
                <div class="submit-hero">
                    <div class="submit-hero-bg">
                        <div class="hero-glow g1"></div>
                        <div class="hero-glow g2"></div>
                    </div>
                    <div class="submit-hero-content">
                        <div class="submit-hero-icon">${svg.send}</div>
                        <h1>Ajukan Cerita</h1>
                        <p>Bagikan kekayaan cerita rakyat Nusantara kepada dunia</p>
                    </div>
                </div>

                <div class="submit-progress">
                    <div class="progress-track"><div class="progress-fill-bar" id="progressFillBar" style="width: 16.6%"></div></div>
                    <div class="progress-steps">
                        <div class="pstep active" data-step="1"><div class="pstep-dot">1</div><span>Informasi</span></div>
                        <div class="pstep" data-step="2"><div class="pstep-dot">2</div><span>Isi Cerita</span></div>
                        <div class="pstep" data-step="3"><div class="pstep-dot">3</div><span>Media</span></div>
                        <div class="pstep" data-step="4"><div class="pstep-dot">4</div><span>Interaktif</span></div>
                        <div class="pstep" data-step="5"><div class="pstep-dot">5</div><span>Preview</span></div>
                        <div class="pstep" data-step="6"><div class="pstep-dot">6</div><span>Kirim</span></div>
                    </div>
                </div>

                <form id="submitStoryForm" class="submit-wizard" onsubmit="Story.handleSubmit(event)" enctype="multipart/form-data">

                    <div class="wiz-step active" data-step="1">
                        <div class="wiz-card glass">
                            <div class="wiz-card-header">
                                <div class="wiz-icon purple">${svg.info}</div>
                                <div><h2>Informasi Cerita</h2><p>Isi data dasar cerita yang akan kamu ajukan</p></div>
                            </div>
                            <div class="wiz-card-body">
                                <div class="form-group">
                                    <label>Judul Cerita</label>
                                    <input type="text" id="stTitle" required placeholder="Masukkan judul cerita rakyat..." class="input-lg">
                                </div>
                                <div class="form-row">
                                    <div class="form-group">
                                        <label><span class="label-icon">${svg.map}</span> Daerah Asal</label>
                                        <input type="text" id="stRegion" required placeholder="Contoh: Sumatera Barat">
                                    </div>
                                    <div class="form-group">
                                        <label><span class="label-icon">${svg.tag}</span> Kategori</label>
                                        <select id="stCategory">
                                            <option value="Legenda">Legenda</option>
                                            <option value="Cerita Rakyat">Cerita Rakyat</option>
                                            <option value="Mitos">Mitos</option>
                                            <option value="Fabel">Fabel</option>
                                            <option value="Sejarah">Sejarah</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label>Deskripsi Singkat</label>
                                    <textarea id="stDesc" rows="3" required placeholder="Ringkasan cerita dalam 2-3 kalimat..." class="input-lg"></textarea>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="wiz-step" data-step="2">
                        <div class="wiz-card glass">
                            <div class="wiz-card-header">
                                <div class="wiz-icon cyan">${svg.edit}</div>
                                <div><h2>Isi Cerita</h2><p>Tuliskan cerita lengkap dengan detail</p></div>
                            </div>
                            <div class="wiz-card-body">
                                <div class="form-group">
                                    <label><span class="label-icon">${svg.book}</span> Isi Cerita Lengkap</label>
                                    <textarea id="stContent" rows="10" required placeholder="Tulis cerita lengkap di sini..." class="input-lg textarea-lg"></textarea>
                                </div>
                                <div class="form-row">
                                    <div class="form-group">
                                        <label><span class="label-icon">${svg.heart}</span> Nilai Moral</label>
                                        <input type="text" id="stMoral" placeholder="Contoh: Hormati orang tua">
                                    </div>
                                    <div class="form-group">
                                        <label><span class="label-icon">${svg.user}</span> Tokoh Utama</label>
                                        <input type="text" id="stChars" placeholder="Contoh: Malin Kundang, Ibu">
                                    </div>
                                </div>
                                <div class="form-row">
                                    <div class="form-group">
                                        <label>Bahasa Daerah</label>
                                        <input type="text" id="stLang" placeholder="Contoh: Bahasa Minang">
                                    </div>
                                    <div class="form-group">
                                        <label><span class="label-icon">${svg.clock}</span> Durasi Membaca</label>
                                        <input type="text" id="stDur" placeholder="Contoh: 8 menit">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="wiz-step" data-step="3">
                        <div class="wiz-card glass">
                            <div class="wiz-card-header">
                                <div class="wiz-icon gold">${svg.camera}</div>
                                <div><h2>Media Pendukung</h2><p>Tambahkan cover dan video (opsional)</p></div>
                            </div>
                            <div class="wiz-card-body">
                                <div class="upload-zone" onclick="document.getElementById('stCover').click()">
                                    <div class="upload-icon">${svg.camera}</div>
                                    <h4>Cover Cerita</h4>
                                    <p>Upload gambar JPG, PNG, atau WebP</p>
                                    <input type="file" id="stCover" accept=".jpg,.jpeg,.png,.webp" style="display:none" onchange="Story.previewCover(this)">
                                    <div id="coverPreview" class="upload-preview"></div>
                                </div>
                                <div class="upload-zone" onclick="document.getElementById('stVideo').click()">
                                    <div class="upload-icon">${svg.eye}</div>
                                    <h4>Video Cerita</h4>
                                    <p>Upload video MP4 atau WebM (opsional)</p>
                                    <input type="file" id="stVideo" accept=".mp4,.webm" style="display:none">
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="wiz-step" data-step="4">
                        <div class="wiz-card glass">
                            <div class="wiz-card-header">
                                <div class="wiz-icon green">${svg.branch}</div>
                                <div><h2>Cerita Interaktif</h2><p>Apa cerita ini memiliki jalur pilihan?</p></div>
                            </div>
                            <div class="wiz-card-body">
                                <div class="toggle-group">
                                    <label class="toggle-option">
                                        <input type="radio" name="interactive" value="0" id="stInterNo" checked>
                                        <div class="toggle-card"><div class="toggle-label">Tidak</div><p>Cerita linear biasa</p></div>
                                    </label>
                                    <label class="toggle-option">
                                        <input type="radio" name="interactive" value="1" id="stInterYes">
                                        <div class="toggle-card"><div class="toggle-label">Ya</div><p>Cerita dengan pilihan</p></div>
                                    </label>
                                </div>
                                <div id="scenesContainer" class="scenes-container"></div>
                                <button type="button" class="btn btn-ghost btn-add-scene" onclick="Story.addSceneField()">
                                    <span class="btn-icon">${svg.plus}</span> Tambah Scene
                                </button>
                            </div>
                        </div>
                    </div>

                    <div class="wiz-step" data-step="5">
                        <div class="wiz-card glass">
                            <div class="wiz-card-header">
                                <div class="wiz-icon purple">${svg.eye}</div>
                                <div><h2>Preview Cerita</h2><p>Periksa tampilan cerita sebelum dikirim</p></div>
                            </div>
                            <div class="wiz-card-body">
                                <div class="submit-preview" id="submitPreview"></div>
                            </div>
                        </div>
                    </div>

                    <div class="wiz-step" data-step="6">
                        <div class="wiz-card glass">
                            <div class="wiz-card-header">
                                <div class="wiz-icon green">${svg.check}</div>
                                <div><h2>Kirim Cerita</h2><p>Cerita akan ditinjau oleh admin sebelum dipublikasikan</p></div>
                            </div>
                            <div class="wiz-card-body">
                                <div class="confirm-box">
                                    <div class="confirm-icon">${svg.send}</div>
                                    <h3>Siap Mengirim?</h3>
                                    <p>Pastikan semua informasi sudah benar. Admin akan meninjau cerita Anda sebelum dipublikasikan.</p>
                                    <button type="submit" class="btn btn-primary btn-lg btn-send">
                                        <span class="btn-icon">${svg.send}</span> Kirim Cerita Sekarang
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="wiz-nav">
                        <button type="button" class="btn btn-ghost" id="prevStepBtn" onclick="Story.prevStep()" style="display:none">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg> Sebelumnya
                        </button>
                        <button type="button" class="btn btn-primary" id="nextStepBtn" onclick="Story.nextStep()">
                            Selanjutnya <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>`;'''

story_content = story_content.replace(
    'renderSubmitPage() {' + old_submit + '},',
    new_submit + '},'
)

# Also add previewCover method
old_add_scene = 'addSceneField() {'
new_add_scene = '''previewCover(input) {
        const preview = document.getElementById('coverPreview');
        if (!preview || !input.files[0]) return;
        const reader = new FileReader();
        reader.onload = (e) => {
            preview.innerHTML = '<img src="' + e.target.result + '" alt="Preview">';
        };
        reader.readAsDataURL(input.files[0]);
    },
    addSceneField() {'''
story_content = story_content.replace(old_add_scene, new_add_scene)

# Write updated story.js
with open(story_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(story_content)
print(f'story.js updated: {len(story_content)} chars')

# Update step dots in nextStep/prevStep
story_content = story_content.replace(
    "document.querySelector(`.step-dot[data-step",
    "document.querySelector(`.pstep[data-step"
)

# Also update all other .step-dot references  
story_content = story_content.replace('.step-dot', '.pstep')

with open(story_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(story_content)
print(f'step-dot references updated')

# Now add the new CSS for submit form to style.css
css_path = 'd:/WEBCERITAA/cerita-nusantara/static/css/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

new_submit_css = """

/* ========== SUBMIT STORY WIZARD ========== */
.submit-story-page { min-height: 100vh; }

.submit-hero {
    position: relative; padding: 60px 0 40px; overflow: hidden;
    background: linear-gradient(180deg, rgba(124,58,237,0.1) 0%, transparent 100%);
}
.submit-hero-bg { position: absolute; inset: 0; pointer-events: none; }
.submit-hero-content { position: relative; z-index: 2; text-align: center; }
.submit-hero-icon {
    width: 72px; height: 72px; margin: 0 auto 20px; border-radius: 20px;
    background: linear-gradient(135deg, var(--purple), var(--cyan));
    display: flex; align-items: center; justify-content: center; color: #fff;
    box-shadow: 0 8px 32px var(--purple-glow);
}
.submit-hero-icon svg { width: 32px; height: 32px; }
.submit-hero-content h1 { font-size: 2rem; margin-bottom: 8px; }
.submit-hero-content p { color: var(--text-secondary); font-size: 1rem; max-width: 400px; margin: 0 auto; }

/* Progress bar */
.submit-progress { margin-bottom: 32px; padding: 0 24px; max-width: 700px; margin-left: auto; margin-right: auto; }
.progress-track { height: 4px; background: rgba(255,255,255,0.06); border-radius: 2px; margin-bottom: 16px; overflow: hidden; }
.progress-fill-bar { height: 100%; background: linear-gradient(90deg, var(--purple), var(--cyan)); border-radius: 2px; transition: width 0.5s ease; }
.progress-steps { display: flex; justify-content: space-between; }
.pstep { display: flex; flex-direction: column; align-items: center; gap: 6px; cursor: pointer; transition: var(--transition); }
.pstep-dot {
    width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem; font-weight: 700; background: rgba(255,255,255,0.06); color: var(--text-muted);
    border: 2px solid transparent; transition: var(--transition);
}
.pstep.active .pstep-dot { background: var(--purple); color: #fff; border-color: var(--purple); box-shadow: 0 0 16px var(--purple-glow); }
.pstep.completed .pstep-dot { background: var(--green); color: #fff; border-color: var(--green); }
.pstep span { font-size: 0.7rem; color: var(--text-muted); font-weight: 500; transition: var(--transition); }
.pstep.active span { color: var(--text-primary); }
.pstep.completed span { color: var(--green); }

/* Wizard steps */
.wiz-step { display: none; animation: fadeSlideUp 0.4s ease; }
.wiz-step.active { display: block; }
@keyframes fadeSlideUp { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: translateY(0); } }

.submit-wizard { max-width: 720px; margin: 0 auto 40px; }

.wiz-card { overflow: hidden; }
.wiz-card-header {
    display: flex; align-items: center; gap: 16px; padding: 24px 28px;
    background: rgba(255,255,255,0.02); border-bottom: 1px solid var(--glass-border);
}
.wiz-icon {
    width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; color: #fff;
}
.wiz-icon.purple { background: linear-gradient(135deg, var(--purple), #9333EA); }
.wiz-icon.cyan { background: linear-gradient(135deg, #0891B2, var(--cyan)); }
.wiz-icon.gold { background: linear-gradient(135deg, #D97706, var(--gold)); }
.wiz-icon.green { background: linear-gradient(135deg, #059669, var(--green)); }
.wiz-icon.red { background: linear-gradient(135deg, #DC2626, var(--red)); }
.wiz-card-header h2 { font-size: 1.15rem; margin-bottom: 2px; }
.wiz-card-header p { font-size: 0.83rem; color: var(--text-muted); }
.wiz-card-body { padding: 28px; }

.label-icon { display: inline-flex; vertical-align: middle; margin-right: 4px; }

.input-lg { padding: 14px 16px !important; font-size: 1rem !important; }
.textarea-lg { min-height: 200px !important; line-height: 1.7 !important; }

/* Upload zones */
.upload-zone {
    border: 2px dashed var(--glass-border); border-radius: var(--radius); padding: 40px 24px;
    text-align: center; cursor: pointer; transition: var(--transition); margin-bottom: 16px;
}
.upload-zone:hover { border-color: var(--purple); background: var(--purple-dim); }
.upload-icon { color: var(--text-muted); margin-bottom: 12px; }
.upload-icon svg { width: 40px; height: 40px; }
.upload-zone h4 { font-size: 1rem; margin-bottom: 4px; }
.upload-zone p { font-size: 0.82rem; color: var(--text-muted); }
.upload-preview { margin-top: 12px; }
.upload-preview img { max-width: 200px; max-height: 140px; border-radius: var(--radius-sm); margin: 0 auto; object-fit: cover; }

/* Toggle group */
.toggle-group { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 20px; }
.toggle-option { cursor: pointer; }
.toggle-option input { display: none; }
.toggle-card {
    padding: 20px; border: 2px solid var(--glass-border); border-radius: var(--radius-sm);
    text-align: center; transition: var(--transition);
}
.toggle-option input:checked + .toggle-card { border-color: var(--purple); background: var(--purple-dim); }
.toggle-label { font-weight: 700; font-size: 1.05rem; margin-bottom: 4px; }
.toggle-card p { font-size: 0.8rem; color: var(--text-muted); }

.scenes-container { display: flex; flex-direction: column; gap: 12px; margin-top: 16px; margin-bottom: 12px; }
.scene-field { padding: 20px; }
.scene-field h4 { font-size: 0.95rem; margin-bottom: 12px; color: var(--purple); }
.btn-add-scene { width: 100%; margin-top: 8px; }

/* Confirm box */
.confirm-box { text-align: center; padding: 40px 20px; }
.confirm-icon {
    width: 80px; height: 80px; margin: 0 auto 20px; border-radius: 50%;
    background: linear-gradient(135deg, var(--purple-dim), var(--cyan-dim));
    display: flex; align-items: center; justify-content: center; color: var(--purple);
}
.confirm-icon svg { width: 36px; height: 36px; }
.confirm-box h3 { font-size: 1.4rem; margin-bottom: 8px; }
.confirm-box p { color: var(--text-muted); margin-bottom: 24px; max-width: 400px; margin-left: auto; margin-right: auto; }
.btn-send { padding: 14px 36px !important; font-size: 1rem !important; }

/* Wizard nav */
.wiz-nav {
    display: flex; justify-content: space-between; align-items: center;
    margin-top: 24px; padding: 0 8px;
}

/* Preview */
.submit-preview .preview-card { padding: 24px; border: 1px solid var(--glass-border); border-radius: var(--radius); }
.submit-preview .preview-card h3 { margin-bottom: 12px; }
.submit-preview .preview-card p { margin-bottom: 8px; font-size: 0.9rem; color: var(--text-secondary); }

@media (max-width: 600px) {
    .progress-steps { gap: 2px; }
    .pstep span { display: none; }
    .toggle-group { grid-template-columns: 1fr; }
}
"""

with open(css_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(css + new_submit_css.strip())
print(f'CSS updated: {len(css + new_submit_css)} chars')

# Rebuild the HTML
exec(open('d:/WEBCERITAA/cerita-nusantara/build_all.py').read())
