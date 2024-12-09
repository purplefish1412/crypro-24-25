import random
import json
import prime_number as pn

json_obj = list()

def get_e(fn):
    while True:
        e = random.randint(2, fn)
        if (pn.gcd(e, fn) == 1):
            return e

def mod_invert(a, m):
    a = a % m
    if a == 0:
        return None

    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0

    return x1 + m0 if x1 < 0 else x1

class Keys:
    def __init__(self, d, p, q, n, e):
        self.d = d
        self.p = p
        self.q = q
        self.n = n
        self.e = e

# a, b діапазон довжини p, q в бітах
def GenerateKeyPair(a, b):
    min = 2 ** a
    max = 2 ** b
    p = pn.get_p(min, max)
    q = pn.get_p(min, max)
    n = p*q
    fn = (p-1)*(q-1)
    e = get_e(fn)
    d = mod_invert(e, fn) % fn
    return Keys(d=d, p=p, q=q, n=n, e=e)

if __name__ == "__main__":
    # При цьому пари чисел беруться так, щоб p * q <= p1 * q1
    alice = GenerateKeyPair(256, 384)
    bob = GenerateKeyPair(384, 512)

    json_obj.append({"name": "Alice", "my_keys": {"d": alice.d, "p": alice.p, "q": alice.q, "n": alice.n, "e": alice.e}, "open_for_me": {"n": bob.n, "e": bob.e}})
    json_obj.append({"name": "Bob", "my_keys": {"d": bob.d, "p": bob.p, "q": bob.q, "n": bob.n, "e": bob.e}, "open_for_me": {"n": alice.n, "e": alice.e}})

    with open("keys.json", "w") as f:
        json.dump(json_obj, f, ensure_ascii=False, indent=4)