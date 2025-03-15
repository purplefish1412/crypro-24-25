import matplotlib.pyplot as plt
from collections import Counter


def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()


def vigenere_encrypt(text, key):
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщьыэюя'
    m = len(alphabet)
    encrypted_text = ""
    key_indices = [alphabet.index(k) for k in key]

    for i, char in enumerate(text):
        if char in alphabet:
            text_index = alphabet.index(char)
            key_index = key_indices[i % len(key)]
            encrypted_text += alphabet[(text_index + key_index) % m]
        else:
            encrypted_text += char
    return encrypted_text


def calculate_index_of_coincidence(text):
    alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
    m = len(alphabet)
    counts = Counter(char for char in text if char in alphabet)
    n = sum(counts.values())
    index = sum(f * (f - 1) for f in counts.values()) / (n * (n - 1)) if n > 1 else 0
    return index


def plot_indices(indices):
    labels = list(indices.keys())
    values = list(indices.values())

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, alpha=0.75)
    plt.xlabel('Текст')
    plt.ylabel('Індекс відповідності')
    plt.title('Порівняння індексів відповідності')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


keys = {
    2: "да",
    3: "мир",
    4: "ключ",
    5: "земля",
    10: "безопаснос",
    15: "криптографиямор",
    20: "шифровальнаямашинася"
}

file_name = "lab_2.txt"
plain_text = read_file(file_name).lower()

encrypted_texts = {}
for key_len, key in keys.items():
    encrypted_texts[key] = vigenere_encrypt(plain_text, key)

indices = {"Відкритий текст": calculate_index_of_coincidence(plain_text)}
for key, encrypted_text in encrypted_texts.items():
    indices[f"Ключ ({len(key)})"] = calculate_index_of_coincidence(encrypted_text)

for text_name, index in indices.items():
    print(f"{text_name}: Індекс відповідності = {index:.4f}")

for key, encrypted_text in encrypted_texts.items():
    output_file_name = f"encrypted_with_key_{len(key)}.txt"
    with open(output_file_name, 'w', encoding='utf-8') as file:
        file.write(encrypted_text)

plot_indices(indices)

print("Шифрування завершено, індекси відповідності обчислено та виведено в консоль. Графік побудовано.")
