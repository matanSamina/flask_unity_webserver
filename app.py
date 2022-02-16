import glob
import os, boto3
from os.path import basename
from zipfile import ZipFile

from flask import Flask, render_template, send_from_directory, flash, request, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename

import time

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads/"
ALLOWED_EXTENSIONS = {'txt', 'json'}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
cors = CORS(app)


@app.route("/")
def index():
    return render_template("index.html", page_name="Unity API")


@app.route('/mazerun', methods=['GET', 'POST'])
def mazerun():
    return render_template('mazerun.html', page_name="mazerun")


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

        return "Access-Control-Allow-Origin: *"

    else:
        print("no req")
        with open(app.config['UPLOAD_FOLDER'] + 'log2', 'w') as f:
            f.write("ping")
            f.close()
        return "Access-Control-Allow-Origin: *"


@app.route('/logs/')
def logs():
    return render_template('logs.html', tree=make_tree("static/uploads/"), page_name="LOGS")


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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def s3_upload_files(f, bucket_name, filename):

    S3_BUCKET = os.environ.get('S3_BUCKET')
    s3 = boto3.client('s3')
    # Creating S3 Resource From the Session.
    # s3 = session.resource('s3')

    result = s3.meta.client.put_object(Body=f, Bucket=S3_BUCKET, Key=filename)

    res = result.get('ResponseMetadata')

    if res.get('HTTPStatusCode') == 200:
        print('File Uploaded Successfully')
    else:
        print('File Not Uploaded')


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
                s3_upload_files(str(request.form.get('data')), "unityflaskwebapp", filename)

            # drive_upload(filename)
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


def s3_upload_small_files(inp_file_name, s3_bucket_name, inp_file_key, content_type):
    client = s3_client()
    upload_file_response = client.put_object(Body=inp_file_name,
                                             Bucket=s3_bucket_name,
                                             Key=inp_file_key,
                                             ContentType=content_type)
    print(f" ** Response - {upload_file_response}")


if __name__ == "__main__":
    # app.config['SESSION_TYPE'] = 'filesystem'
    # app.run(debug=True)

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
