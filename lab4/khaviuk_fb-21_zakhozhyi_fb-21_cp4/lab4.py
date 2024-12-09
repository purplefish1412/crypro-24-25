import random

def is_prime_trial_division(n):
    """
    Перевірка на простоту методом пробних ділень.
    """
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
        if n % p == 0 and n != p:
            return False
    return True

def miller_rabin_test(n, k=5):
    """
    Імовірнісний тест Міллера-Рабіна.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Представлення n-1 у вигляді 2^s * d
    s, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    def check_composite(a):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return False
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return False
        return True

    for _ in range(k):
        a = random.randint(2, n - 2)
        if check_composite(a):
            return False
    return True

def generate_random_prime(bit_length):
    """
    Генерація випадкового простого числа заданої довжини в бітах.
    """
    while True:
        candidate = random.getrandbits(bit_length) | (1 << (bit_length - 1)) | 1
        if is_prime_trial_division(candidate) and miller_rabin_test(candidate):
            return candidate

# Використання функції
bit_length = 256  # Довжина числа в бітах
random_prime = generate_random_prime(bit_length)
print(f"Випадкове просте число ({bit_length} біт): {random_prime}")
