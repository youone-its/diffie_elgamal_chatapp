"""Klien TUI Alice/Budi. Pesan dienkripsi lokal; server hanya meneruskan ciphertext."""

import json
import readline
import sys
import threading
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from Backend.generator.encrypt import elgamal_decrypt, elgamal_encrypt
from Backend.generator.gen_primitive_root import gen_priv_int

SERVER = "http://127.0.0.1:8000"
P, G = 467, 2


def api(path, data=None):
    payload = None if data is None else json.dumps(data).encode()
    request = Request(SERVER + path, payload, {"Content-Type": "application/json"})
    try:
        with urlopen(request, timeout=3) as response:
            return json.load(response)
    except HTTPError as error:
        message = json.load(error).get("error", str(error))
        raise ValueError(message) from error


def encrypt_text(message, public_key):
    raw = message.encode("utf-8")
    if len(raw) > 4096:
        raise ValueError("Pesan maksimal 4096 byte")
    return [list(elgamal_encrypt(byte + 1, P, G, public_key)) for byte in raw]


def decrypt_text(ciphertext, private_key):
    raw = bytes(elgamal_decrypt(c1, c2, P, private_key) - 1 for c1, c2 in ciphertext)
    return raw.decode("utf-8")


def run(name):
    peer = "budi" if name == "alice" else "alice"
    private_key = gen_priv_int(P)
    public_key = pow(G, private_key, P)
    try:
        api("/register", {"name": name, "public_key": public_key})
    except URLError:
        print("Server belum jalan. Jalankan backend lebih dulu.")
        return

    def receive():
        while True:
            try:
                for item in api("/inbox/" + name)["messages"]:
                    sender = item["sender"].title()
                    ciphertext = item["ciphertext"]
                    message = decrypt_text(ciphertext, private_key)
                    if sys.stdout.isatty():
                        print("\r\033[2K", end="")
                    print(f"{sender} [cipher]: {json.dumps(ciphertext)}")
                    print(f"{sender} [message]: {message}")
                    if sys.stdout.isatty():
                        print(f"{name.title()}: {readline.get_line_buffer()}", end="", flush=True)
            except (URLError, ValueError, UnicodeError) as error:
                print(f"\nGagal menerima pesan: {error}")
            time.sleep(1)

    threading.Thread(target=receive, daemon=True).start()
    print(f"{name.title()} siap. Ketik pesan untuk {peer.title()}, /quit untuk keluar.")
    try:
        while True:
            message = input(f"{name.title()}: ")
            if message == "/quit":
                break
            if not message:
                continue
            try:
                public_key = api("/public/" + peer)["public_key"]
                ciphertext = encrypt_text(message, public_key)
                api("/messages", {"sender": name, "recipient": peer, "ciphertext": ciphertext})
            except (URLError, ValueError) as error:
                print(f"Gagal mengirim: {error}")
    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == "__main__":
    run(sys.argv[1].lower())
