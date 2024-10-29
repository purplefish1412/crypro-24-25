import random
from collections import Counter

FILENAME = "./seneka_short.txt"
ALPHABET = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

def prepare_text(text):
    text = text.replace('ё', 'е').lower()
    prepared_text = ''.join([char for char in text if char in ALPHABET])
    # print(prepared_text)
    return prepared_text

def generate_key(length):
    return ''.join(random.choice(ALPHABET) for _ in range(length))

def vigenere_encrypt(plaintext, key):
    ciphertext = []
    for i, char in enumerate(plaintext):
        p = ALPHABET.index(char)
        k = ALPHABET.index(key[i % len(key)])
        c = (p + k) % len(ALPHABET)
        ciphertext.append(ALPHABET[c])
    return ''.join(ciphertext)

def index_of_coincidence(text):
    n = len(text)
    freqs = Counter(text)
    ic = sum(f * (f - 1) for f in freqs.values()) / (n * (n - 1)) if n > 1 else 0
    return ic

def find_key_length(ciphertext, max_key_length=20):
    avg_ics = {}
    for key_length in range(1, max_key_length + 1):
        ics = []
        for i in range(key_length):
            nth_subtext = ciphertext[i::key_length]
            ics.append(index_of_coincidence(nth_subtext))
        avg_ics[key_length] = sum(ics) / len(ics)
    likely_key_length = max(avg_ics, key=avg_ics.get)
    return likely_key_length

def frequency_analysis(text):
    return Counter(text).most_common()

def decrypt_vigenere(ciphertext, key):
    plaintext = []
    for i, char in enumerate(ciphertext):
        c = ALPHABET.index(char)
        k = ALPHABET.index(key[i % len(key)])
        p = (c - k) % len(ALPHABET)
        plaintext.append(ALPHABET[p])
    return ''.join(plaintext)

def find_vigenere_key(ciphertext, key_length):
    key = []
    for i in range(key_length):
        nth_subtext = ciphertext[i::key_length]
        freq_analysis = frequency_analysis(nth_subtext)
        most_common_letter = freq_analysis[0][0]
        likely_key_letter = ALPHABET[(ALPHABET.index(most_common_letter) - ALPHABET.index('о')) % len(ALPHABET)]
        key.append(likely_key_letter)
    return ''.join(key)

def main():
    # Завантаження та підготовка тексту
    with open(FILENAME, 'r', encoding='utf-8') as f:
        plaintext = prepare_text(f.read())
    
    # Зашифрування тексту з різними ключами
    keys = [generate_key(r) for r in [2, 3, 4, 5] + [random.randint(10, 20) for _ in range(1)]]
    encrypted_texts = [(key, vigenere_encrypt(plaintext, key)) for key in keys]
    
    # Підрахунок індексів відповідності
    print("Індекси відповідності для текстів:")
    print(f"Відкритий текст: {index_of_coincidence(plaintext)}")
    
    for key, ciphertext in encrypted_texts:
        ic = index_of_coincidence(ciphertext)
        print(f"Ключ: {key} | Індекс відповідності: {ic}")
    
    # Розшифрування шифротексту з завдання №3
    with open("./alpha.txt", 'r', encoding='utf-8') as f:
        ciphertext = prepare_text(f.read())
    
    # Крок 1: Визначення довжини ключа
    likely_key_length = find_key_length(ciphertext)
    print(f"\nЙмовірна довжина ключа: {likely_key_length}")
    
    # Крок 2: Відновлення ключа за частотним аналізом
    probable_key = find_vigenere_key(ciphertext, likely_key_length)
    print(f"Відновлений ключ: {probable_key}")
    
    # Крок 3: Розшифрування шифротексту за допомогою знайденого ключа
    decrypted_text = decrypt_vigenere(ciphertext, probable_key)
    print(f"\nРозшифрований текст: {decrypted_text}...")

if __name__ == "__main__":
    main()