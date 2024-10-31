#!/bin/python
from typing import Callable
import subprograms as sp

def main():
    ### Driver code
    a = 341
    m = 960
    gcd, u, v = sp.gcdEuclideanExtended(a, m)
    print(f"gcd({a}, {m})={gcd}, u={u}, v={v}")

    inverse, err = sp.modularInverse(a, m)
    if not err:
        print(f"{a}^(-1) mod {m} = {inverse}")
    return

if __name__ == "__main__":
    main()