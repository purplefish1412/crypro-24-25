from typing import Callable

def gcdEuclideanExtended(a: int, m: int) -> tuple[int]:
    if a == 0:
        return m, 0, 1
    
    # gcd(a, m) = um + va.
    gcd, u, v = gcdEuclideanExtended(m % a, a)
    return gcd, v - (m // a) * u, u

def modularInverse(a: int, m: int) -> tuple[int, bool]:
    gcd, v, _ = gcdEuclideanExtended(a, m)
    if gcd != 1:
        print(f"[!] ERROR: Variables a = {a} and m = {m} are not mutually prime!")
        return gcd, True
    
    # v = a**(-1) mod m.
    return v % m, False

# ax = b mod m.
def linearCongruence(a: int, b: int, m: int) -> tuple[list[int], bool]:
    gcd, _, _ = gcdEuclideanExtended(a, m)
    if gcd == 1:
        return [(modularInverse(a, m)[0] * b) % m], False
    
    # Return error if b cannot be divided by gcd ≠ 1.
    if b / gcd != b // gcd:
        print(f"[!] ERROR: gcd(a = {a}, m = {m}) = {gcd} (≠ 1), but b = {b} cannot be divided by {gcd}!!")
        return [], True
    
    solutions = []
    a //= gcd
    b //= gcd
    m //= gcd

    root = (modularInverse(a, m)[0] * b) % m
    solutions.append(root)
    
    step = m
    for r in range(1, gcd):
        solutions.append(root + r*step)

    return solutions, False