import base64
import os
import uuid
import io

from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt

from flask import Flask, request

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads/"


@app.route("/")
def index():
    return "Hello World!"


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


if __name__ == "__main__":
    app.run(debug=True)
