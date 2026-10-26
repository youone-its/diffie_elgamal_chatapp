"""API demonstrasi Diffie–Hellman dan ElGamal untuk pesan bilangan bulat.

Jalankan: python Backend/UserAPI/API.py
Parameter kecil di bawah hanya untuk pembelajaran, bukan keamanan produksi.
"""

import sys
from pathlib import Path
from threading import Lock

from flask import Flask, jsonify, request

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from Backend.generator.encrypt import elgamal_decrypt, elgamal_encrypt
from Backend.generator.gen_primitive_root import gen_priv_int

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 100_000
P = 467
G = 2
USERS = {}
INBOX = {"alice": [], "budi": []}
LOCK = Lock()


def integer(data: dict, name: str, minimum: int, maximum: int) -> int:
    value = data.get(name)
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(f"{name} harus bilangan bulat antara {minimum} dan {maximum}")
    return value


def body() -> dict:
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValueError("Body harus objek JSON")
    return data


@app.errorhandler(ValueError)
def invalid_input(error):
    return jsonify(error=str(error)), 400


@app.route("/keys", methods=["POST"])
def keys():
    private_key = gen_priv_int(P)
    return jsonify(p=P, g=G, private_key=private_key,
                   public_key=pow(G, private_key, P))


@app.route("/exchange", methods=["POST"])
def exchange():
    data = body()
    private_key = integer(data, "private_key", 2, P - 2)
    peer_public_key = integer(data, "peer_public_key", 2, P - 1)
    return jsonify(shared_secret=pow(peer_public_key, private_key, P))


@app.route("/encrypt", methods=["POST"])
def encrypt():
    data = body()
    message = integer(data, "message", 1, P - 1)
    public_key = integer(data, "public_key", 2, P - 1)
    c1, c2 = elgamal_encrypt(message, P, G, public_key)
    return jsonify(c1=c1, c2=c2)


@app.route("/decrypt", methods=["POST"])
def decrypt():
    data = body()
    c1 = integer(data, "c1", 1, P - 1)
    c2 = integer(data, "c2", 1, P - 1)
    private_key = integer(data, "private_key", 2, P - 2)
    return jsonify(message=elgamal_decrypt(c1, c2, P, private_key))


@app.route("/register", methods=["POST"])
def register():
    data = body()
    name = data.get("name")
    if name not in INBOX:
        raise ValueError("name harus alice atau budi")
    public_key = integer(data, "public_key", 2, P - 1)
    with LOCK:
        USERS[name] = public_key
        INBOX[name].clear()
    return jsonify(ok=True)


@app.route("/public/<name>", methods=["GET"])
def public_key(name):
    with LOCK:
        key = USERS.get(name)
    if key is None:
        return jsonify(error="Pengguna belum online"), 404
    return jsonify(public_key=key)


@app.route("/messages", methods=["POST"])
def send_message():
    data = body()
    sender, recipient, ciphertext = data.get("sender"), data.get("recipient"), data.get("ciphertext")
    if sender not in INBOX or recipient not in INBOX or sender == recipient:
        raise ValueError("Pengirim atau penerima tidak valid")
    if (not isinstance(ciphertext, list) or len(ciphertext) > 4096 or
            any(not isinstance(pair, list) or len(pair) != 2 or
                any(type(value) is not int or not 1 <= value < P for value in pair)
                for pair in ciphertext)):
        raise ValueError("ciphertext tidak valid")
    with LOCK:
        if sender not in USERS or recipient not in USERS:
            raise ValueError("Pengirim atau penerima belum online")
        INBOX[recipient].append({"sender": sender, "ciphertext": ciphertext})
    return jsonify(ok=True)


@app.route("/inbox/<name>", methods=["GET"])
def inbox(name):
    if name not in INBOX:
        return jsonify(error="Pengguna tidak dikenal"), 404
    with LOCK:
        messages = INBOX[name][:]
        INBOX[name].clear()
    return jsonify(messages=messages)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
