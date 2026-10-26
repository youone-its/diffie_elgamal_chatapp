import secrets


def elgamal_encrypt(m: int, p: int, g: int, y: int) -> tuple[int, int]:
    """
    m : pesan
    p : bilangan prima
    g : generator (akar primitif dari p)
    y : kunci publik penerima, y = g^x mod p
    Mengembalikan ciphertext (c1, c2).
    """
    if not 1 <= m < p:
        raise ValueError("m harus memenuhi 1 <= m < p")

    k = secrets.randbelow(p - 3) + 2
    c1 = pow(g, k, p)
    c2 = (m * pow(y, k, p)) % p
    return c1, c2

def elgamal_decrypt(c1: int, c2: int, p: int, x: int) -> int:
    """
    c1, c2 : ciphertext
    p      : bilangan prima
    x      : kunci privat penerima
    Mengembalikan pesan asli m.
    """
    s = pow(c1, x, p)
    return (c2 * pow(s, -1, p)) % p