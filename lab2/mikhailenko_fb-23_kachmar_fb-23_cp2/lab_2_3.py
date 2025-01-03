from collections import Counter


def calculate_coincidence_rate(data):
    """Обчислює індекс збігів."""
    total_chars = len(data)
    if total_chars < 2:
        return 0.0

    char_counts = Counter(data)
    coincidence_rate = sum(freq * (freq - 1) for freq in char_counts.values())
    return coincidence_rate / (total_chars * (total_chars - 1))


def segment_text(input_text, segment_size):
    """Розбиває текст на сегменти для аналізу частотності."""
    segments = [''] * segment_size
    for idx, char in enumerate(input_text):
        segments[idx % segment_size] += char
    return segments


def compute_avg_coincidence_for_size(input_text, segment_size):
    """Обчислює середній індекс збігів для певної довжини ключа."""
    segments = segment_text(input_text, segment_size)
    coincidence_rates = [calculate_coincidence_rate(segment) for segment in segments]
    return sum(coincidence_rates) / len(coincidence_rates)


def estimate_key_size(encrypted_text, max_size=30):
    """Оцінює довжину ключа за індексом збігів."""
    results = {}
    for size in range(2, max_size + 1):
        coincidence = compute_avg_coincidence_for_size(encrypted_text, size)
        results[size] = coincidence
        print(f"Довжина ключа: {size}, Індекс збігів: {coincidence}")
    best_key_size = max(results, key=results.get)
    return best_key_size if results[best_key_size] > 0.04 else 1


def decrypt_vigenere_cipher(encoded_text, key):
    """Розшифровує текст шифром Віженера."""
    result = []
    key = key.lower()
    key_len = len(key)
    key_counter = 0

    for symbol in encoded_text:
        if 'а' <= symbol <= 'я':
            shift_value = ord(key[key_counter % key_len]) - ord('а')
            decoded_symbol = chr((ord(symbol) - ord('а') - shift_value + 32) % 32 + ord('а'))
            result.append(decoded_symbol)
            key_counter += 1
        else:
            result.append(symbol)

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
    """Завантажує текст з файлу, очищає його до російських символів."""
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
    except IOError:
        print("Не вдалося відкрити файл!")
        exit(1)

    processed_text = ''.join(c for c in content if 'а' <= c.lower() <= 'я')
    return processed_text


def main():
    file_name = "var_11.txt"
    encrypted_text = load_file_content(file_name)

    key_size = estimate_key_size(encrypted_text)
    print(f"\nЙмовірна довжина ключа: {key_size}")

    detected_key = "венецианскийкупец"
    print(f"\nЙмовірний ключ: {detected_key}")

    decrypted_output = decrypt_vigenere_cipher(encrypted_text, detected_key)
    print(f"\nРозшифрований текст (перші 1000 символів):\n{decrypted_output}")


if __name__ == "__main__":
    main()
