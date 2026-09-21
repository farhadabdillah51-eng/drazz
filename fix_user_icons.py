import os

# SVG Icons library
ICONS = {
    'temple': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="10" width="4" height="10"/><rect x="10" y="6" width="4" height="14"/><rect x="17" y="10" width="4" height="10"/><path d="M2 20h20"/><path d="M12 2v4"/><path d="M4 10h16"/><path d="M8 6l4-4 4 4"/></svg>',
    'bell': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>',
    'home': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    'book': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
    'heart': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>',
    'edit': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>',
    'send': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>',
    'search': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
    'user': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    'fire': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 12c2-2.96 0-7-1-8 0 3.038-1.773 4.741-3 6-1.226 1.26-2 3.24-2 5a6 6 0 1 0 12 0c0-1.532-1.056-3.94-2-5-1.786 3-2.791 3-4 2z"/></svg>',
    'trending': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>',
    'clock': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    'eye': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>',
    'upload': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>',
    'check_circle': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
    'quiz': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    'menu': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>',
    'arrow_right': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
    'arrow_left': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>',
    'logout': '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>',
    'pencil': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/></svg>',
}

icon = lambda name: ICONS.get(name, '')

user_path = 'd:/WEBCERITAA/cerita-nusantara/static/js/user.js'
with open(user_path, 'r', encoding='utf-8') as f:
    old_content = f.read()

