from flask import Flask, render_template, send_from_directory, abort, request, url_for
import os
import mimetypes
from datetime import datetime

BASE_FOLDER = 'files'

app = Flask(__name__, template_folder='templates', static_folder='static')
os.makedirs(BASE_FOLDER, exist_ok=True)

def get_all_files(path):
    entries = []
    for entry in sorted(os.listdir(path), key=str.lower):
        full_path = os.path.join(path, entry)
        is_dir = os.path.isdir(full_path)

        stat = os.stat(full_path)
        size = stat.st_size
        modified = datetime.fromtimestamp(stat.st_mtime)

        entries.append({
            'name': entry,
            'type': 'dir' if is_dir else 'file',
            'size': size,
            'modified': modified.strftime("%Y-%m-%d %H:%M"),
            'mime': mimetypes.guess_type(full_path)[0] if not is_dir else None
        })
    return entries


def build_breadcrumbs(subpath):
    if not subpath:
        return []
    parts = subpath.split('/')
    crumbs = []
    for i in range(len(parts)):
        crumbs.append({
            'name': parts[i],
            'path': '/'.join(parts[:i+1])
        })
    return crumbs


def search_files(query):
    results = []
    query = query.lower()

    for root, dirs, files in os.walk(BASE_FOLDER):
        rel_root = os.path.relpath(root, BASE_FOLDER)
        rel_root = "" if rel_root == "." else rel_root

        folder_name = os.path.basename(root)
        if query in folder_name.lower() and rel_root != "":
            results.append({
                'name': folder_name,
                'path': rel_root,
                'type': 'dir'
            })

        for f in files:
            if query in f.lower():
                file_path = os.path.join(rel_root, f)
                results.append({
                    'name': f,
                    'path': file_path,
                    'type': 'file'
                })

    return results


@app.route('/', defaults={'subpath': ''})
@app.route('/<path:subpath>/')
def browse(subpath):
    dir_path = os.path.join(BASE_FOLDER, subpath)

    if not os.path.exists(dir_path):
        abort(404)

    entries = get_all_files(dir_path)

    if not subpath:
        parent_path = None
    elif '/' in subpath:
        parent_path = subpath.rsplit('/', 1)[0]
    else:
        parent_path = ''

    breadcrumbs = build_breadcrumbs(subpath)

    return render_template(
        'directory.html',
        entries=entries,
        current_path=subpath,
        parent_path=parent_path,
        breadcrumbs=breadcrumbs
    )


@app.route('/download/<path:subpath>')
def download(subpath):
    file_path = os.path.join(BASE_FOLDER, subpath)

    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_from_directory(
            os.path.dirname(file_path),
            os.path.basename(file_path),
            as_attachment=True
        )

    abort(404)


@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return render_template('search.html', query="", results=[], parent_path="")

    results = search_files(query)

    return render_template(
        'search.html',
        query=query,
        results=results,
        parent_path=""
    )



if __name__ == '__main__':
    app.run(port=5000)
