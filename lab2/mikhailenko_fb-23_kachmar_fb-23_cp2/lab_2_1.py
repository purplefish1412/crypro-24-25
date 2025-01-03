import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

from collections import Counter

def read_input_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def vigenere_cipher_encrypt(content, cipher_key):
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщьыэюя'
    alpha_len = len(alphabet)
    encrypted_content = ""
    key_shifts = [alphabet.index(k) for k in cipher_key]

    for idx, char in enumerate(content):
        if char in alphabet:
            char_index = alphabet.index(char)
            shift = key_shifts[idx % len(cipher_key)]
            encrypted_content += alphabet[(char_index + shift) % alpha_len]
        else:
            encrypted_content += char
    return encrypted_content

def compute_coincidence_index(text_data):
    alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
    char_count = Counter(char for char in text_data if char in alphabet)
    total_chars = sum(char_count.values())
    coincidence_index = (
        sum(freq * (freq - 1) for freq in char_count.values()) / (total_chars * (total_chars - 1))
        if total_chars > 1 else 0
    )
    return coincidence_index

def display_coincidence_chart(data):
    labels = list(data.keys())
    values = list(data.values())

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, alpha=0.75)
    plt.xlabel('Текст')
    plt.ylabel('Індекс відповідності')
    plt.title('Порівняння індексів відповідності')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

keys_map = {
    2: "да",
    3: "мир",
    4: "ключ",
    5: "земля",
    10: "бензопанос",
    15: "криптографиямич",
    20: "шифровальнаямашинаки"
}

input_file_name = "lab_2.txt"
plaintext = read_input_file(input_file_name).lower()

encrypted_variants = {}
for key_size, cipher_key in keys_map.items():
    encrypted_variants[cipher_key] = vigenere_cipher_encrypt(plaintext, cipher_key)

coincidence_indices = {"Відкритий текст": compute_coincidence_index(plaintext)}
for cipher_key, encrypted_text in encrypted_variants.items():
    coincidence_indices[f"Ключ ({len(cipher_key)})"] = compute_coincidence_index(encrypted_text)

for text_label, coincidence_index in coincidence_indices.items():
    print(f"{text_label}: Індекс відповідності = {coincidence_index:.4f}")

for cipher_key, encrypted_text in encrypted_variants.items():
    output_file_path = f"encrypted_with_key_{len(cipher_key)}.txt"
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(encrypted_text)

display_coincidence_chart(coincidence_indices)

print("Шифрування завершено, індекси відповідності обчислено та виведено в консоль. Графік побудовано.")
