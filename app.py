import glob
import os
from os.path import basename
from zipfile import ZipFile

from flask import Flask, render_template, send_from_directory, flash, request, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import time

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads/"
ALLOWED_EXTENSIONS = {'txt', 'json'}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
cors = CORS(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/mazerun', methods=['GET', 'POST'])
def mazerun():
    return render_template('mazerun.html')


@app.route("/delete")
def delete():
    files = glob.glob('/static/**/*.txt', recursive=True)

    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))


@app.route("/unity", methods=["POST"])
def unity():
    if request.method == "POST":

        auth = GoogleAuth()
        drive = GoogleDrive(auth)
        client_json_path = 'static/client_secrets.json'
        GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = client_json_path

        form = request.form
        # FileStorage object wrapper
        print(form)
        filename = form.get('fileName') + ".txt"
        print(form.get('fileData'))

        with open(app.config['UPLOAD_FOLDER'] + filename, 'w') as f:
            f.write(str(form.get('fileData')))
            f.close()

        fileToDrive = app.config['UPLOAD_FOLDER'] + filename
        print(fileToDrive)
        file = drive.CreateFile({'parents': [{'id': "1oNuqmcxNPctnHNC_BjgJnoXM8p2Ykuqz"}]})
        # Read file and set it as the content of this instance.
        file.SetContentFile(fileToDrive)
        file.Upload()  # Upload the file.

        return "Access-Control-Allow-Origin: *"

    else:
        print("no req")
        with open(app.config['UPLOAD_FOLDER'] + 'log2', 'w') as f:
            f.write("ping")
            f.close()
        return "Access-Control-Allow-Origin: *"


@app.route('/logs/')
def logs():
    return render_template('logs.html', tree=make_tree("static/uploads/"))


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    print(app.root_path)
    full_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    print(full_path)
    return send_from_directory(full_path, filename)


def make_tree(path):
    tree = dict(name=os.path.basename(path), children=[])
    try:
        lst = os.listdir(path)
    except OSError:
        pass  # ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                with open(fn) as f:
                    contents = f.read()
                tree['children'].append(dict(name=name, contents=contents))
    return tree


# create a ZipFile object
@app.route('/downloadzip/<path:filename>', methods=['GET', 'POST'])
def downloadzip(path):
    with ZipFile('sampleDir.zip', 'w') as zipObj:
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk(path):
            for filename in filenames:
                # create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                # Add file to zip
                zipObj.write(filePath, basename(filePath))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part or form
        if 'file' not in request.files and not request.form:
            flash('No file part')
            return redirect(request.url)

        if 'data' in request.form:
            now = time.strftime("%Y%m%d_%H%M%S")
            filename = request.form.get('fileName') + now + ".txt"
            with open(app.config['UPLOAD_FOLDER'] + filename, 'w') as f:
                f.write(str(request.form.get('data')))
                f.close()
            return '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>File Uploaded Successfully</h1>
            '''

        if 'file' in request.files:
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join('static/', filename))
                return '''
                <!doctype html>
                <title>Upload new File</title>
                <h1>File Uploaded Successfully</h1>
                '''
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
