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

p = pn.get_p(2 ** 256, 2 ** 512)
q = pn.get_p(2 ** 256, 2 ** 512)    
p1 = pn.get_p(2 ** 512, 2 ** 1024)
q1 = pn.get_p(2 ** 512, 2 ** 1024)

n = p*q
n1 = p1*q1

fn = (p-1)*(q-1)
fn1 = (p1-1)*(q1-1)

e = get_e(fn)
e1 = get_e(fn1)

d = mod_invert(e, fn) % fn
d1 = mod_invert(e1, fn1) % fn1

print("Alice")
print("Open key n&e:", n, e)
print("Privat key d:", d)
print("Bob")
print("Open key n&e:", n1, e1)
print("Privat key d:", d1)

json_obj.append({"name": "Alice", "my_keys": {"d": d, "p": p, "q": q, "n": n, "e": e}, "bob_open_key": {"n": n1, "e": e1}})
json_obj.append({"name": "Bob", "my_keys": {"d": d1, "p": p1, "q": q1, "n": n1, "e": e1}, "alice_open_key": {"n": n, "e": e}})

with open("keys.json", "w") as f:
    json.dump(json_obj, f, ensure_ascii=False, indent=4)