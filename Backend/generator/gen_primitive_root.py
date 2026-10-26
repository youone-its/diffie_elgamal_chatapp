from Backend.checker.check_primitive_root import is_primitive_root
import secrets


def generate_primitive_roots(p: int) -> list[int]:
    # Menghasilkan semua akar primitif dari bilangan prima p.
    #Contoh: generate_primitive_roots(7) -> [3, 5]
    return [g for g in range(1, p) if is_primitive_root(g, p)]

def gen_priv_int(p: int) -> int:
    # buat bikin int secret
    return secrets.randbelow(p - 3) + 2

def generate_discrete_logarithm(g:int, x:int, n:int) -> int:
    return pow(g,x)%n
