from math import log2

class entrho_calc:

    space = True # with or without spaces
    text = ""

    monogram_count = 0
    monograms = {}
    monogram_frequancy = {}

    bigram_count = 0
    bigrams = {}
    bigrams_frequancy = {}

    totalOverlappedBigrams = 0
    overlappedBigramCount = {}

    def __init__(self, path, space=True):
        self.space = space
        file = open(path, "r", encoding="utf-8")
        self.text = file.read()

        self.text = self.text.lower()
        if (self.space==True):
            allowed_chars = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя ")
        else:
            allowed_chars = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
        self.text = ''.join(filter(lambda char: char in allowed_chars, self.text))
        self.text = self.text.replace('ъ', 'ь')
        self.text = self.text.replace('ё', 'е')

    def save_to_file(self, name=""):
        with open("normalized_text" + name + ".txt", "w", encoding="utf-8") as file:
            file.write(self.text)
            file.close()

    def count_monograms(self):
        for char in self.text:
            if char in self.monograms:
                self.monograms[char] += 1
            else:
                self.monograms[char] = 1
            self.monogram_count += 1
    
    def count_bigrams(self):
        self.bigrams={}
        for i in range(len(self.text) - 1):
            bigram = self.text[i:i+2]
            if bigram in self.bigrams:
                self.bigrams[bigram] += 1
            else:
                self.bigrams[bigram] = 1
            self.bigram_count += 1

    def count_bigrams_not_overlapped(self):
        self.bigrams={}
        for i in range(0, len(self.text) - 1, 2):
            bigram = self.text[i:i+2]
            if bigram in self.bigrams:
                self.bigrams[bigram] += 1
            else:
                self.bigrams[bigram] = 1
            self.bigram_count += 1

    def mono_frequancy_calc(self):
        self.monogram_frequancy = self.monograms
        for char in self.monogram_frequancy:
                self.monograms[char] = self.monograms[char] / self.monogram_count

    def bigr_frequancy_calc(self):
        self.bigrams_frequancy = self.bigrams
        for char in self.bigrams_frequancy:
                self.bigrams[char] = self.bigrams[char] / self.bigram_count

    def entrophy_calc(self, freq_list):
        arr = freq_list
        for char in arr:
                arr[char] = arr[char] * log2(arr[char])
        return -sum(arr.values())

def main():
    # print("######spaces######")
    # text_with_space = entrho_calc("text.txt")
    # # text_with_space = entrho_calc("lab1/laptiev_fb-22_proskurnia_fb-22_cp1/text.txt")

    # #monograms
    # text_with_space.count_monograms()
    # text_with_space.mono_frequancy_calc()
    # print("monograms frequancy:")
    # for char, gram in text_with_space.monogram_frequancy.items():
    #     print(f"{char}, {gram:.20f}")
    # print(f"monograms entrophy: {text_with_space.entrophy_calc(text_with_space.monogram_frequancy)}")

    # #birgams overlapped
    # text_with_space.count_bigrams()
    # text_with_space.bigr_frequancy_calc()
    # print("bigrams frequancy:")
    # for char, gram in text_with_space.bigrams_frequancy.items():
    #     print(f"{char}, {gram:.20f}")
    # print(f"bigrams overlapped entrophy: {text_with_space.entrophy_calc(text_with_space.bigrams_frequancy)}")

    # #birgams not overlapped
    # text_with_space.count_bigrams_not_overlapped()
    # text_with_space.bigr_frequancy_calc()
    # print("bigrams frequancy:")
    # for char, gram in text_with_space.bigrams_frequancy.items():
    #     print(f"{char}, {gram:.20f}")
    # print(f"bigrams not overlapped entrophy: {text_with_space.entrophy_calc(text_with_space.bigrams_frequancy)}")

#===============================================================================================================================

    print("######NO spaces######")
    text_without_space = entrho_calc("text.txt", False)
    text_without_space.save_to_file("shit")

    #monograms
    text_without_space.count_monograms()
    text_without_space.mono_frequancy_calc()
    print("monograms frequancy:")
    for char, gram in text_without_space.monogram_frequancy.items():
        print(f"{char}, {gram:.20f}")
    print(f"monograms entrophy: {text_without_space.entrophy_calc(text_without_space.monogram_frequancy)}")

    #bigrams overlapped
    text_without_space.count_bigrams()
    text_without_space.bigr_frequancy_calc()
    print("bigrams frequancy:")
    for char, gram in text_without_space.bigrams_frequancy.items():
        print(f"{char}, {gram:.20f}")
    print(f"bigrams overllaped entrophy: {text_without_space.entrophy_calc(text_without_space.bigrams_frequancy)}")
    
    #bigrams not overlapped
    text_without_space.count_bigrams_not_overlapped()
    text_without_space.bigr_frequancy_calc()
    print("bigrams frequancy:")
    for char, gram in text_without_space.bigrams_frequancy.items():
        print(f"{char}, {gram:.20f}")
    print(f"bigrams not overllaped entrophy: {text_without_space.entrophy_calc(text_without_space.bigrams_frequancy)}")



if __name__ == "__main__":
    main()