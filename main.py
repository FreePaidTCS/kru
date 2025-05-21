from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)
DB_FILE = "database.json"

# Eğer database.json yoksa oluştur
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({}, f)

def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def home():
    return "API Çalışıyor!"

@app.route("/keys", methods=["GET"])
def get_keys():
    return jsonify(load_db())

@app.route("/add", methods=["POST"])
def add_key():
    data = request.json
    db = load_db()
    key = data["key"]
    db[key] = data["data"]
    save_db(db)
    return jsonify({"status": "success"})

@app.route("/update", methods=["POST"])
def update_key():
    data = request.json
    db = load_db()
    key = data["key"]
    if key not in db:
        return jsonify({"status": "error", "message": "Key not found"}), 404
    db[key] = data["data"]
    save_db(db)
    return jsonify({"status": "success"})

# Yeni: Key silme endpoint'i
@app.route("/delete", methods=["POST"])
def delete_key():
    data = request.json
    db = load_db()
    key = data["key"]
    if key not in db:
        return jsonify({"status": "error", "message": "Key not found"}), 404
    del db[key]
    save_db(db)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
