import itertools
from text_class import TextProcessor
from affine_cryptanalysis import AffineCryptanalysis
from language_detector_class import LanguageDetector

class CryptanalysisSystem:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.cryptanalysis = AffineCryptanalysis()
        self.language_detector = LanguageDetector()
        
    def analyze_ciphertext(self, ciphertext):
        # 1. попередня обробка тексту
        filtered_text = self.text_processor.filter_text(ciphertext)
        text_numbers = self.text_processor.text_to_numbers(filtered_text)
        
        # 2. знаходження 5 найчастіших біграм
        frequent_bigrams = [pair[0] for pair in self.text_processor.analyze_bigrams(filtered_text, n=5)]
        print("Найчастіші біграми шифротексту:", frequent_bigrams)
        
        # 3. генерація всіх можливих пар біграм для аналізу
        bigram_pairs = self.text_processor.get_bigram_pairs(frequent_bigrams)
        
        # 4. перебір пар біграм та пошук можливих ключів
        best_result = None
        best_score = 0
        
        for (x1, y1), (x2, y2) in itertools.combinations(bigram_pairs, 2):
            possible_keys = self.cryptanalysis.find_possible_keys(x1, y1, x2, y2)
            
            for key in possible_keys:
                try:
                    # спроба дешифрування
                    decrypted_numbers = self.cryptanalysis.decrypt_text(text_numbers, key[0], key[1])
                    decrypted_text = self.text_processor.numbers_to_text(decrypted_numbers)
                    
                    # перевірка змістовності
                    if self.language_detector.is_meaningful_text(decrypted_text):
                        # обчислення "якості" тексту на основі частот
                        frequencies = self.language_detector.calculate_letter_frequencies(decrypted_text)
                        score = sum(1 for letter in self.language_detector.common_letters 
                                  if abs(frequencies.get(letter, 0) - 
                                       self.language_detector.common_letters[letter]) < 0.02)
                        
                        if score > best_score:
                            best_score = score
                            best_result = (decrypted_text, key)
                            
                except Exception as e:
                    continue
        
        if best_result is None:
            raise ValueError("Не вдалося знайти правильний ключ")
            
        return best_result

def main():
    text_path = r'C:\Users\rdk\d_disk\5sem\cryptography\lab_3\task\variants.utf8\02.txt'
    with open(text_path, 'r', encoding='utf-8') as file:
        encrypted_text = file.read().replace('\n', '')

    system = CryptanalysisSystem()

    try:
        decrypted_text, key = system.analyze_ciphertext(encrypted_text)
        print("\nУспішно розшифровано!")
        print(f"Знайдений ключ (a, b) = {key}")
        print("\nРозшифрований текст:")
        print(f"{decrypted_text[:200]}...")
        
    except Exception as e:
        print(f"Помилка під час криптоаналізу: {e}")

if __name__ == "__main__":
    main()