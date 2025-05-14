import matplotlib.pyplot as plt
from collections import Counter

# Алфавит
ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
ALPHABET_SIZE = len(ALPHABET)


# Шифрование текста
def vigenere_encrypt(plaintext, key):
    encrypted = []
    key_indices = [ALPHABET.index(k) for k in key]
    for i, char in enumerate(plaintext):
        if char in ALPHABET:
            char_index = ALPHABET.index(char)
            key_index = key_indices[i % len(key)]
            encrypted_index = (char_index + key_index) % ALPHABET_SIZE
            encrypted.append(ALPHABET[encrypted_index])
        else:
            encrypted.append(char)  # Пропускаем символы, не входящие в алфавит
    return ''.join(encrypted)


# Дешифрование текста
def vigenere_decrypt(ciphertext, key):
    decrypted = []
    key_indices = [ALPHABET.index(k) for k in key]
    for i, char in enumerate(ciphertext):
        if char in ALPHABET:
            char_index = ALPHABET.index(char)
            key_index = key_indices[i % len(key)]
            decrypted_index = (char_index - key_index) % ALPHABET_SIZE
            decrypted.append(ALPHABET[decrypted_index])
        else:
            decrypted.append(char)  # Пропускаем символы, не входящие в алфавит
    return ''.join(decrypted)


# Разбиение текста на блоки
def split_into_blocks(text, key_length):
    blocks = ['' for _ in range(key_length)]
    for i, char in enumerate(text):
        blocks[i % key_length] += char
    return blocks


# Расчет индекса совпадений
def calculate_ic(text):
    frequencies = Counter(text)
    n = len(text)
    return sum(f * (f - 1) for f in frequencies.values()) / (n * (n - 1)) if n > 1 else 0


# Оценка длины ключа
def estimate_key_length(ciphertext, max_key_length=30):
    ic_values = {}
    for key_length in range(2, max_key_length + 1):
        blocks = split_into_blocks(ciphertext, key_length)
        avg_ic = sum(calculate_ic(block) for block in blocks) / key_length
        ic_values[key_length] = avg_ic
    return ic_values


# Определение ключа
def find_key(ciphertext, key_length):
    blocks = split_into_blocks(ciphertext, key_length)
    key = ''
    for block in blocks:
        frequencies = Counter(block)
        most_common = max(frequencies, key=frequencies.get)  # Самая частая буква
        key_letter_index = (ALPHABET.index(most_common) - ALPHABET.index('о')) % ALPHABET_SIZE  # Допустим, 'о' - это наиболее частая буква
        key += ALPHABET[key_letter_index]
    return key


# Основная программа
if __name__ == "__main__":
    # Чтение зашифрованного текста (вы указываете свой файл)
    input_file = 'ciphertext.txt'  # Убедитесь, что файл существует и находится в той же папке
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            ciphertext = file.read().strip()
    except FileNotFoundError:
        print("Ошибка: файл с шифротекстом не найден.")
        exit(1)

    # 1. Оценка длины ключа
    print("Оценка длины ключа...")
    ic_results = estimate_key_length(ciphertext)
    for length, ic in ic_results.items():
        print(f"Длина ключа {length}: IC = {ic:.4f}")

    # 2. Определение наиболее вероятной длины ключа
    likely_key_length = max(ic_results, key=ic_results.get)
    print(f"Наиболее вероятная длина ключа: {likely_key_length}")

    # Построение графика IC
    plt.plot(list(ic_results.keys()), list(ic_results.values()), marker='o')
    plt.title("График индекса совпадений")
    plt.xlabel("Длина ключа")
    plt.ylabel("IC")
    plt.grid()
    plt.show()

    # 3. Определение ключа
    found_key = find_key(ciphertext, likely_key_length)
    print(f"Найденный ключ: {found_key}")

    # 4. Дешифровка текста
    decrypted_text = vigenere_decrypt(ciphertext, found_key)
    print(f"Расшифрованный текст сохранен в файл: decrypted_output.txt")
    with open('decrypted_output.txt', 'w', encoding='utf-8') as file:
        file.write(decrypted_text)


sample_text = """
На рассвете солнце медленно поднималось над горизонтом, окрашивая небо в нежные розовые тона. Прохладный утренний воздух был наполнен ароматом полевых цветов и свежескошенной травы. Маленькая деревенька, затерянная среди холмов, постепенно просыпалась. Дым из печных труб поднимался вверх ровными столбами, растворяясь в прозрачном воздухе. На околице паслось стадо, присматривал за которым старый пастух. Его верный пес лежал рядом, внимательно следя за овцами.

В такие моменты особенно чувствуется единение с природой. Каждый звук, каждое движение наполнено особым смыслом. Вот пролетела стайка птиц, направляясь к далекому лесу. В высокой траве стрекочут кузнечики, а над цветущим лугом кружат разноцветные бабочки. Легкий ветерок колышет верхушки берез, создавая причудливую игру света и тени.
"""