import string

def read_file(f_name):
    file = open(f_name, "r", encoding="utf-8")
    return file.read()

def normalize_text_with_space(text):
    allowed_chars = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя " + "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ ")
    norm_text = ''.join(filter(lambda char: char in allowed_chars, text))
    norm_text = norm_text.lower()
    norm_text = norm_text.replace('ъ', 'ь')
    norm_text = norm_text.replace('ё', 'е')
    with open("normalized_text_with_space.txt", "w", encoding="utf-8") as file:
        file.write(norm_text)

def count_letters(text):
    letter_count = {}
    for char in text:
        if char in letter_count:
            letter_count[char] += 1
        else:
            letter_count[char] = 1
    return letter_count

def count_bigrams(text):
    bigram_count = {}
    for i in range(len(text) - 1):
        bigram = text[i:i+2]
        if bigram in bigram_count:
            bigram_count[bigram] += 1
        else:
            bigram_count[bigram] = 1
    return bigram_count



def main():
    # text = read_file("text.txt")
    # norm_text = normalize_text_with_space(text)

    norm_text = read_file("normalized_text_with_space.txt")
    print(count_letters(norm_text)) 
    print(len(count_letters(norm_text))) # 32


if __name__ == "__main__":
    main()