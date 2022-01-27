import base64
import os
import uuid
import io

from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
from os.path import basename
from flask import Flask, request, render_template, send_from_directory

from zipfile import ZipFile

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads/"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/unity", methods=["POST"])
def unity():
    if request.method == "POST":
        form = request.form
        # FileStorage object wrapper
        print(request.files)
        file = request.files['dataFile']
        if file:
            # text_content = file.read()
            filename = secure_filename(file.filename)
            file.save(app.config['UPLOAD_FOLDER'] + filename)
            return "File Accepted " + filename
        else:
            print(form["name"])
            return "Accepted"
    else:
        return "None"


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


if __name__ == "__main__":
    app.run(debug=False)
