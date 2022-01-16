import base64
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World!"


@app.route("/unity", methods=["POST"])
def unity():
    if request.method == "POST":
        form = request.form
        # FileStorage object wrapper
        file = request.files["fileUpload"]
        if file:
            image_string = base64.b64encode(file.read())
            print(image_string.decode('utf-8'))

        print(form["name"])
        return "Accepted"
    else:
        return "None"


if __name__ == "__main__":
    app.run(debug=True)
