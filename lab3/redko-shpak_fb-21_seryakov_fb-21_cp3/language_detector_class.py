from collections import Counter

class LanguageDetector:
    def __init__(self):
        # частоти рос. мови
        self.common_letters = {'о': 0.10983, 'е': 0.08483, 'а': 0.07998}
        self.rare_letters = {'ф': 0.00267, 'щ': 0.00361, 'ь': 0.01735}
        self.common_bigrams = {'ст': 0.0216, 'но': 0.0169, 'то': 0.0168, 'на': 0.0167, 'ен': 0.0159}
        
        # заборонені біграми (ніколи не зустрічаються в рос мові)
        self.forbidden_bigrams = {
            'ьь', 'ыь', 'щщ', 'щч', 'щй', 'щц', 'щш', 'щщ', 'щэ', 'щю', 'щя',
            'ьы', 'ьэ', 'ыы', 'ыэ', 'эы', 'эь', 'юы', 'юь', 'яы', 'яь'
        }
        
        # порогові значення для різних критеріїв
        self.letter_freq_threshold = 0.4  # допустиме відхилення для частот літер
        self.rare_letter_threshold = 0.05  # макс сумарна частота рідких літер
        self.forbidden_threshold = 0.01    # макс частота заборонених біграм
        self.bigram_threshold = 0.3        # мін схожість біграмного профілю

    def calculate_letter_frequencies(self, text):
        """ обчислює частоти літер у тексті """
        counter = Counter(text)
        total = len(text)
        return {char: count/total for char, count in counter.items()}

    def calculate_bigram_frequencies(self, text):
        """ обчислює частоти біграм на перетині """
        bigrams = [text[i:i+2] for i in range(len(text)-1)]
        counter = Counter(bigrams)
        total = len(bigrams)
        return {bigram: count/total for bigram, count in counter.items()}

    def check_common_letters(self, frequencies):
        """ перевіряє частоти частих літер """
        error = 0
        for letter, expected_freq in self.common_letters.items():
            actual_freq = frequencies.get(letter, 0)
            error += abs(actual_freq - expected_freq) / expected_freq
        return error/len(self.common_letters) <= self.letter_freq_threshold

    def check_rare_letters(self, frequencies):
        """ перевіряє частоти рідких літер """
        total_rare = sum(frequencies.get(letter, 0) for letter in self.rare_letters)
        return total_rare <= self.rare_letter_threshold

    def check_forbidden_bigrams(self, text):
        """ перевіряє наявність заборонених біграм """
        bigram_freqs = self.calculate_bigram_frequencies(text)
        forbidden_freq = sum(bigram_freqs.get(bigram, 0) for bigram in self.forbidden_bigrams)
        return forbidden_freq <= self.forbidden_threshold

    def check_common_bigrams(self, text):
        """ перевіряє частоти найбільш поширених біграм """
        bigram_freqs = self.calculate_bigram_frequencies(text)
        matches = 0
        for bigram in self.common_bigrams:
            if bigram in bigram_freqs:
                actual_freq = bigram_freqs[bigram]
                expected_freq = self.common_bigrams[bigram]
                if abs(actual_freq - expected_freq) / expected_freq <= 0.5:
                    matches += 1
        return matches >= len(self.common_bigrams) * self.bigram_threshold

    def is_meaningful_text(self, text):
        """ перевірка осмисленості тексту"""
        text = text.lower()
        text = text.replace('ё', 'е').replace('ъ', 'ь')
        text = ''.join(c for c in text if c.isalpha())
        
        if len(text) < 100:
            return False
            
        frequencies = self.calculate_letter_frequencies(text)
        
        # всі критерії
        criteria = [
            self.check_common_letters(frequencies),
            self.check_rare_letters(frequencies),
            self.check_forbidden_bigrams(text),
            self.check_common_bigrams(text)
        ]
        
        # якщо проходить більшість критеріїв => вважається осмисленим
        return sum(criteria) >= 3


def test_language_detector():
    detector = LanguageDetector()
    
    # тест на осмисленому тексті
    meaningful_text = """
    востокзападсеверюгсолнцелуназемлянебоморерекагородстранадомлес
    человекженщинамужчинаработакнигажизньсмертьдетиродителимирвойна
    """
    meaningful_text = meaningful_text.strip()
    assert detector.is_meaningful_text(meaningful_text), "Помилка: осмислений текст не розпізнано"
    
    # тест на випадковому тексті
    random_text = "щщщфьыэюяфьыыээяюфьыээюяфьыээюя" * 10
    assert not detector.is_meaningful_text(random_text), "Помилка: випадковий текст прийнято за осмислений"
    
    # тест частотного аналізу
    frequencies = detector.calculate_letter_frequencies(meaningful_text)
    assert 'о' in frequencies, "Помилка: не знайдено частоту літери 'о'"
    
    print("всі тести пройдено успішно!")

if __name__ == "__main__":
    test_language_detector()