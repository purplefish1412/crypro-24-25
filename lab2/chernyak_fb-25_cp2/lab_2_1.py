def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()


def vigenere_encrypt(text, key):
    alphabet = 'а б в г д е ё ж з и й к л м н о п р с т у ф х ц ч ш щ ъ ы ь э ю я'
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

for key, encrypted_text in encrypted_texts.items():
    output_file_name = f"encrypted_with_key_{len(key)}.txt"
    with open(output_file_name, 'w', encoding='utf-8') as file:
        file.write(encrypted_text)

print("Шифрування завершено. Зашифровані тексти збережено у файли.")
