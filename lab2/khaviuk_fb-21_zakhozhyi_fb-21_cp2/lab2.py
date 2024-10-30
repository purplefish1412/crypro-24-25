import matplotlib.pyplot as plt # for plots
from collections import Counter # for efficient frequency counting

FILENAME_FOR_ENCRYPTION = "./toEncrypt.txt"
FILENAME_FOR_DECRYPTION = "./toDecrypt.txt"
ALPHABET = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

def prepare_text(text):
    text = text.replace('ё', 'е').lower()
    return ''.join([char for char in text if char in ALPHABET])

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
    mono_freq_counter = Counter(text)
    ic = sum(freq * (freq - 1) for freq in mono_freq_counter.values()) / (n * (n - 1)) if n > 1 else 0
    return ic

def find_key_length(ciphertext, max_key_length=30):
    avg_ics = {}
    for key_length in range(1, max_key_length + 1):
        ics = [index_of_coincidence(ciphertext[i::key_length]) for i in range(key_length)]
        avg_ics[key_length] = sum(ics) / len(ics)
    likely_key_length = max(avg_ics, key=avg_ics.get)
    return likely_key_length, avg_ics

def plot_index_of_coincidence(avg_ics):
    plt.figure(figsize=(10, 6))
    plt.bar(list(avg_ics.keys()), list(avg_ics.values()), color='yellow')
    plt.xlabel('Довжина ключа')
    plt.ylabel('Індекс відповідності')
    plt.title('Індекси відповідності для різних довжин ключа')
    plt.grid()
    plt.show()

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
    with open(FILENAME_FOR_ENCRYPTION, 'r', encoding='utf-8') as f:
        plaintext = prepare_text(f.read())
    
    # Предефіновані ключі
    keys = ["ты", "кот", "зима", "весна", "киноактриса", "абстрагирование"]
    encrypted_texts = [(key, vigenere_encrypt(plaintext, key)) for key in keys]
    
    # Підрахунок індексів відповідності
    print("Індекси відповідності для текстів:")
    print(f"Відкритий текст: {index_of_coincidence(plaintext)}")
    for key, ciphertext in encrypted_texts:
        ic = index_of_coincidence(ciphertext)
        print(f"Ключ: {key} | Індекс відповідності: {ic}")
    
    # Розшифрування шифротексту з завдання №3
    with open(FILENAME_FOR_DECRYPTION, 'r', encoding='utf-8') as f:
        ciphertext = prepare_text(f.read())
    
    # Визначення довжини ключа та побудова графіка індексів відповідності
    likely_key_length, avg_ics = find_key_length(ciphertext)
    print(f"\nЙмовірна довжина ключа: {likely_key_length}")
    plot_index_of_coincidence(avg_ics)
    
    # Відновлення ключа та розшифрування
    probable_key = find_vigenere_key(ciphertext, likely_key_length)
    print(f"Відновлений ключ: {probable_key}")
    decrypted_text = decrypt_vigenere(ciphertext, probable_key)
    print(f"\nРозшифрований текст: {decrypted_text[:200]}...")

if __name__ == "__main__":
    main()