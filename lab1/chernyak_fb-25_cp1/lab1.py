import re
import pandas as pd
import numpy as np
from collections import Counter
from math import log2

def preprocess_text(text, remove_spaces=False):
    text = text.lower()
    text = re.sub(r'[^а-яё ]', '', text)
    text = re.sub(r'\s+', ' ', text)
    if remove_spaces:
        text = text.replace(" ", "")
    return text

def bigram_frequencies(text, overlap=True):
    bigrams = []
    step = 1 if overlap else 2
    for i in range(0, len(text) - 1, step):
        bigrams.append(text[i:i+2])
    bigram_counts = Counter(bigrams)
    total_bigrams = sum(bigram_counts.values())
    return {bigram: count / total_bigrams for bigram, count in bigram_counts.items()}

def calculate_frequencies(text, overlap):
    letter_counts = Counter(text)
    total_letters = sum(letter_counts.values())
    letter_freq = {char: count / total_letters for char, count in letter_counts.items()}
    bigram_freqs = bigram_frequencies(text, overlap)
    alphabet = sorted(set(text) - {" "})
    bigram_matrix = pd.DataFrame(0, index=alphabet, columns=alphabet, dtype=float)
    for bigram, freq in bigram_freqs.items():
        if bigram[0] in alphabet and bigram[1] in alphabet:
            bigram_matrix.at[bigram[0], bigram[1]] = freq
    return letter_freq, bigram_matrix

def entropy(frequencies):
    if isinstance(frequencies, dict):
        return -sum(freq * log2(freq) for freq in frequencies.values() if freq > 0)
    elif isinstance(frequencies, pd.DataFrame):
        return -np.sum(frequencies.values * np.log2(frequencies.values + 1e-10))

def redundancy(H, H_max):
    return 1 - H / H_max

def save_to_csv(data, filename, index_label=None, columns_label=None):
    if isinstance(data, pd.DataFrame):
        data.to_csv(filename, index_label=index_label)
    else:
        df = pd.DataFrame.from_dict(data, orient='index', columns=[columns_label])
        df = df.sort_values(by=columns_label, ascending=False)
        df.to_csv(filename, index_label=index_label)

def main():
    with open("input_text.txt", "r", encoding="utf-8") as file:
        text = file.read()

    cleaned_text_with_spaces = preprocess_text(text, remove_spaces=False)
    cleaned_text_without_spaces = preprocess_text(text, remove_spaces=True)

    letter_freq_with_spaces, bigram_matrix_overlap_with_spaces = calculate_frequencies(cleaned_text_with_spaces, overlap=True)
    _, bigram_matrix_non_overlap_with_spaces = calculate_frequencies(cleaned_text_with_spaces, overlap=False)

    letter_freq_without_spaces, bigram_matrix_overlap_without_spaces = calculate_frequencies(cleaned_text_without_spaces, overlap=True)
    _, bigram_matrix_non_overlap_without_spaces = calculate_frequencies(cleaned_text_without_spaces, overlap=False)

    H1_with_spaces = entropy(letter_freq_with_spaces)
    H2_overlap_with_spaces = entropy(bigram_matrix_overlap_with_spaces) / 2
    H2_non_overlap_with_spaces = entropy(bigram_matrix_non_overlap_with_spaces) / 2

    H1_without_spaces = entropy(letter_freq_without_spaces)
    H2_overlap_without_spaces = entropy(bigram_matrix_overlap_without_spaces) / 2
    H2_non_overlap_without_spaces = entropy(bigram_matrix_non_overlap_without_spaces) / 2

    H_max_1 = log2(len(set(cleaned_text_with_spaces) - {" "}))
    H_max_2 = log2(len(set(cleaned_text_with_spaces) - {" "}) ** 2)

    redundancy_H1_with_spaces = redundancy(H1_with_spaces, H_max_1)
    redundancy_H2_overlap_with_spaces = redundancy(H2_overlap_with_spaces, H_max_2)
    redundancy_H2_non_overlap_with_spaces = redundancy(H2_non_overlap_with_spaces, H_max_2)

    redundancy_H1_without_spaces = redundancy(H1_without_spaces, H_max_1)
    redundancy_H2_overlap_without_spaces = redundancy(H2_overlap_without_spaces, H_max_2)
    redundancy_H2_non_overlap_without_spaces = redundancy(H2_non_overlap_without_spaces, H_max_2)

    print("Ентропія та надлишковість для тексту з пробілами:")
    print(f"H1 (ентропія букв): {H1_with_spaces}, R: {redundancy_H1_with_spaces}")
    print(f"H2 (ентропія біграм з перетином): {H2_overlap_with_spaces}, R: {redundancy_H2_overlap_with_spaces}")
    print(f"H2 (ентропія біграм без перетину): {H2_non_overlap_with_spaces}, R: {redundancy_H2_non_overlap_with_spaces}")

    print("\nЕнтропія та надлишковість для тексту без пробілів:")
    print(f"H1 (ентропія букв): {H1_without_spaces}, R: {redundancy_H1_without_spaces}")
    print(f"H2 (ентропія біграм з перетином): {H2_overlap_without_spaces}, R: {redundancy_H2_overlap_without_spaces}")
    print(f"H2 (ентропія біграм без перетину): {H2_non_overlap_without_spaces}, R: {redundancy_H2_non_overlap_without_spaces}")

    save_to_csv(letter_freq_with_spaces, "letter_frequencies_with_spaces.csv", index_label="Літера", columns_label="Частота")
    save_to_csv(bigram_matrix_overlap_with_spaces, "bigram_matrix_overlap_with_spaces.csv", index_label="Перша літера")
    save_to_csv(bigram_matrix_non_overlap_with_spaces, "bigram_matrix_non_overlap_with_spaces.csv", index_label="Перша літера")
    save_to_csv(letter_freq_without_spaces, "letter_frequencies_without_spaces.csv", index_label="Літера", columns_label="Частота")
    save_to_csv(bigram_matrix_overlap_without_spaces, "bigram_matrix_overlap_without_spaces.csv", index_label="Перша літера")
    save_to_csv(bigram_matrix_non_overlap_without_spaces, "bigram_matrix_non_overlap_without_spaces.csv", index_label="Перша літера")

if __name__ == "__main__":
    main()
