#!/bin/python
from typing import Callable
import subprograms as sp

TESTDATA = "./data/V2"
VARDATA = "./data/02.txt"
EXITMSG = "No integer solutions exist. Skipping...\n"
MOSTFREQBIGRAMS = ["ст", "но", "то", "на", "ен"]
MODULUS = len(sp.ALPHABET)

def main():
    test_data = sp.readText(TESTDATA)

    freqs = sp.calculateFrequencies(test_data)
    givenBigrams: list[str] = list(freqs.keys())

    aSolutions: list[int] = []
    abSolutions: dict[int, int] = {}
    # WARNING TODO: iterates through all bigram combos, including duplicate pairs.
    # Not sure how to fix. I mean, it doesn't affect the overall functionality, but
    # it's definitely an issue to the performance (govnocod).
    for i in range(len(givenBigrams)):
        for j in range(len(givenBigrams)):
            if i != j:
                actualBigram1 = givenBigrams[i]
                expectedBigram1 = MOSTFREQBIGRAMS[i]

                actualBigram2 = givenBigrams[j]
                expectedBigram2 = MOSTFREQBIGRAMS[j]

                # X = ord(char1) * m + ord(char2)
                X1 = sp.ALPHABET.index(actualBigram1[0]) * MODULUS + sp.ALPHABET.index(actualBigram1[1])
                Y1 = sp.ALPHABET.index(expectedBigram1[0]) * MODULUS + sp.ALPHABET.index(expectedBigram1[1])

                X2 = sp.ALPHABET.index(actualBigram2[0]) * MODULUS + sp.ALPHABET.index(actualBigram2[1])
                Y2 = sp.ALPHABET.index(expectedBigram2[0]) * MODULUS + sp.ALPHABET.index(expectedBigram2[1])

                aVariations, err = sp.linearCongruence((X1 - X2) % MODULUS ** 2, (Y1 - Y2) % MODULUS ** 2, MODULUS ** 2)
                if err:
                    print(f"Bigram1: {expectedBigram1} -> {actualBigram1}\nBigram2: {expectedBigram2} -> {actualBigram2}")
                    print(EXITMSG)
                    continue

                for a in aVariations:
                    if a not in aSolutions:
                        aSolutions.append(a)

                    abSolutions[a] = (Y1 - a * X1) % MODULUS**2
                
                print(f"Bigram1: {expectedBigram1} -> {actualBigram1}\nBigram2: {expectedBigram2} -> {actualBigram2}\nSolutions: {aVariations}\n")

    print(aSolutions, abSolutions)
    return

if __name__ == "__main__":
    main()