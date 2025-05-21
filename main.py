from flask import Flask, jsonify, request
import json
import os
import time

app = Flask(__name__)
DB_FILE = "database.json"

# database.json yoksa oluşturuyoruz
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({}, f)

def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

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

# Reset HWID: Sadece ilgili key için, 10 günde bir reset yapılabilir.
@app.route("/reset_hwid", methods=["POST"])
def reset_hwid():
    data = request.json
    db = load_db()
    key = data["key"]
    new_hwid = data["new_hwid"]
    now = int(time.time())
    if key not in db:
        return jsonify({"status": "error", "message": "Key not found"}), 404
    last_reset = db[key].get("last_reset", 0)
    if now - last_reset < 864000:  # 864000 saniye = 10 gün
        remaining = 864000 - (now - last_reset)
        return jsonify({"status": "error", "message": f"HWID reset için {remaining} saniye beklemelisin."}), 403
    db[key]["hwid"] = new_hwid
    db[key]["last_reset"] = now
    save_db(db)
    return jsonify({"status": "success", "message": "HWID reset başarılı!"})

# Delete key endpoint
@app.route("/delete", methods=["POST"])
def delete_key():
    data = request.json
    db = load_db()
    key = data["key"]
    if key not in db:
        return jsonify({"status": "error", "message": "Key not found"}), 404
    del db[key]
    save_db(db)
    return jsonify({"status": "success", "message": "Key deleted successfully!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
