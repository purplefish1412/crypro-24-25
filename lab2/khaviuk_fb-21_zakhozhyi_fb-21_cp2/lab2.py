from collections import Counter
import matplotlib.pyplot as plt

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
    freq_counter = Counter(text)
    
    if n > 1:
        ic_numerator = sum(freq * (freq - 1) for freq in freq_counter.values())
        ic_denominator = n * (n - 1)
        ic = ic_numerator / ic_denominator
    else:
        ic = 0
    
    return ic

def find_key_length(ciphertext, max_key_length=30):
    avg_ics = {}
    for key_length in range(1, max_key_length + 1):
        ics = []
        for i in range(key_length):
            nth_subtext = ciphertext[i::key_length]
            ics.append(index_of_coincidence(nth_subtext))
        
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
    freq_counter = Counter(text)
    freq_analysis = freq_counter.most_common()
    return freq_analysis

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
        
        likely_key_letter_index = (
            ALPHABET.index(most_common_letter) - ALPHABET.index('о')
        ) % len(ALPHABET)
        
        likely_key_letter = ALPHABET[likely_key_letter_index]
        key.append(likely_key_letter)
    
    return ''.join(key)

def main():
    with open(FILENAME_FOR_ENCRYPTION, 'r', encoding='utf-8') as f:
        plaintext = prepare_text(f.read())
    
    keys = ["ты", "кот", "зима", "весна", "киноактриса", "абстрагирование"]
    encrypted_texts = [(key, vigenere_encrypt(plaintext, key)) for key in keys]
    
    # підрахунок індексів відповідності
    print("Індекси відповідності для текстів:")
    print(f"Відкритий текст: {index_of_coincidence(plaintext)}")
    for key, ciphertext in encrypted_texts:
        ic = index_of_coincidence(ciphertext)
        print(f"Ключ: {key} | Індекс відповідності: {ic}")
    
    # розшифрування шифротексту з завдання №3
    with open(FILENAME_FOR_DECRYPTION, 'r', encoding='utf-8') as f:
        ciphertext = prepare_text(f.read())
    
    # визначення довжини ключа та побудова графіка індексів відповідності
    likely_key_length, avg_ics = find_key_length(ciphertext)
    print(f"\nЙмовірна довжина ключа: {likely_key_length}")
    plot_index_of_coincidence(avg_ics)
    
    # відновлення ключа та розшифрування
    probable_key = find_vigenere_key(ciphertext, likely_key_length)
    print(f"Відновлений ключ: {probable_key}")
    decrypted_text = decrypt_vigenere(ciphertext, probable_key)
    print(f"\nРозшифрований текст: {decrypted_text[:200]}...")

if __name__ == "__main__":
    main()