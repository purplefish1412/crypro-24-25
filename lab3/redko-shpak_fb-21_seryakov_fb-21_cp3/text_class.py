from collections import Counter

class TextProcessor:
    def __init__(self):
        # розмір алфавіту (рос. мова без ё, з заміною ъ на ь)
        self.m = 31
        self.m_squared = self.m * self.m
        
        self.alpha = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
        self.char_to_num = {char: num for num, char in enumerate(self.alpha)}
        self.num_to_char = {num: char for num, char in enumerate(self.alpha)}
        
        # найчастіші біграми рос. мови (з методички)
        self.common_bigrams = ['ст', 'но', 'то', 'на', 'ен']
    
    def filter_text(self, text):
        text = text.lower()
        text = text.replace('ё', 'е').replace('ъ', 'ь')
        return ''.join(char for char in text if char in self.char_to_num)
    
    def text_to_numbers(self, text):
        """ текст у послідовність чисел (індексів букв) """
        return [self.char_to_num[char] for char in text]
    
    def numbers_to_text(self, numbers):
        """ послідовність чисел назад у текст """
        return ''.join(self.num_to_char[num % self.m] for num in numbers)
    
    def get_bigram_number(self, bigram):
        """ біграму в число X = x_1m + x_ """
        x1, x2 = bigram
        return (x1 * self.m + x2) % self.m_squared
    
    def get_number_bigram(self, number):
        """ число назад у біграму (x_1, x_2) """
        x1 = number // self.m
        x2 = number % self.m
        return (x1, x2)

    def get_text_bigrams(self, text, overlapping=False):
        """ розбиває текст на біграми """
        if overlapping:
            return [text[i:i+2] for i in range(len(text)-1)]
        return [text[i:i+2] for i in range(0, len(text)-1, 2)]
    
    def analyze_bigrams(self, text, n=5, overlapping=False):
        """ знаходить n найчастіших біграм у тексті """
        # фільтруємо текст та отримуємо біграми
        text = self.filter_text(text)
        bigrams = self.get_text_bigrams(text, overlapping)
        
        # рахуємо та нормалізуємо частоти
        bigram_freq = Counter(bigrams)
        total_bigrams = sum(bigram_freq.values())
        frequencies = {bigram: count / total_bigrams for bigram, count in bigram_freq.items()}
        
        # повертаємо найчастіші біграми
        return sorted(frequencies.items(), key=lambda x: x[1], reverse=True)[:n]
    
    def get_bigram_pairs(self, encrypted_freq_bigrams):
        """ створює пари (X*, Y*) для аналізу на основі частих біграм """
        pairs = []
        
        # часті біграми мови в числа
        known_numbers = [self.get_bigram_number(
            (self.char_to_num[b[0]], self.char_to_num[b[1]]))
            for b in self.common_bigrams
        ]
        
        # часті біграми шифротексту в числа
        encrypted_numbers = [self.get_bigram_number(
            (self.char_to_num[b[0]], self.char_to_num[b[1]]))
            for b in encrypted_freq_bigrams
        ]
        
        # всі можливі пари для аналізу
        for x in known_numbers:
            for y in encrypted_numbers:
                pairs.append((x, y))
        
        return pairs
