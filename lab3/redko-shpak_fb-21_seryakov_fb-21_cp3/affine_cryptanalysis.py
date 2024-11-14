from math_class import solve_linear_congruence, mod_inverse

class AffineCryptanalysis:
    def __init__(self, m=31):
        self.m = m
        self.m_squared = m * m
        
    def encrypt_bigram(self, X, a, b):
        """ шифрує біграми за формулою Y = (aX + b) mod m^2 """
        return (a * X + b) % self.m_squared
    
    def decrypt_bigram(self, Y, a, b):
        """ дешифрує біграми за формулою X = a^(-1)(Y - b) mod m^2 """
        a_inv = mod_inverse(a, self.m_squared)
        if a_inv is None:
            raise ValueError(f"Не існує оберненого до {a} за модулем {self.m_squared}")
        return (a_inv * (Y - b)) % self.m_squared
    
    def find_possible_keys(self, x1, y1, x2, y2):
        """ знаходить можливі ключі (a,b) за двома парами біграм (X*, Y*) і (X**, Y**) """
        diff_y = (y1 - y2) % self.m_squared
        diff_x = (x1 - x2) % self.m_squared
        
        possible_a = solve_linear_congruence(diff_x, diff_y, self.m_squared)
        
        keys = []
        for a in possible_a:
            if mod_inverse(a, self.m_squared) is not None:
                b = (y1 - a * x1) % self.m_squared
                keys.append((a, b))
        
        return keys
    
    def encrypt_text(self, text_numbers, a, b):
        """ шифрує послідовності чисел (які відповідають біграмам тексту) """
        encrypted = []
        for i in range(0, len(text_numbers), 2):
            X = (text_numbers[i] * self.m + text_numbers[i + 1]) % self.m_squared
            Y = self.encrypt_bigram(X, a, b)
            encrypted.extend([Y // self.m, Y % self.m])
        return encrypted
    
    def decrypt_text(self, text_numbers, a, b):
        """ дешифрує послідовності чисел (які відповідають біграмам тексту) """
        decrypted = []
        for i in range(0, len(text_numbers), 2):
            Y = (text_numbers[i] * self.m + text_numbers[i + 1]) % self.m_squared
            X = self.decrypt_bigram(Y, a, b)
            decrypted.extend([X // self.m, X % self.m])
        return decrypted


def test_affine_cryptanalysis():
    cryptanalysis = AffineCryptanalysis()
    
    # тест шифрування/дешифрування однієї біграми
    a, b = 7, 13
    X = 42
    Y = cryptanalysis.encrypt_bigram(X, a, b)
    X_dec = cryptanalysis.decrypt_bigram(Y, a, b)
    assert X == X_dec, f"Помилка: {X} != {X_dec}"
    
    # тест пошуку ключів
    x1, y1 = 42, cryptanalysis.encrypt_bigram(42, a, b)
    x2, y2 = 100, cryptanalysis.encrypt_bigram(100, a, b)
    keys = cryptanalysis.find_possible_keys(x1, y1, x2, y2)
    assert (a, b) in keys, f"Правильний ключ {(a, b)} не знайдено серед {keys}"
    
    # тест шифрування/дешифрування тексту
    text = [1, 2, 3, 4, 5, 6]
    encrypted = cryptanalysis.encrypt_text(text, a, b)
    decrypted = cryptanalysis.decrypt_text(encrypted, a, b)
    assert text == decrypted, f"Помилка: {text} != {decrypted}"
    
    print("всі тести пройдено успішно!")

if __name__ == "__main__":
    test_affine_cryptanalysis()