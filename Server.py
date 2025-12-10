from flask import Flask, render_template, send_from_directory, abort
import os

BASE_FOLDER = 'files'

app = Flask(__name__, template_folder='templates', static_folder='static')

if not os.path.exists(BASE_FOLDER):
    os.makedirs(BASE_FOLDER)

def get_all_files(path):
    entries = []
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            entries.append({'name': entry, 'type': 'dir'})
        else:
            entries.append({'name': entry, 'type': 'file'})
    return entries

# ---------- Browse folders ----------
@app.route('/', defaults={'subpath': ''})
@app.route('/<path:subpath>/')
def browse(subpath):
    dir_path = os.path.join(BASE_FOLDER, subpath)
    if not os.path.exists(dir_path):
        abort(404)

    entries = get_all_files(dir_path)
    parent_path = '/'.join(subpath.split('/')[:-1]) if subpath else None
    return render_template('directory.html',
                           entries=entries,
                           current_path=subpath,
                           parent_path=parent_path)

# ---------- Download files ----------
@app.route('/download/<path:subpath>')
def download(subpath):
    file_path = os.path.join(BASE_FOLDER, subpath)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        dir_name = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        return send_from_directory(dir_name, file_name, as_attachment=True)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(port=5000)

