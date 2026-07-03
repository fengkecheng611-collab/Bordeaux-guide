# -*- coding: utf-8 -*-
"""波尔多生活指南 — Flask 知识库应用"""

import os
import re
import secrets
import shutil
import yaml
import markdown
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(BASE_DIR, 'content')
PENDING_DIR = os.path.join(CONTENT_DIR, 'pending')
UPLOAD_DIR = os.path.join(BASE_DIR, 'static', 'uploads')

# Admin password — defaults to 'bordeaux2026', override with ADMIN_PASSWORD env var
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'bordeaux2026')

# Allowed image types and max size (5MB)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_IMAGE_SIZE = 5 * 1024 * 1024

# Color options for article cards
CARD_COLORS = {
    'red':    {'name': '波尔多红', 'css': '#8b1a2b', 'light': '#f5e6e8'},
    'blue':   {'name': '海洋蓝',   'css': '#1a6b8b', 'light': '#e6f0f5'},
    'green':  {'name': '葡萄绿',   'css': '#3a7d44', 'light': '#edf7ee'},
    'purple': {'name': '薰衣草紫', 'css': '#6b3a7d', 'light': '#f3eef7'},
    'orange': {'name': '阳光橙',   'css': '#c06a20', 'light': '#fdf3e8'},
    'teal':   {'name': '薄荷青',   'css': '#1a7d6b', 'light': '#e8f7f3'},
}

CATEGORIES = {
    'yi':  {'name': '衣', 'icon': '👔', 'dir': 'yi'},
    'shi': {'name': '食', 'icon': '🍽️', 'dir': 'shi'},
    'zhu': {'name': '住', 'icon': '🏠', 'dir': 'zhu'},
    'xing':{'name': '行', 'icon': '🚌', 'dir': 'xing'},
    'wan': {'name': '玩', 'icon': '🎯', 'dir': 'wan'},
    'app': {'name': 'App', 'icon': '📱', 'dir': 'app'},
}

