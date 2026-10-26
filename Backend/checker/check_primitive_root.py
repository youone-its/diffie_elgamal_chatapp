def _prime_factors(n: int) -> set[int]:
    # Mengembalikan himpunan faktor prima dari n.
    factors = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.add(d)
            n //= d
        d += 1
    if n > 1:
        factors.add(n)
    return factors


def is_primitive_root(g: int, p: int) -> bool:
    """
    Cek apakah g adalah akar primitif dari bilangan prima p.

    Cara kerja: g adalah akar primitif jika untuk setiap faktor prima q
    dari (p-1), berlaku g^((p-1)/q) mod p != 1.
    """
    if p < 2 or not _prime_factors(p) == {p}:
        raise ValueError("p harus bilangan prima")

    g %= p
    if g == 0:
        return False
    if p == 2:
        return g == 1

    return all(pow(g, (p - 1) // q, p) != 1 for q in _prime_factors(p - 1))