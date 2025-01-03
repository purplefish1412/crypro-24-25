import re
import pandas as pd
from collections import Counter
from math import log2

def preprocess_text(text, remove_spaces=False):
    """Очистка тексту: перетворення в нижній регістр, видалення неалфавітних символів."""
    cleaned_text = text.lower()
    cleaned_text = re.sub(r'[^а-яё ]', '', cleaned_text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    if remove_spaces:
        cleaned_text = cleaned_text.replace(" ", "")
    return cleaned_text

def calculate_frequencies(text):
    """Обчислення частот літер і біграм."""
    letter_counts = Counter(text)
    total_letters = sum(letter_counts.values())
    letter_frequencies = {char: count / total_letters for char, count in letter_counts.items()}

    bigram_counts_with_overlap = Counter(
        [text[i:i + 2] for i in range(len(text) - 1) if " " not in text[i:i + 2]]
    )
    total_bigrams_with_overlap = sum(bigram_counts_with_overlap.values())
    bigram_frequencies_with_overlap = {
        bigram: count / total_bigrams_with_overlap for bigram, count in bigram_counts_with_overlap.items()
    }

    bigram_counts_no_overlap = Counter(
        [text[i:i + 2] for i in range(0, len(text) - 1, 2) if " " not in text[i:i + 2]]
    )
    total_bigrams_no_overlap = sum(bigram_counts_no_overlap.values())
    bigram_frequencies_no_overlap = {
        bigram: count / total_bigrams_no_overlap for bigram, count in bigram_counts_no_overlap.items()
    }

    return letter_frequencies, bigram_frequencies_with_overlap, bigram_frequencies_no_overlap

def calculate_entropy(frequencies):
    """Обчислення ентропії."""
    return -sum(freq * log2(freq) for freq in frequencies.values())

def save_frequencies_to_csv(data, filename, index_label=None, columns_label=None):
    """Збереження частот у CSV-файл."""
    dataframe = pd.DataFrame.from_dict(data, orient='index', columns=[columns_label])
    dataframe = dataframe.sort_values(by=columns_label, ascending=False)
    dataframe.to_csv(filename, index_label=index_label)

def main():
    with open("input_text.txt", "r", encoding="utf-8") as file:
        raw_text = file.read()

    text_with_spaces = preprocess_text(raw_text, remove_spaces=False)
    text_without_spaces = preprocess_text(raw_text, remove_spaces=True)

    letter_freq_with_spaces, bigram_freq_with_overlap_with_spaces, bigram_freq_no_overlap_with_spaces = calculate_frequencies(text_with_spaces)
    letter_freq_without_spaces, bigram_freq_with_overlap_without_spaces, bigram_freq_no_overlap_without_spaces = calculate_frequencies(text_without_spaces)

    entropy_letters_with_spaces = calculate_entropy(letter_freq_with_spaces)
    entropy_bigrams_with_overlap_with_spaces = calculate_entropy(bigram_freq_with_overlap_with_spaces) / 2
    entropy_bigrams_no_overlap_with_spaces = calculate_entropy(bigram_freq_no_overlap_with_spaces) / 2

    entropy_letters_without_spaces = calculate_entropy(letter_freq_without_spaces)
    entropy_bigrams_with_overlap_without_spaces = calculate_entropy(bigram_freq_with_overlap_without_spaces) / 2
    entropy_bigrams_no_overlap_without_spaces = calculate_entropy(bigram_freq_no_overlap_without_spaces) / 2

    print("\nРезультати для тексту з пробілами:")
    print(f"Ентропія літер: {entropy_letters_with_spaces:.4f}")
    print(f"Ентропія біграм (з перетином): {entropy_bigrams_with_overlap_with_spaces:.4f}")
    print(f"Ентропія біграм (без перетину): {entropy_bigrams_no_overlap_with_spaces:.4f}")

    print("\nРезультати для тексту без пробілів:")
    print(f"Ентропія літер: {entropy_letters_without_spaces:.4f}")
    print(f"Ентропія біграм (з перетином): {entropy_bigrams_with_overlap_without_spaces:.4f}")
    print(f"Ентропія біграм (без перетину): {entropy_bigrams_no_overlap_without_spaces:.4f}")

    save_frequencies_to_csv(letter_freq_with_spaces, "letter_frequencies_with_spaces.csv", index_label="Літера", columns_label="Частота")
    save_frequencies_to_csv(bigram_freq_with_overlap_with_spaces, "bigram_frequencies_with_overlap_with_spaces.csv", index_label="Біграма", columns_label="Частота з перетином")
    save_frequencies_to_csv(bigram_freq_no_overlap_with_spaces, "bigram_frequencies_no_overlap_with_spaces.csv", index_label="Біграма", columns_label="Частота без перетину")

    save_frequencies_to_csv(letter_freq_without_spaces, "letter_frequencies_without_spaces.csv", index_label="Літера", columns_label="Частота")
    save_frequencies_to_csv(bigram_freq_with_overlap_without_spaces, "bigram_frequencies_with_overlap_without_spaces.csv", index_label="Біграма", columns_label="Частота з перетином")
    save_frequencies_to_csv(bigram_freq_no_overlap_without_spaces, "bigram_frequencies_no_overlap_without_spaces.csv", index_label="Біграма", columns_label="Частота без перетину")

if __name__ == "__main__":
    main()