os.makedirs(PENDING_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def parse_article(filepath):
    """Parse a Markdown file with YAML frontmatter. Returns (meta, html_content)."""
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    meta = {}
    body = content

    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                meta = yaml.safe_load(parts[1]) or {}
            except yaml.YAMLError:
                pass
            body = parts[2].strip()

    html = markdown.markdown(body, extensions=['extra', 'nl2br', 'sane_lists'])

    excerpt = ''
    for line in body.split('\n'):
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('!') and not line.startswith('<'):
            excerpt = line[:150] + ('…' if len(line) > 150 else '')
            break

    return meta, html, excerpt


def get_articles(category_key=None):
    """Get all articles, optionally filtered by category."""
    articles = []
    dirs_to_scan = [category_key] if category_key else CATEGORIES.keys()

    for cat_key in dirs_to_scan:
        cat_dir = os.path.join(CONTENT_DIR, cat_key)
        if not os.path.isdir(cat_dir):
            continue

        for filename in sorted(os.listdir(cat_dir)):
            if not filename.endswith('.md'):
                continue

            filepath = os.path.join(cat_dir, filename)
            meta, html, excerpt = parse_article(filepath)

            articles.append({
                'id': filename.replace('.md', ''),
                'filename': filename,
                'category_key': cat_key,
                'category_name': meta.get('category', CATEGORIES.get(cat_key, {}).get('name', cat_key)),
                'title': meta.get('title', filename.replace('.md', '').replace('_', ' ')),
                'author': meta.get('author', '匿名'),
                'date': meta.get('date', ''),
                'color': meta.get('color', 'red'),
                'excerpt': excerpt,
                'html': html,
                'filepath': filepath,
                'edit_key': meta.get('edit_key', ''),
            })

    articles.sort(key=lambda a: a['date'], reverse=True)
    return articles


def search_articles(query):
    """Search articles by title and content."""
    if not query:
        return []

    results = []
    all_articles = get_articles()

    for article in all_articles:
        score = 0
        query_lower = query.lower()
        if query_lower in article['title'].lower():
            score += 10

        with open(article['filepath'], 'r', encoding='utf-8') as f:
            content = f.read().lower()
            count = content.count(query_lower)
            if count > 0:
                score += count

        if score > 0:
            article['score'] = score
            idx = content.find(query_lower)
            if idx != -1:
                start = max(0, idx - 40)
                end = min(len(content), idx + len(query) + 80)
                snippet = content[start:end]
                if start > 0:
                    snippet = '…' + snippet
                if end < len(content):
                    snippet = snippet + '…'
                article['snippet'] = snippet
            results.append(article)

    results.sort(key=lambda r: r['score'], reverse=True)
    return results


def get_pending_articles():
    """Get articles in the pending review directory."""
    articles = []
    if not os.path.isdir(PENDING_DIR):
        return articles

    for filename in sorted(os.listdir(PENDING_DIR)):
        if not filename.endswith('.md'):
            continue
        filepath = os.path.join(PENDING_DIR, filename)
        meta, html, excerpt = parse_article(filepath)
        articles.append({
            'id': filename.replace('.md', ''),
            'filename': filename,
            'title': meta.get('title', ''),
            'author': meta.get('author', '匿名'),
            'date': meta.get('date', ''),
            'category': meta.get('category', '未知'),
            'html': html,
            'filepath': filepath,
        })
    return articles


# ─── Public Routes ─────────────────────────────────────────────

@app.route('/')
def index():
    all_articles = get_articles()
    grouped = {}
    for cat_key, cat_info in CATEGORIES.items():
        grouped[cat_key] = {
            'info': cat_info,
            'articles': [a for a in all_articles if a['category_key'] == cat_key],
        }
    return render_template('index.html', grouped=grouped, categories=CATEGORIES, colors=CARD_COLORS)


@app.route('/category/<cat_key>/')
def category(cat_key):
    if cat_key not in CATEGORIES:
        return redirect(url_for('index'))
    articles = get_articles(cat_key)
    return render_template('category.html', cat_key=cat_key,
                           cat_info=CATEGORIES[cat_key], articles=articles,
                           categories=CATEGORIES, colors=CARD_COLORS)


@app.route('/post/<cat_key>/<article_id>/')
def post(cat_key, article_id):
    filename = article_id + '.md'
    filepath = os.path.join(CONTENT_DIR, cat_key, filename)
    if not os.path.exists(filepath):
        return redirect(url_for('index'))

    meta, html, excerpt = parse_article(filepath)
    cat_articles = get_articles(cat_key)
    prev_article = next_article = None
    for i, a in enumerate(cat_articles):
        if a['id'] == article_id:
            if i > 0:
                prev_article = cat_articles[i - 1]
            if i < len(cat_articles) - 1:
                next_article = cat_articles[i + 1]
            break

    return render_template('post.html', cat_key=cat_key, article_id=article_id,
                           title=meta.get('title', article_id),
                           author=meta.get('author', '匿名'),
                           date=meta.get('date', ''),
                           category_name=CATEGORIES.get(cat_key, {}).get('name', cat_key),
                           html=html, prev_article=prev_article,
                           next_article=next_article, categories=CATEGORIES)


@app.route('/search/')
def search():
    query = request.args.get('q', '').strip()
    results = search_articles(query) if query else []
    return render_template('search.html', query=query, results=results, categories=CATEGORIES)


@app.route('/contribute/', methods=['GET', 'POST'])
def contribute():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        cat_key = request.form.get('category', '').strip()
        author = request.form.get('author', '').strip()
        card_color = request.form.get('color', 'red').strip()
        content = request.form.get('content', '').strip()

        if not title or not cat_key or not content:
            flash('请填写标题、分类和正文内容。', 'error')
            return render_template('contribute.html', categories=CATEGORIES, colors=CARD_COLORS)

        if cat_key not in CATEGORIES:
            flash('请选择有效的分类。', 'error')
            return render_template('contribute.html', categories=CATEGORIES, colors=CARD_COLORS)

        # Handle image upload
        image_file = request.files.get('image')
        image_md = ''
        if image_file and image_file.filename and allowed_file(image_file.filename):
            # Check file size
            image_file.seek(0, os.SEEK_END)
            size = image_file.tell()
            image_file.seek(0)
            if size > MAX_IMAGE_SIZE:
                flash('图片不能超过 5MB。', 'error')
                return render_template('contribute.html', categories=CATEGORIES, colors=CARD_COLORS)

            safe_name = secure_filename(image_file.filename)
            # Add random prefix to avoid name collision
            unique_name = f"{secrets.token_hex(4)}_{safe_name}"
            image_path = os.path.join(UPLOAD_DIR, unique_name)
            image_file.save(image_path)
            image_md = f'\n![{title}配图](/static/uploads/{unique_name})\n'

        # Generate edit key
        edit_key = secrets.token_urlsafe(12)

        today = datetime.now().strftime('%Y%m%d')
        safe_title = re.sub(r'[^\w\s-]', '', title)
        safe_title = re.sub(r'[-\s]+', '_', safe_title)
        filename = f'contrib_{today}_{safe_title[:30]}.md'

        article_content = f"""---
title: "{title}"
category: "{CATEGORIES[cat_key]['name']}"
author: "{author or '匿名'}"
date: "{datetime.now().strftime('%Y-%m-%d')}"
color: "{card_color}"
edit_key: "{edit_key}"
---

{content}
{image_md}
"""
        filepath = os.path.join(PENDING_DIR, filename)
        os.makedirs(PENDING_DIR, exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(article_content)

        edit_url = url_for('edit_article', cat_key=cat_key, article_id=filename.replace('.md', ''),
                           edit_key=edit_key, _external=True)

        flash(f'投稿成功！你的文章"{title}"已提交审核。', 'success')
        return render_template('contribute_success.html',
                               title=title, edit_url=edit_url, edit_key=edit_key,
                               categories=CATEGORIES)

    return render_template('contribute.html', categories=CATEGORIES, colors=CARD_COLORS)


# ─── Edit Key Routes ──────────────────────────────────────────

@app.route('/edit/<cat_key>/<article_id>/<edit_key>/', methods=['GET', 'POST'])
def edit_article(cat_key, article_id, edit_key):
    """Edit an article using its edit key."""
    # Check both pending and published directories
    filepath = os.path.join(PENDING_DIR, article_id + '.md')
    is_pending = os.path.exists(filepath)
    if not is_pending:
        filepath = os.path.join(CONTENT_DIR, cat_key, article_id + '.md')

    if not os.path.exists(filepath):
        flash('文章不存在。', 'error')
        return redirect(url_for('index'))

    meta, html, excerpt = parse_article(filepath)

    if meta.get('edit_key', '') != edit_key:
        flash('编辑密钥不正确，无法编辑此文章。', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        content = request.form.get('content', '').strip()

        if not title or not content:
            flash('标题和正文不能为空。', 'error')
            return render_template('edit.html', article=meta, body=body_text(filepath),
                                   cat_key=cat_key, article_id=article_id,
                                   edit_key=edit_key, categories=CATEGORIES)

        # Handle image upload
        image_file = request.files.get('image')
        image_md = ''
        if image_file and image_file.filename and allowed_file(image_file.filename):
            image_file.seek(0, os.SEEK_END)
            size = image_file.tell()
            image_file.seek(0)
            if size <= MAX_IMAGE_SIZE:
                safe_name = secure_filename(image_file.filename)
                unique_name = f"{secrets.token_hex(4)}_{safe_name}"
                image_path = os.path.join(UPLOAD_DIR, unique_name)
                image_file.save(image_path)
                image_md = f'\n![{title}配图](/static/uploads/{unique_name})\n'

        updated = f"""---
title: "{title}"
category: "{meta.get('category', CATEGORIES.get(cat_key, {}).get('name', ''))}"
author: "{author or meta.get('author', '匿名')}"
date: "{meta.get('date', '')}"
edit_key: "{edit_key}"
last_modified: "{datetime.now().strftime('%Y-%m-%d %H:%M')}"
---

{content}
{image_md}
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated)

        flash(f'文章"{title}"已更新。', 'success')
        if is_pending:
            return redirect(url_for('index'))
        else:
            return redirect(url_for('post', cat_key=cat_key, article_id=article_id))

    # GET — show edit form
    body = body_text(filepath)
    return render_template('edit.html', article=meta, body=body,
                           cat_key=cat_key, article_id=article_id,
                           edit_key=edit_key, categories=CATEGORIES)


def body_text(filepath):
    """Extract body text (without YAML frontmatter) from a markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return content.strip()


# ─── Admin Routes ──────────────────────────────────────────────

@app.route('/admin/', methods=['GET', 'POST'])
def admin():
    """Admin panel — requires login."""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        action = request.form.get('action', '')
        article_id = request.form.get('article_id', '')
        pending_cat = request.form.get('pending_cat', 'yi')

        if action == 'approve' and article_id:
            # Move from pending to appropriate category dir
            pending_path = os.path.join(PENDING_DIR, article_id + '.md')
            if os.path.exists(pending_path):
                # Determine category from the file metadata
                meta, _, _ = parse_article(pending_path)
                cat_name = meta.get('category', '')
                # Reverse lookup category key from name
                target_cat = pending_cat
                for ck, ci in CATEGORIES.items():
                    if ci['name'] == cat_name:
                        target_cat = ck
                        break
                target_dir = os.path.join(CONTENT_DIR, target_cat)
                os.makedirs(target_dir, exist_ok=True)
                target_path = os.path.join(target_dir, article_id + '.md')
                shutil.move(pending_path, target_path)
                flash(f'已批准并发布文章。', 'success')

        elif action == 'reject' and article_id:
            pending_path = os.path.join(PENDING_DIR, article_id + '.md')
            if os.path.exists(pending_path):
                os.remove(pending_path)
                flash(f'已拒绝并删除投稿。', 'info')

        elif action == 'delete' and article_id:
            # Delete a published article
            cat_key = request.form.get('cat_key', '')
            if cat_key in CATEGORIES:
                filepath = os.path.join(CONTENT_DIR, cat_key, article_id + '.md')
                if os.path.exists(filepath):
                    os.remove(filepath)
                    flash(f'已删除文章。', 'info')

        return redirect(url_for('admin'))

    pending = get_pending_articles()
    published = get_articles()
    return render_template('admin.html', pending=pending, published=published,
                           categories=CATEGORIES)


@app.route('/admin/login/', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('密码错误。', 'error')
    return render_template('admin_login.html', categories=CATEGORIES)


@app.route('/admin/logout/')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))


# ─── Letters & About ──────────────────────────────────────────

@app.route('/letters/')
def letters():
    letters_dir = os.path.join(CONTENT_DIR, 'xu')
    articles = []
    if os.path.isdir(letters_dir):
        for filename in sorted(os.listdir(letters_dir)):
            if filename.endswith('.md'):
                filepath = os.path.join(letters_dir, filename)
                meta, html, excerpt = parse_article(filepath)
                articles.append({
                    'title': meta.get('title', ''),
                    'author': meta.get('author', '匿名'),
                    'date': meta.get('date', ''),
                    'html': html,
                })
    return render_template('letters.html', articles=articles, categories=CATEGORIES)


@app.route('/about/')
def about():
    return render_template('about.html', categories=CATEGORIES)


@app.template_filter('truncate')
def truncate_filter(s, length=100):
    if len(s) <= length:
        return s
    return s[:length].rsplit(' ', 1)[0] + '…'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
