import json
from math import log2
import sys

alph_ = "абвгдежзийклмнопрстуфхцчшщьыэюя"
bigrams_ = ['аы', 'бй', 'гй', 'дй', 'еы', 'жй', 'жщ', 'зщ', 'иы', 'йй', 'йэ', 'кщ', 'оь', 'пй', 'сй', 'уь', 'уы', 'фж', 'фй', 'фх', 'хй', 'хю', 'цж', 'цй', 'цщ', 'чг', 'чз', 'чй', 'чщ', 'чю', 'шж', 'шз', 'шй', 'шщ', 'шя', 'щб', 'щд', 'щж', 'щз', 'щй', 'щс', 'щф', 'щх', 'щц', 'щщ', 'щы', 'щэ', 'щю', 'щя', 'ьы', 'ыа', 'ыь', 'ыы', 'ыэ', 'эщ', 'эь', 'эы', 'юу', 'юь', 'юы', 'яы', 'яэ']

def freq_symbols(text):
    letters = dict()

    for item in text:
        if item not in letters.keys():
            letters[item] = 1
        else:
            letters[item] += 1

    for key, val in letters.items():
        letters[key] = val / len(text)
    return letters

def bigrams(text, gap, cross):
    bigrams = dict()

    alph = alph_ + ' ' if gap else alph_

    for i in alph:
        for j in alph:
            bigrams[i + j] = 0

    for i in range(0, len(text) - 1, 1 if cross else 2):
        item = text[i] + text[i + 1]
        if item in bigrams.keys():
            bigrams[item] += 1

    new_b = dict()
    for key, val in bigrams.items():
        if val != 0:
            new_b[key] = val

    return new_b

def entropy(bigrams, n = 1):
    return -sum(p * log2(p) for p in bigrams.values() if p > 0) / n

def redundancy(h, alphabet):
    return 1 - (h / log2(len(alphabet)))

with open("text.json", "r") as f:
    root = json.load(f)

if len(sys.argv) == 1:
    print("Set method")
    exit()

if sys.argv[1] == "-e":
    entr = dict()
    for obj in root:
        letters = freq_symbols(obj["text"])
        en = entropy(letters)
        re = redundancy(en, alph_)
        entr[(obj["a"], obj["b"])] = re
    
    entr = dict(sorted(entr.items(), key=lambda item: item[1]))

    for k, v in entr.items():
        print(f"{k[0] :<5} {k[1] :<5} {v}")


    max_key = max(entr, key=entr.get)
    
    for o in root:
        if o["a"] == max_key[0] and o["b"] == max_key[1]:
            print(o["text"])

elif sys.argv[1] == "-b":
    x_bigr = dict()

    for obj in root:
        tb = bigrams(obj["text"], False, True)
        sum = 0
        for b in bigrams_:
            if b in tb.keys():
                sum += tb[b]
        x_bigr[(obj["a"], obj["b"])] = sum

    x_bigr_s = dict(sorted(x_bigr.items(), key=lambda item: item[1], reverse=True))
    
    for k, v in x_bigr_s.items():
        print(f"{k[0] :<5} {k[1] :<5} {v}")

    max_key = min(x_bigr, key=x_bigr.get)

    for obj in root:
        if obj["a"] == max_key[0] and obj["b"] == max_key[1]:
            print(obj["text"])
else:
    print("unknown method")
