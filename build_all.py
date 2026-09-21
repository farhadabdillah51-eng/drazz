import os

# Build configuration
BASE_DIR = 'd:/WEBCERITAA/cerita-nusantara'
CSS_PATH = os.path.join(BASE_DIR, 'static/css/style.css')
JS_DIR = os.path.join(BASE_DIR, 'static/js')
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates/index.html')

JS_FILES = ['storage.js', 'auth.js', 'story.js', 'quiz.js', 'user.js', 'admin.js', 'app.js']

# Read CSS from style.css file (the single source of truth)
with open(CSS_PATH, 'r', encoding='utf-8') as f:
    css_content = f.read()
print(f'Read CSS from file: {len(css_content)} chars')

# Read all JS files
js_scripts = []
for jf in JS_FILES:
    jpath = os.path.join(JS_DIR, jf)
    with open(jpath, 'r', encoding='utf-8') as f:
        js_content = f.read()
    js_scripts.append(f'    <script>\n// ===== {jf} =====\n{js_content}\n    </script>')
    print(f'Read {jf}: {len(js_content)} chars')

# Build HTML with inline CSS + JS
html = f'''<!DOCTYPE html>
<html lang="id" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CERITA NUSANTARA</title>
    <meta name="description" content="Platform digital interaktif untuk membaca, menjelajahi, dan mempelajari cerita rakyat Indonesia.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
{css_content.strip()}
    </style>
</head>
<body>
    <div id="app"></div>
    <div id="toast-container"></div>
    <div id="modal-overlay" class="modal-overlay hidden">
        <div id="modal-content" class="modal-content"></div>
    </div>
{chr(10).join(js_scripts)}
</body>
</html>
'''

with open(TEMPLATE_PATH, 'w', encoding='utf-8', newline='\n') as f:
    f.write(html)

print(f'\\nHTML written: {len(html)} chars')
print(f'All CSS + JS inlined into: {TEMPLATE_PATH}')
print('BUILD COMPLETE!')
