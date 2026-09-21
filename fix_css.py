#!/usr/bin/env python3
"""Append story enhancement CSS to style.css"""
import os

CSS_PATH = 'd:/WEBCERITAA/cerita-nusantara/static/css/style.css'

CSS_ADD = """
/* ========== STORY CARDS COVER ENHANCEMENTS ========== */
.story-card { border-radius: 16px; overflow: hidden; transition: transform 0.3s ease, box-shadow 0.3s ease; cursor: pointer; }
.story-card:hover { transform: translateY(-6px); box-shadow: 0 12px 40px rgba(124,58,237,0.25); }
.story-card-img { position: relative; height: 200px; overflow: hidden; }
.story-card-img img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s ease; }
.story-card:hover .story-card-img img { transform: scale(1.08); }
.story-card-overlay { position: absolute; inset: 0; background: linear-gradient(180deg, transparent 40%, rgba(7,11,23,0.9) 100%); z-index: 1; }
.story-card-img .badge { position: absolute; top: 12px; z-index: 2; }
.story-card-img .badge:first-child { left: 12px; }
.story-card-img .badge:nth-child(2) { left: auto; right: 12px; }
.story-card-img .badge-video { position: absolute; top: 12px; right: 12px; z-index: 2; }
.story-card-body { padding: 16px 20px 20px; }
.story-card-title { font-size: 1.1rem; font-weight: 700; margin-bottom: 6px; line-height: 1.3; }
.story-card-desc { font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5; margin-bottom: 12px; }
.story-card-meta { display: flex; gap: 16px; align-items: center; font-size: 0.8rem; color: var(--text-muted); }
.story-card-meta span { display: inline-flex; align-items: center; gap: 4px; }
.story-card-meta svg { width: 14px; height: 14px; flex-shrink: 0; }
.story-card-meta span:nth-child(2) { color: var(--green); }
.story-card-placeholder { display: flex; align-items: center; justify-content: center; height: 200px; background: linear-gradient(135deg, var(--purple-dim), var(--cyan-dim)); }
.story-placeholder-icon svg { width: 48px; height: 48px; opacity: 0.3; }

/* Badge styling improvements */
.badge-region { background: linear-gradient(135deg, rgba(124,58,237,0.85), rgba(124,58,237,0.6)) !important; backdrop-filter: blur(8px); }
.badge-category { background: linear-gradient(135deg, rgba(6,182,212,0.85), rgba(6,182,212,0.6)) !important; backdrop-filter: blur(8px); }
.badge-video { background: linear-gradient(135deg, rgba(220,38,38,0.85), rgba(220,38,38,0.6)) !important; backdrop-filter: blur(8px); display: inline-flex; align-items: center; gap: 4px; }
.badge svg { width: 12px; height: 12px; }

/* Story cards grid */
.story-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 24px; }
@media (max-width: 768px) { .story-grid { grid-template-columns: 1fr; } }

/* Story detail hero enhancements */
.story-hero { position: relative; min-height: 400px; display: flex; align-items: flex-end; }
.story-hero-bg { position: absolute; inset: 0; background-size: cover; background-position: center; }
.story-hero-overlay { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(7,11,23,0.3) 0%, rgba(7,11,23,0.95) 80%); z-index: 1; }
.story-hero-content { position: relative; z-index: 2; padding: 40px 32px; max-width: 800px; }
.story-hero-content h1 { font-size: 2.2rem; font-weight: 800; margin: 12px 0 8px; line-height: 1.2; }
.story-hero-desc { color: var(--text-secondary); font-size: 1rem; line-height: 1.6; margin-bottom: 16px; }
.story-info-row { display: flex; gap: 20px; margin-bottom: 20px; font-size: 0.9rem; color: var(--text-muted); }
.story-info-row span { display: inline-flex; align-items: center; gap: 6px; }
.story-info-row svg { width: 16px; height: 16px; }
.story-actions { display: flex; gap: 12px; flex-wrap: wrap; }

/* Story section improvements */
.story-section { padding: 32px 0; }
.story-section h2 { font-size: 1.3rem; font-weight: 700; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
.story-section h2 svg { width: 24px; height: 24px; color: var(--purple); }
.story-content-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 24px; }
@media (max-width: 768px) { .story-content-grid { grid-template-columns: 1fr; } }
.story-main-content { padding: 28px; border-radius: var(--radius); }
.story-text { font-size: 1rem; line-height: 1.8; color: var(--text-secondary); }
.story-sidebar { display: flex; flex-direction: column; gap: 16px; }
.story-info-card { padding: 24px; border-radius: var(--radius); }
.story-info-card h3 { font-size: 1.1rem; font-weight: 700; margin-bottom: 14px; display: flex; align-items: center; gap: 8px; }
.story-info-card h3 svg { width: 20px; height: 20px; color: var(--cyan); }
.info-item { padding: 10px 0; border-bottom: 1px solid var(--glass-border); font-size: 0.9rem; color: var(--text-secondary); }
.info-item:last-child { border-bottom: none; }
.info-item strong { color: var(--text-primary); font-weight: 600; }

/* Reader page enhancements */
.reader-page { min-height: 100vh; padding-bottom: 80px; }
.reader-header { display: flex; align-items: center; justify-content: space-between; padding: 14px 24px; position: sticky; top: 0; z-index: 100; border-bottom: 1px solid var(--glass-border); backdrop-filter: blur(16px); }
.reader-progress-info { flex: 1; margin: 0 24px; text-align: center; }
.reader-progress-info span { font-size: 0.82rem; color: var(--text-muted); margin-bottom: 4px; display: block; }
.progress-bar { height: 4px; background: rgba(255,255,255,0.08); border-radius: 2px; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg, var(--purple), var(--cyan)); border-radius: 2px; transition: width 0.4s ease; }
.reader-controls-top { display: flex; align-items: center; gap: 8px; }
.tts-speed-select { background: var(--glass-bg); border: 1px solid var(--glass-border); color: var(--text-primary); border-radius: 8px; padding: 4px 8px; font-size: 0.78rem; cursor: pointer; }
.reader-body { max-width: 740px; margin: 0 auto; padding: 40px 24px; }
.reader-scene-title { font-size: 1.6rem; font-weight: 800; margin-bottom: 24px; color: var(--text-primary); line-height: 1.3; }
.reader-text p { font-size: 1.1rem; line-height: 2; color: var(--text-secondary); margin-bottom: 20px; text-align: justify; }
.reader-image { width: 100%; border-radius: var(--radius); margin-bottom: 24px; max-height: 360px; object-fit: cover; }
.reader-footer { display: flex; justify-content: space-between; align-items: center; padding: 16px 24px; position: fixed; bottom: 0; left: 0; right: 0; z-index: 100; border-top: 1px solid var(--glass-border); backdrop-filter: blur(16px); }

/* Ending badges */
.ending-badge { padding: 24px; border-radius: var(--radius); text-align: center; margin-top: 32px; }
.ending-original { border: 2px solid var(--green); background: rgba(34,197,94,0.08); }
.ending-alternative { border: 2px solid var(--purple); background: rgba(124,58,237,0.08); }
.ending-badge h3 { font-size: 1.1rem; font-weight: 700; margin-bottom: 6px; display: flex; align-items: center; justify-content: center; gap: 8px; }
.ending-badge h3 svg { width: 20px; height: 20px; }

/* Choice container */
.choice-container { margin-top: 32px; }
.choice-container h3 { font-size: 1.2rem; font-weight: 700; margin-bottom: 16px; text-align: center; display: flex; align-items: center; justify-content: center; gap: 8px; }
.choice-cards { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
@media (max-width: 600px) { .choice-cards { grid-template-columns: 1fr; } }
.choice-card { padding: 20px; cursor: pointer; transition: var(--transition); border: 2px solid var(--glass-border); border-radius: var(--radius-sm); text-align: center; }
.choice-card:hover { border-color: var(--purple); background: var(--purple-dim); transform: translateY(-2px); }
.choice-letter { width: 32px; height: 32px; border-radius: 50%; background: var(--purple); color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 700; margin: 0 auto 8px; font-size: 0.9rem; }

/* Interactive badge */
.interactive-badge { border: 2px dashed var(--purple); text-align: center; }
.interactive-badge h3 { justify-content: center; color: var(--purple); }
.interactive-badge p { color: var(--text-muted); font-size: 0.9rem; }
.content-notice { padding: 24px 0; }
.notice-card { padding: 20px 24px; border-left: 4px solid var(--purple); border-radius: var(--radius-sm); }
.notice-card p { font-size: 0.9rem; color: var(--text-muted); line-height: 1.6; display: flex; align-items: flex-start; gap: 8px; }
.notice-card p svg { flex-shrink: 0; margin-top: 2px; }
"""

with open(CSS_PATH, 'a', encoding='utf-8') as f:
    f.write(CSS_ADD)

size = os.path.getsize(CSS_PATH)
print(f'CSS updated: {size} bytes')
print('Done!')
