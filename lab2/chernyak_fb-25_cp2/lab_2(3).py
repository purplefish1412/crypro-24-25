from collections import Counter
import matplotlib.pyplot as plt

def calculate_coincidence_rate(data):
    total_chars = len(data)
    if total_chars < 2:
        return 0.0

    char_counts = Counter(data)
    coincidence_rate = sum(freq * (freq - 1) for freq in char_counts.values())
    return coincidence_rate / (total_chars * (total_chars - 1))

def segment_text(input_text, segment_size):
    segments = [''] * segment_size
    for idx, char in enumerate(input_text):
        segments[idx % segment_size] += char
    return segments


def compute_avg_coincidence_for_size(input_text, segment_size):
    segments = segment_text(input_text, segment_size)
    coincidence_rates = [calculate_coincidence_rate(segment) for segment in segments]
    return sum(coincidence_rates) / len(coincidence_rates)


def estimate_key_size(encrypted_text, max_size=30):
    results = {}
    for size in range(2, max_size + 1):
        coincidence = compute_avg_coincidence_for_size(encrypted_text, size)
        results[size] = coincidence
        print(f"Розмір ключа: {size}, IC: {coincidence}")
    return results


def plot_key_indices(indices):
    keys = list(indices.keys())  # Ключі
    values = list(indices.values())  # Індекси відповідності

    plt.figure(figsize=(10, 6))
    plt.bar(keys, values, alpha=0.75)
    plt.xlabel('Ключ')
    plt.ylabel('Індекс відповідності (IC)')
    plt.title('Порівняння індексів відповідності для різних ключів')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def decrypt_vigenere_cipher(encoded_text, key):
    result = []
    lower_key = key.lower()
    key_len = len(lower_key)
    key_counter = 0

    for symbol in encoded_text:
        if 'а' <= symbol <= 'я':
            shift_value = ord(lower_key[key_counter % key_len]) - ord('а')
            decoded_symbol = chr((ord(symbol) - ord('а') - shift_value + 32) % 32 + ord('а'))
            result.append(decoded_symbol)
            key_counter += 1

    return ''.join(result)


def recover_key(encoded_text, segment_size):
    segments = segment_text(encoded_text, segment_size)
    recovered_key = []

    for segment in segments:
        char_freq = Counter(segment)
        top_char = max(char_freq.items(), key=lambda x: x[1])[0]
        offset = (ord(top_char) - ord('о') + 32) % 32
        recovered_key.append(chr(ord('а') + offset))

    return ''.join(recovered_key)


def load_file_content(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
    except IOError:
        print("Не вдалося відкрити файл!")
        exit(1)

    content = content.replace('ё', 'е')
    processed_text = ''.join(c for c in content if 'а' <= c <= 'я')
    return processed_text

def print_coincidence_indices(encrypted_text, decrypted_text):
    ic_encrypted = calculate_coincidence_rate(encrypted_text)
    ic_decrypted = calculate_coincidence_rate(decrypted_text)

    print(f"\nІндекс відповідності зашифрованого тексту: {ic_encrypted:.4f}")
    print(f"\nІндекс відповідності розшифрованого тексту: {ic_decrypted:.4f}")

def main():
    file_name = "lab_2_3.txt"
    encrypted_text = load_file_content(file_name)

    results = estimate_key_size(encrypted_text)
    plot_key_indices(results)

    detected_key_14 = recover_key(encrypted_text, 14)
    print(f"\nЙмовірний ключ: {detected_key_14}")

    decrypted_output_14 = decrypt_vigenere_cipher(encrypted_text, detected_key_14)
    print(f"\nРозшифрований текст:\n{decrypted_output_14}")

    print_coincidence_indices(encrypted_text, decrypted_output_14)



if __name__ == "__main__":
    main()
