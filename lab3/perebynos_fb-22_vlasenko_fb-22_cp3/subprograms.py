from decimal import Decimal, getcontext
getcontext().prec = 50

import itertools

ALPHABET = "абвгдежзийклмнопрстуфхцчшщьыэюя"

def readText(fileName: str):
    with open(fileName, "r", encoding="utf-8") as f:
        return f.read()

def gcdEuclideanExtended(a: int, m: int) -> tuple[int]:
    """
    Вираховує НСД(a, m) та повертає відповідні коефіцієнти u, v.
    gcd(a, m) = um + va.
    """
    if a == 0:
        return m, 0, 1
    
    # gcd(a, m) = um + va.
    gcd, u, v = gcdEuclideanExtended(m % a, a)
    return gcd, v - (m // a) * u, u

def modularInverse(a: int, m: int) -> tuple[int, bool]:
    """
    Повертає обернене a за модулем m. a**(-1) mod m.
    """
    gcd, v, _ = gcdEuclideanExtended(a, m)
    if gcd != 1:
        print(f"[!] ERROR: Variables a = {a} and m = {m} are not mutually prime!")
        return gcd, True
    
    # v = a**(-1) mod m.
    return v % m, False

def linearCongruence(a: int, b: int, m: int) -> tuple[list[int], bool]:
    """
    Повертає списком усі розв'язки лінійного порівняння ax = b mod m.
    """
    gcd, _, _ = gcdEuclideanExtended(a, m)
    if gcd == 1:
        return [(modularInverse(a, m)[0] * b) % m], False
    
    # Return error if b cannot be divided by gcd ≠ 1.
    if b / gcd != b // gcd:
        print(f"[!] ERROR: gcd(a = {a}, m = {m}) = {gcd} (≠ 1), but b = {b} cannot be divided by {gcd}!!")
        return [], True
    
    solutions: list[int] = []
    a //= gcd
    b //= gcd
    m //= gcd

    root = (modularInverse(a, m)[0] * b) % m
    solutions.append(root)
    
    for r in range(1, gcd):
        solutions.append(root + r*m)

    return solutions, False

def countBigrams(data: str) -> tuple[dict[str, int], int]:
    """
    Вираховує загальну кількість біграм, що перетинаються,
    та кількість кожної з біграм.
    """
    totalBigramCount: int = 0
    bigramCounts: dict[str, int] = {c1 + c2: 0 for c1 in ALPHABET for c2 in ALPHABET}
    prevChar: str | None = None

    for c in data:
        if prevChar is not None and prevChar in ALPHABET and c in ALPHABET:
            bigramCounts[prevChar + c] += 1
            totalBigramCount += 1
        prevChar = c

    return bigramCounts, totalBigramCount

def calculateFrequencies(data: str) -> dict[str, Decimal]:
    """
    Вираховує частоту кожної біграми у тексті. Повертає найчастіші 5.
    """
    bigramCounts, totalBigramCount = countBigrams(data)
    return dict(itertools.islice(dict(sorted({bigram: Decimal(count) / Decimal(totalBigramCount) for bigram, count in bigramCounts.items()}.items(), key=lambda item: item[1], reverse=True)).items(), 5))