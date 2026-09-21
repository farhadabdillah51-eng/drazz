#!/usr/bin/env python3
"""Fix story.js: replace emojis with SVG icons and enhance card placeholders"""
import os

JS_PATH = 'd:/WEBCERITAA/cerita-nusantara/static/js/story.js'

with open(JS_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add ICONS_STORY at the very top of the file
ICONS_BLOCK = """// SVG Icons for Story
const ICONS_STORY = {
    book: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 016.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"/></svg>',
    pencil: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 3a2.83 2.83 0 114 4L7.5 20.5 2 22l1.5-5.5z"/></svg>',
    clock: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
    eye: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>',
    play: '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>',
    quote: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 21c3 0 7-1 7-8V5c0-1.25-.756-2.017-2-2H4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .008-1 1.031V21z"/><path d="M15 21c3 0 7-1 7-8V5c0-1.25-.757-2.017-2-2h-4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2h.75c0 2.25.25 4-2.75 4v3z"/></svg>',
    info: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>',
    map: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    users: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>',
    heart: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg>',
    zap: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    headphones: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 18v-6a9 9 0 0118 0v6"/><path d="M21 19a2 2 0 01-2 2h-1a2 2 0 01-2-2v-3a2 2 0 012-2h3z"/></svg>',
    volume: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/></svg>',
    x: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
    arrow_left: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>',
    arrow_right: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
    sparkle: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
};

"""

# Insert after first line comment
if 'ICONS_STORY' not in content:
    content = content.replace('// story.js', ICONS_BLOCK + '// story.js', 1)

# 2. Fix placeholder emoji
content = content.replace(
    '<div class="story-card-placeholder"><span>\U0001f4d6</span></div>',
    '<div class="story-card-placeholder"><div class="story-placeholder-icon">${ICONS_STORY.book}</div></div>'
)

# 3. Fix video badge
content = content.replace(
    "'\u25b6 Video</span>' : ''}",
    "`${ICONS_STORY.play} Video</span>` : ''}"
)

# 4. Fix story-card-meta icons
content = content.replace(
    '<span>\u23f1 ${s.reading_duration',
    '<span>${ICONS_STORY.clock} ${s.reading_duration'
)
content = content.replace(
    '<span>\U0001f441 ${App.formatNumber',
    '<span>${ICONS_STORY.eye} ${App.formatNumber'
)

# 5. Fix detail page icons
content = content.replace(
    '\u270d\ufe0f ${story.author_name',
    '${ICONS_STORY.pencil} ${story.author_name'
)
content = content.replace(
    '\u23f1 ${story.reading_duration',
    '${ICONS_STORY.clock} ${story.reading_duration'
)
content = content.replace(
    '\U0001f441 ${App.formatNumber',
    '${ICONS_STORY.eye} ${App.formatNumber'
)

# 6. Fix reader buttons
content = content.replace(
    '\u2715 Tutup',
    '${ICONS_STORY.x} Tutup'
)
content = content.replace(
    '\U0001f50a Dengarkan',
    '${ICONS_STORY.headphones} Dengarkan'
)
content = content.replace(
    '\u23f8 Pause',
    '${ICONS_STORY.volume} Pause'
)
content = content.replace(
    '\U0001f4d6 Mulai Membaca',
    '${ICONS_STORY.book} Mulai Membaca'
)
content = content.replace(
    '\U0001f4dd Ikuti Quiz',
    '${ICONS_STORY.pencil} Ikuti Quiz'
)
content = content.replace(
    '"\u25b6 Video Cerita"',
    '"Video Cerita"'
)

# 7. Fix heading icons
content = content.replace(
    '<h2>\U0001f4dd Ringkasan</h2>',
    '<h2>${ICONS_STORY.quote} Ringkasan</h2>'
)
content = content.replace(
    '<h3>\U0001f3ad Kenali Ceritanya</h3>',
    '<h3>${ICONS_STORY.info} Kenali Ceritanya</h3>'
)

# 8. Fix reader nav
content = content.replace(
    '\u2190 Sebelumnya',
    '${ICONS_STORY.arrow_left} Sebelumnya'
)
content = content.replace(
    'Lanjut \u2192',
    'Lanjut ${ICONS_STORY.arrow_right}'
)

# 9. Fix choice prompt
content = content.replace(
    '\U0001f914 Apa yang akan kamu lakukan?',
    'Pilihan Cerita'
)

# 10. Fix ending badges
content = content.replace(
    '<h3>\U0001f500 ENDING ALTERNATIF</h3>',
    '<h3>${ICONS_STORY.zap} ENDING ALTERNATIF</h3>'
)
content = content.replace(
    '<h3>\U0001f4d6 Cerita Asli</h3>',
    '<h3>${ICONS_STORY.book} Cerita Asli</h3>'
)

# 11. Fix notice
content = content.replace(
    '<p>\U0001f4d6 Cerita rakyat dapat memiliki',
    '<p>${ICONS_STORY.info} Cerita rakyat dapat memiliki'
)

with open(JS_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'story.js updated: {os.path.getsize(JS_PATH)} bytes')
print('Done! All emojis replaced with SVG icons.')
