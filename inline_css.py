import os

# Read all CSS files
css_dir = 'd:/WEBCERITAA/cerita-nusantara/static/css'
css_files = ['style.css', 'auth.css', 'user.css', 'admin.css']
combined_css = ''
for f in css_files:
    with open(os.path.join(css_dir, f), 'r', encoding='utf-8') as fh:
        combined_css += fh.read() + '\n'

# Build the new HTML with inline CSS
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
{combined_css}
    </style>
</head>
<body>
    <div id="app"></div>
    <div id="toast-container"></div>
    <div id="modal-overlay" class="modal-overlay hidden">
        <div id="modal-content" class="modal-content glass"></div>
    </div>
    <script src="/static/js/storage.js?v=4.0"></script>
    <script src="/static/js/auth.js?v=4.0"></script>
    <script src="/static/js/story.js?v=4.0"></script>
    <script src="/static/js/quiz.js?v=4.0"></script>
    <script src="/static/js/user.js?v=4.0"></script>
    <script src="/static/js/admin.js?v=4.0"></script>
    <script src="/static/js/app.js?v=4.0"></script>
</body>
</html>
'''

html_path = 'd:/WEBCERITAA/cerita-nusantara/templates/index.html'
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'OK! HTML with inline CSS written: {len(html)} chars')
print(f'Combined CSS: {len(combined_css)} chars')
print(f'HTML file: {html_path}')
