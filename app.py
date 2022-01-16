from flask import Flask, request, redirect

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World!"


@app.route("/unity", methods=["POST", "GET"])
def unity():
    if request.method == "POST":
        user = request.form
    else:
        return "No request"


if __name__ == "__main__":
    app.run(debug=True)