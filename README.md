# 🏛️ CERITA NUSANTARA

Platform digital interaktif untuk membaca, menjelajahi, dan mempelajari cerita rakyat Indonesia.

---

## 🚀 Cara Membuka / Menjalankan Website

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Build Frontend (CSS + JS)

```bash
python build_all.py
```

### 3. Jalankan Server

```bash
python app.py
```

### 4. Buka di Browser

Buka link berikut di browser Anda:

| Link | Keterangan |
|------|------------|
| **[http://127.0.0.1:5000](http://127.0.0.1:5000)** | Localhost |
| **[http://localhost:5000](http://localhost:5000)** | Localhost (alternatif) |
| **[http://192.168.1.12:5000](http://192.168.1.12:5000)** | Akses dari perangkat lain di jaringan yang sama |

---

## 🔑 Akun Demo

| Role | Username | Password |
|------|----------|----------|
| **Admin** | `admin` | `Admin123!` |
| **User** | `farhad` | `farhad123` |

---

## 📁 Struktur Project

```
cerita-nusantara/
├── app.py                 # Backend Flask (API & routes)
├── build_all.py           # Build script (inline CSS + JS ke HTML)
├── requirements.txt       # Python dependencies
├── database/
│   └── cerita_nusantara.db  # SQLite database (otomatis dibuat)
├── static/
│   ├── css/
│   │   ├── style.css      # Main design system
│   │   ├── auth.css       # Login & Register styles
│   │   ├── user.css       # User dashboard styles
│   │   └── admin.css      # Admin dashboard styles
│   └── js/
│       ├── storage.js     # LocalStorage helper
│       ├── auth.js        # Authentication logic
│       ├── story.js       # Story reader & submit page
│       ├── quiz.js        # Quiz system
│       ├── user.js        # User dashboard & pages
│       ├── admin.js       # Admin dashboard
│       └── app.js         # Router & app initialization
├── templates/
│   └── index.html         # Generated HTML (build output)
└── uploads/               # User uploaded files
    ├── stories/
    ├── images/
    └── videos/
```

---

## 🛠 Tech Stack

- **Backend**: Python Flask + SQLite
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Design**: Dark theme, Glassmorphism, SVG icons
- **Auth**: Session-based with password hashing (Werkzeug)

---

## ✨ Fitur

- **Homepage**: Cerita populer & terbaru dengan animasi modern
- **Story Reader**: Baca cerita interaktif dengan pilihan jalur
- **Quiz**: Kuis interaktif berbasis cerita
- **Submit Story**: Wizard 6 langkah untuk mengajukan cerita baru
- **Favorit**: Simpan cerita favorit
- **Profil**: Lihat statistik baca & edit profil
- **Admin Dashboard**: Kelola cerita, pengguna, quiz, dan komentar
- **Notifikasi**: Sistem notifikasi real-time

---

## 📝 Catatan

- Database dan folder uploads dibuat **otomatis** saat pertama kali menjalankan `python app.py`
- Setelah mengubah file CSS atau JS, jalankan `python build_all.py` lalu restart server
- Website menggunakan **Single Page Application (SPA)** dengan hash-based routing
