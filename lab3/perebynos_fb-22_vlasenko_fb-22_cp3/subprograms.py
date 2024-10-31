from typing import Callable

def gcdEuclideanExtended(a: int, m: int) -> tuple[int, int, int]:
    if a == 0:
        return m, 0, 1
    
    # gcd(a, m) = um + va
    gcd, u, v = gcdEuclideanExtended(m % a, a)
    return gcd, v - (m // a) * u, u

def modularInverse(a: int, m: int) -> tuple[int, bool]:
    gcd, v, _ = gcdEuclideanExtended(a, m)
    if gcd != 1:
        print(f"[!] ERROR: Variables a = {a} and m = {m} are not mutually prime!")
        return gcd, True
    
    # v = a**(-1) mod m
    return v % m, False

### TODO: Linear congruences.