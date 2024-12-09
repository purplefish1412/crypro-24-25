import json
import prime_number as pn

class Import_key():
    def __init__(self, name):
        with open("keys.json", "r") as f:
            root = json.load(f)
        status = False
        for obj in root:
            if obj["name"] == name:
                self.d = obj["my_keys"]["d"]
                self.p = obj["my_keys"]["p"]
                self.q = obj["my_keys"]["q"]
                self.n = obj["my_keys"]["n"]
                self.e = obj["my_keys"]["e"]
                self.o_n = obj["open_for_me"]["n"]
                self.o_e = obj["open_for_me"]["e"]
                status = True
                break
        if not status:
            raise KeyError("Not found keys for " + name)

def Encrypt(M, e, n):
    return pn._pow(M, e, n)

def Decrypt(C, d, n):
    return pn._pow(C, d, n)
 
def Sign(M, d, n):
    return pn._pow(M, d, n) # S

def Verify(S, M, e, n):
    return pn._pow(S, e, n) == M

def txt2int(text):
    return int(''.join(f"{ord(c):08b}" for c in text), 2)

def int2txt(number):
    number = bin(number)[2:]

    zero = len(number) % 8
    if zero != 0:
        number = "0" * (8 - zero) + number

    text = ""
    for i in range(0, len(number), 8):
        text += chr(int(number[i:i+8], 2))
    return text

if __name__ == "__main__":
    alice = Import_key("Alice")
    bob = Import_key("Bob")
    mess_number = txt2int("Hello Bob")
    # C_alice2bob = Encrypt(mess_number, alice.o_e, alice.o_n)
    # M_alice2bob = Decrypt(C_alice2bob, bob.d, bob.n)

    # print(int2txt(M_alice2bob))

    S_from_alice = Sign(mess_number, alice.d, alice.n)
    print(hex(S_from_alice))
    print(hex(alice.n))
    print(hex(alice.e))
    Bob_verify = Verify(S_from_alice, mess_number, bob.o_e, bob.o_n)

    if Bob_verify:
        print("Yes, it work")
    else:
        print("Ohh noooo :>")