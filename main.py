import io
from os import getenv
from flask import Flask, request, jsonify, render_template, send_file
from deta import Deta
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

deta = Deta(getenv('MY_PROJECT_KEY'))
db = deta.Base('simpleDB')
drive = deta.Drive("images")


@app.route('/', methods=["GET"])
def hello_world():
    return "Hello, world!"


@app.route('/users', methods=["POST"])
def create_user():
    name = request.json.get("name")
    age = request.json.get("age")
    hometown = request.json.get("hometown")

    user = db.put({
        "name": name,
        "age": age,
        "hometown": hometown
    })

    return jsonify(user, 201)


@app.route('/users/<key>', methods=["PUT"])
def update_user(key):
    user = db.put(request.json, key)
    return user


@app.route('/users/<key>')
def get_user(key):
    user = db.get(key)
    return user if user else jsonify({"error": "Not found"}, 404)


@app.route('/users/<key>', methods=["DELETE"])
def delete_user(key):
    db.delete(key)
    return jsonify({"status": "ok"}, 200)


@app.route('/upload', methods=['GET'])
def upload_page():
    return render_template("upload.html")


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    res = drive.put(f.filename, f)
    return res


@app.route('/download/<name>', methods=["GET"])
def download_img(name):
    res = drive.get(name).read()
    return send_file(path_or_file=io.BytesIO(res), download_name=f'{name}', as_attachment=True)
