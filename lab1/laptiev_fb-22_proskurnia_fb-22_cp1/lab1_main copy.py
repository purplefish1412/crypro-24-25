from math import log2

class entrho_calc:

    space = True # with or without spaces
    text = ""

    monogram_count = 0
    monograms = {}
    mono_freq = {}

    bigram_count = 0
    bigrams = {}

    totalOverlappedBigrams = 0
    overlappedBigramCount = {}

    def __init__(self, path, space=True):
        self.space = space
        file = open(path, "r", encoding="utf-8")
        self.text = file.read()

        if (self.space==True):
            allowed_chars = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя " + "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ ")
        else:
            allowed_chars = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя" + "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")
        self.text = ''.join(filter(lambda char: char in allowed_chars, self.text))
        self.text = self.text.lower()
        self.text = self.text.replace('ъ', 'ь')
        self.text = self.text.replace('ё', 'е')

        # with open("normalized_text.txt", "w", encoding="utf-8") as file:
        #     file.write(self.text)

    def count_monograms(self):
        for char in self.text:
            if char in self.monograms:
                self.monograms[char] += 1
            else:
                self.monograms[char] = 1
            self.monogram_count += 1

    def count_bigrams(self):
        for i in range(len(self.text) - 1):
            bigram = self.text[i:i+2]
            if bigram in self.bigrams:
                self.bigrams[bigram] += 1
            else:
                self.bigrams[bigram] = 1
            self.bigram_count += 1

    def mono_frequancy(self):
        self.mono_freq = self.monograms
        for char in self.monograms:
                p = self.monograms[char] / self.monogram_count
                self.mono_freq[char] = p * log2(p)

def main():
    text_with_space = entrho_calc("text.txt")
    text_without_space = entrho_calc("text.txt", False)

    text_with_space.count_monograms()
    text_with_space.count_bigrams()

    text_with_space.mono_frequancy()
    print("Monogram Frequencies with Spaces:")
    for char, freq in text_with_space.mono_freq.items():
        print(f"'{char}': {freq:.6f}")





if __name__ == "__main__":
    main()