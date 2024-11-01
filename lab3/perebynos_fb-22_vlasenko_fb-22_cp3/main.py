#!/bin/python
from typing import Callable
import subprograms as sp

TESTDATA = "./data/V2"
VARDATA = "./data/02.txt"
EXITMSG = "No integer solutions exist. Exiting..."

def main():
    """
    ### Driver code.
    # inverse test.
    a = 341
    m = 960
    gcd, u, v = sp.gcdEuclideanExtended(a, m)
    print(f"gcd({a}, {m}) = {gcd}, u = {u}, v = {v}")

    inverse, err = sp.modularInverse(a, m)
    if err:
        print(EXITMSG)
        return
    
    print(f"{a}^(-1) mod {m} = {inverse}")
    
    # linear congruence test.
    a = 17
    b = 3
    m = 23
    solutions, err = sp.linearCongruence(a, b, m)
    if err:
        print(EXITMSG)
        return

    solve = ""
    for i in solutions:
        solve += str(i) + " "
    print(f"{a}x = {b} mod {m}, x = {solve}")
    """

    ### TODO: handle & parse text (check for forbidden chars).

    # bigram (overlapped) count test.
    test_data = "ялошара"
    bCounts, total = sp.countBigrams(test_data)
    for k, v in bCounts.items():
        if v != 0:
            print(f'"{k}": {v}, ')
    print(total)
    ###

    return

if __name__ == "__main__":
    main()