new_content = f"""// user.js — User dashboard, profile, my stories, favorites (SVG icons version)
const User = {{
    stats: null,

    async loadStats() {{
        try {{
            const r = await fetch('/api/user/stats');
            this.stats = await r.json();
        }} catch(e) {{ this.stats = {{stories_read:0,favorites:0,quizzes_completed:0,stories_uploaded:0}}; }}
        return this.stats;
    }},

    renderUserNavbar() {{
        const u = Auth.currentUser;
        const I = {{
            home: '{icon("home")}',
            book: '{icon("book")}',
            heart: '{icon("heart")}',
            edit: '{icon("edit")}',
            send: '{icon("send")}',
            bell: '{icon("bell")}',
            user: '{icon("user")}',
            logout: '{icon("logout")}',
            menu: '{icon("menu")}',
            temple: '{icon("temple")}',
        }};
        return `
        <nav class="navbar glass">
            <div class="nav-brand" onclick="App.navigate('#/home')">
                <span class="nav-logo">${{I.temple}}</span>
                <span class="nav-title">CERITA <span class="accent">NUSANTARA</span></span>
            </div>
            <div class="nav-links">
                <a href="#/home" class="nav-link">${{I.home}} Beranda</a>
                <a href="#/stories" class="nav-link">${{I.book}} Cerita</a>
                <a href="#/favorites" class="nav-link">${{I.heart}} Favorit</a>
                <a href="#/my-stories" class="nav-link">${{I.edit}} Cerita Saya</a>
                <a href="#/submit" class="nav-link">${{I.send}} Ajukan Cerita</a>
            </div>
            <div class="nav-right">
                <div class="notif-bell" onclick="User.toggleNotifPanel()" id="notifBell">
                    ${{I.bell}} <span class="notif-badge" id="notifBadge" style="display:none">0</span>
                </div>
                <div class="nav-user" onclick="App.navigate('#/profile')">
                    <div class="nav-avatar">${{(u?.name||'U')[0]}}</div>
                    <span class="nav-username">${{u?.name || 'User'}}</span>
                </div>
                <button class="btn btn-ghost btn-sm" onclick="User.logout()">${{I.logout}} Logout</button>
            </div>
            <button class="nav-mobile-toggle" onclick="User.toggleMobileMenu()">${{I.menu}}</button>
            <div class="nav-mobile-menu" id="mobileMenu">
                <a href="#/home" onclick="User.closeMobileMenu()">${{I.home}} Beranda</a>
                <a href="#/stories" onclick="User.closeMobileMenu()">${{I.book}} Cerita</a>
                <a href="#/favorites" onclick="User.closeMobileMenu()">${{I.heart}} Favorit</a>
                <a href="#/my-stories" onclick="User.closeMobileMenu()">${{I.edit}} Cerita Saya</a>
                <a href="#/submit" onclick="User.closeMobileMenu()">${{I.send}} Ajukan Cerita</a>
                <a href="#/profile" onclick="User.closeMobileMenu()">${{I.user}} Profil</a>
                <button onclick="User.logout()">${{I.logout}} Logout</button>
            </div>
        </nav>
        <div class="notif-panel glass hidden" id="notifPanel"></div>`;
    }},

    toggleMobileMenu() {{
        document.getElementById('mobileMenu')?.classList.toggle('active');
    }},
    closeMobileMenu() {{
        document.getElementById('mobileMenu')?.classList.remove('active');
    }},

    async renderHomePage() {{
        const stats = await this.loadStats();
        const stories = await Story.loadStories({{status:'approved', sort:'popular'}});
        const progress = await (await fetch('/api/progress')).json();
        const newStories = stories.slice(0, 6);
        const u = Auth.currentUser;
        const I = {{
            book: '{icon("book")}',
            heart: '{icon("heart")}',
            quiz: '{icon("quiz")}',
            fire: '{icon("fire")}',
            trending: '{icon("trending")}',
            arrow_right: '{icon("arrow_right")}',
            temple: '{icon("temple")}',
        }};

        return `
        ${{this.renderUserNavbar()}}
        <div class="user-content">
            <section class="hero-section">
                <div class="hero-bg-effects">
                    <div class="hero-glow g1"></div>
                    <div class="hero-glow g2"></div>
                </div>
                <div class="container">
                    <div class="hero-text">
                        <h1>Selamat datang, <span class="accent">${{u?.name || 'Pembaca'}}</span></h1>
                        <p class="hero-subtitle">Temukan cerita baru dan jelajahi kekayaan budaya Nusantara.</p>
                        <div class="hero-stats">
                            <div class="hero-stat glass"><span class="stat-icon">${{I.book}}</span><span class="stat-val">${{stats.stories_read}}</span><span>Dibaca</span></div>
                            <div class="hero-stat glass"><span class="stat-icon">${{I.heart}}</span><span class="stat-val">${{stats.favorites}}</span><span>Favorit</span></div>
                            <div class="hero-stat glass"><span class="stat-icon">${{I.quiz}}</span><span class="stat-val">${{stats.quizzes_completed}}</span><span>Quiz</span></div>
                        </div>
                    </div>
                </div>
            </section>

            ${{progress.length > 0 ? `
            <section class="section">
                <div class="container">
                    <h2 class="section-title">${{I.trending}} Lanjutkan Membaca</h2>
                    <div class="continue-cards">
                        ${{progress.map(p => {{
                            const pct = p.completed ? 100 : Math.min(90, (p.current_scene || 1) * 20);
                            return `
                            <div class="continue-card glass" onclick="Story.startReader(${{p.story_id}})">
                                <div class="continue-info">
                                    <h3>${{p.story_title}}</h3>
                                    <div class="progress-bar"><div class="progress-fill" style="width:${{pct}}%"></div></div>
                                    <span class="text-muted">${{pct}}% selesai</span>
                                </div>
                                <button class="btn btn-primary btn-sm">Lanjutkan ${{I.arrow_right}}</button>
                            </div>`;
                        }}).join('')}}
                    </div>
                </div>
            </section>` : ''}}

            <section class="section">
                <div class="container">
                    <h2 class="section-title">${{I.fire}} Cerita Populer</h2>
                    <div class="stories-grid">${{stories.slice(0,3).map(s => Story.renderStoryCard(s)).join('')}}</div>
                </div>
            </section>

            <section class="section">
                <div class="container">
                    <h2 class="section-title">${{I.trending}} Cerita Terbaru</h2>
                    <div class="stories-grid">${{newStories.map(s => Story.renderStoryCard(s)).join('')}}</div>
                    <div class="section-footer"><a href="#/stories" class="btn btn-ghost">Lihat Semua Cerita ${{I.arrow_right}}</a></div>
                </div>
            </section>

            <footer class="footer glass">
                <div class="container footer-grid">
                    <div><h3>${{I.temple}} CERITA NUSANTARA</h3><p>Menjelajahi kekayaan cerita dan budaya Nusantara melalui pengalaman digital interaktif.</p></div>
                    <div><h4>Menu</h4><a href="#/home">Beranda</a><a href="#/stories">Cerita</a><a href="#/favorites">Favorit</a><a href="#/submit">Ajukan Cerita</a></div>
                    <div><h4>Tentang</h4><p class="text-muted">Dibuat untuk tujuan edukasi dan pelestarian budaya.</p></div>
                </div>
            </footer>
        </div>`;
    }},

    async renderStoriesPage() {{
        const stories = await Story.loadStories({{status:'approved'}});
        const regions = await (await fetch('/api/regions')).json();
        const categories = await (await fetch('/api/categories')).json();
        const I = {{ book: '{icon("book")}', search: '{icon("search")}' }};
        return `
        ${{this.renderUserNavbar()}}
        <div class="user-content">
            <div class="container">
                <div class="page-header"><h1>${{I.book}} Koleksi Cerita</h1><p>Jelajahi kekayaan cerita rakyat Nusantara</p></div>
                <div class="filter-bar glass">
                    <div class="search-box">
                        <span class="search-icon">${{I.search}}</span>
                        <input type="text" id="searchInput" placeholder="Cari cerita rakyat..." oninput="User.filterStories()">
                    </div>
                    <select id="filterRegion" onchange="User.filterStories()"><option value="">Semua Daerah</option>${{regions.map(r=>`<option>${{r}}</option>`).join('')}}</select>
                    <select id="filterCategory" onchange="User.filterStories()"><option value="">Semua Kategori</option>${{categories.map(c=>`<option>${{c}}</option>`).join('')}}</select>
                    <select id="filterSort" onchange="User.filterStories()"><option value="newest">Terbaru</option><option value="popular">Terpopuler</option><option value="oldest">Terlama</option></select>
                </div>
                <div class="stories-grid" id="storiesGrid">${{stories.map(s => Story.renderStoryCard(s)).join('')}}</div>
            </div>
        </div>`;
    }},

    async filterStories() {{
        const params = {{
            status: 'approved',
            search: document.getElementById('searchInput')?.value || '',
            region: document.getElementById('filterRegion')?.value || '',
            category: document.getElementById('filterCategory')?.value || '',
            sort: document.getElementById('filterSort')?.value || 'newest'
        }};
        const stories = await Story.loadStories(params);
        const grid = document.getElementById('storiesGrid');
        if (grid) grid.innerHTML = stories.length ? stories.map(s => Story.renderStoryCard(s)).join('') : '<div class="empty-state"><p>Belum ada cerita yang tersedia.</p></div>';
    }},

    async renderFavoritesPage() {{
        const favs = await (await fetch('/api/favorites')).json();
        const I = {{ heart: '{icon("heart")}' }};
        return `
        ${{this.renderUserNavbar()}}
        <div class="user-content">
            <div class="container">
                <div class="page-header"><h1>${{I.heart}} Cerita Favorit</h1><p>Cerita yang Anda sukai</p></div>
                <div class="stories-grid">${{favs.length ? favs.map(f => Story.renderStoryCard({{
                    id: f.story_id, title: f.title, cover: f.cover, region: f.region,
                    category: f.category, description: f.description, reading_duration: f.reading_duration, views: f.views
                }})).join('') : `<div class="empty-state"><span class="empty-icon">${{I.heart}}</span><p>Belum ada cerita favorit.</p><a href="#/stories" class="btn btn-primary">Jelajahi Cerita</a></div>`}}</div>
            </div>
        </div>`;
    }},

    async renderMyStoriesPage() {{
        const stories = await Story.loadStories({{user_id: Auth.currentUser.id, status: ''}});
        const I = {{ edit: '{icon("edit")}' }};
        return `
        ${{this.renderUserNavbar()}}
        <div class="user-content">
            <div class="container">
                <div class="page-header"><h1>${{I.edit}} Cerita Saya</h1><p>Cerita yang pernah Anda ajukan</p></div>
                <div class="stories-grid">${{stories.length ? stories.map(s => Story.renderStoryCard(s, true)).join('') : `<div class="empty-state"><span class="empty-icon">${{I.edit}}</span><p>Belum ada cerita yang kamu ajukan.</p><a href="#/submit" class="btn btn-primary">Ajukan Cerita</a></div>`}}</div>
            </div>
        </div>`;
    }},

    async renderProfilePage() {{
        const u = Auth.currentUser;
        const stats = await this.loadStats();
        const I = {{
            user: '{icon("user")}',
            book: '{icon("book")}',
            heart: '{icon("heart")}',
            quiz: '{icon("quiz")}',
            upload: '{icon("upload")}',
            pencil: '{icon("pencil")}',
        }};
        return `
        ${{this.renderUserNavbar()}}
        <div class="user-content">
            <div class="container">
                <div class="page-header"><h1>${{I.user}} Profil Saya</h1></div>
                <div class="profile-grid">
                    <div class="profile-card glass">
                        <div class="profile-avatar">${{(u?.name||'U')[0]}}</div>
                        <h2>${{u?.name || ''}}</h2>
                        <p class="text-muted">@${{u?.username || ''}}</p>
                        <p class="text-muted">${{u?.email || ''}}</p>
                        <p class="text-muted">Bergabung: ${{u?.created_at ? new Date(u.created_at).toLocaleDateString('id-ID') : '-'}}</p>
                    </div>
                    <div class="profile-stats-grid">
                        <div class="profile-stat glass"><span class="stat-icon">${{I.book}}</span><span class="stat-val">${{stats.stories_read}}</span><span>Cerita Dibaca</span></div>
                        <div class="profile-stat glass"><span class="stat-icon">${{I.heart}}</span><span class="stat-val">${{stats.favorites}}</span><span>Favorit</span></div>
                        <div class="profile-stat glass"><span class="stat-icon">${{I.quiz}}</span><span class="stat-val">${{stats.quizzes_completed}}</span><span>Quiz Selesai</span></div>
                        <div class="profile-stat glass"><span class="stat-icon">${{I.upload}}</span><span class="stat-val">${{stats.stories_uploaded}}</span><span>Cerita Diunggah</span></div>
                    </div>
                </div>
                <div class="profile-actions"><button class="btn btn-primary" onclick="User.showEditProfile()">${{I.pencil}} Edit Profil</button></div>
            </div>
        </div>`;
    }},

    showEditProfile() {{
        const u = Auth.currentUser;
        App.showModal(`
            <h2>Edit Profil</h2>
            <form onsubmit="User.saveProfile(event)">
                <div class="form-group"><label>Nama</label><input type="text" id="editName" value="${{u?.name||''}}" required></div>
                <div class="form-group"><label>Email</label><input type="email" id="editEmail" value="${{u?.email||''}}" required></div>
                <div class="form-actions"><button type="button" class="btn btn-ghost" onclick="App.closeModal()">Batal</button><button type="submit" class="btn btn-primary">Simpan</button></div>
            </form>
        `);
    }},

    async saveProfile(e) {{
        e.preventDefault();
        try {{
            await fetch('/api/auth/profile', {{
                method:'PUT', headers:{{'Content-Type':'application/json'}},
                body:JSON.stringify({{name:document.getElementById('editName').value, email:document.getElementById('editEmail').value}})
            }});
            Auth.currentUser = await (await fetch('/api/auth/me')).json();
            App.closeModal();
            App.showToast('Profil diperbarui','success');
            App.navigate('#/profile');
        }} catch(e) {{ App.showToast('Gagal memperbarui profil','error'); }}
    }},

    async toggleNotifPanel() {{
        const panel = document.getElementById('notifPanel');
        if (!panel) return;
        panel.classList.toggle('hidden');
        if (!panel.classList.contains('hidden')) {{
            const r = await fetch('/api/notifications');
            const data = await r.json();
            panel.innerHTML = `
                <div class="notif-header"><h3>Notifikasi</h3><button class="btn btn-ghost btn-sm" onclick="User.markAllRead()">Tandai semua dibaca</button></div>
                <div class="notif-list">${{data.notifications.length ? data.notifications.map(n => `
                    <div class="notif-item ${{n.is_read ? '' : 'unread'}}" onclick="User.markRead(${{n.id}})">
                        <strong>${{n.title}}</strong><p>${{n.message}}</p>
                        <span class="text-muted">${{new Date(n.created_at).toLocaleString('id-ID')}}</span>
                    </div>
                `).join('') : '<p class="text-muted" style="padding:1rem">Tidak ada notifikasi.</p>'}}</div>`;
            User.updateNotifBadge();
        }}
    }},

    async updateNotifBadge() {{
        try {{
            const r = await fetch('/api/notifications');
            const data = await r.json();
            const badge = document.getElementById('notifBadge');
            if (badge) {{
                if (data.unread_count > 0) {{
                    badge.textContent = data.unread_count;
                    badge.style.display = '';
                }} else {{
                    badge.style.display = 'none';
                }}
            }}
        }} catch(e) {{}}
    }},

    async markRead(nid) {{
        await fetch(`/api/notifications/${{nid}}/read`, {{method:'POST'}});
        User.updateNotifBadge();
    }},

    async markAllRead() {{
        await fetch('/api/notifications/read-all', {{method:'POST'}});
        User.updateNotifBadge();
        const panel = document.getElementById('notifPanel');
        if (panel) panel.classList.add('hidden');
    }},

    async logout() {{
        App.showModal(`
            <h2>Konfirmasi Logout</h2>
            <p>Apakah Anda yakin ingin keluar?</p>
            <div class="form-actions">
                <button class="btn btn-ghost" onclick="App.closeModal()">Batal</button>
                <button class="btn btn-danger" onclick="User.confirmLogout()">Logout</button>
            </div>
        `);
    }},

    async confirmLogout() {{
        await Auth.logout();
        App.closeModal();
        window.location.hash = '#/login';
    }}
}};
"""

with open(user_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(new_content)
print(f'user.js rewritten: {len(new_content)} chars')

exec(open('d:/WEBCERITAA/cerita-nusantara/build_all.py').read())
print('BUILD DONE!')
