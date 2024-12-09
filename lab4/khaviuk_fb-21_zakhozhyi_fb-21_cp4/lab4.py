import random
from math import gcd

# ---------------- option 1 ----------------------------------------

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

# ---------------- option 2 ----------------------------------------

def generate_prime_pairs(bit_length):
    """
    Генерація двох пар простих чисел (p, q) та (p1, q1), де pq <= p1q1.
    """
    # Генерація першої пари для абонента A
    p = generate_random_prime(bit_length)
    q = generate_random_prime(bit_length)
    
    # Генерація другої пари для абонента B
    p1 = generate_random_prime(bit_length)
    q1 = generate_random_prime(bit_length)

    # Перевірка умови pq <= p1q1
    while (p * q) > (p1 * q1):
        p1 = generate_random_prime(bit_length)
        q1 = generate_random_prime(bit_length)
    
    return (p, q), (p1, q1)

# Використання функції
bit_length = 256  # Довжина числа в бітах
pair_A, pair_B = generate_prime_pairs(bit_length)

# Вивід результатів
print(f"Пара для абонента A: p = {pair_A[0]}, q = {pair_A[1]}")
print(f"Пара для абонента B: p1 = {pair_B[0]}, q1 = {pair_B[1]}")


# ---------------- option 3 ----------------------------------------

def generate_rsa_keypair(bit_length):
    """
    Генерує секретний та відкритий ключі для RSA.
    """
    # Генерація простих чисел p та q
    p = generate_random_prime(bit_length)
    q = generate_random_prime(bit_length)

    # Обчислення n та функції Ейлера φ(n)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Генерація відкритої експоненти e (взаємно простої з φ(n))
    e = 65537  # Стандартний вибір для RSA
    if gcd(e, phi_n) != 1:
        # Якщо e не взаємно просте з φ(n), вибираємо інше
        while True:
            e = random.randint(2, phi_n - 1)
            if gcd(e, phi_n) == 1:
                break

    # Обчислення секретного ключа d (обернений за модулем φ(n))
    d = pow(e, -1, phi_n)

    # Повернення секретного (d, p, q) та відкритого (e, n) ключів
    return (d, p, q), (e, n)

def rsa_setup(bit_length):
    """
    Побудова схем RSA для абонентів A та B.
    """
    # Генерація ключових пар для абонента A
    private_key_a, public_key_a = generate_rsa_keypair(bit_length)

    # Генерація ключових пар для абонента B
    private_key_b, public_key_b = generate_rsa_keypair(bit_length)

    return private_key_a, public_key_a, private_key_b, public_key_b

# Використання функції
bit_length = 256  # Довжина простих чисел
private_a, public_a, private_b, public_b = rsa_setup(bit_length)

# Вивід результатів
print(f"Відкритий ключ A: e = {public_a[0]}, n = {public_a[1]}")
print(f"Секретний ключ A: d = {private_a[0]}, p = {private_a[1]}, q = {private_a[2]}")
print(f"Відкритий ключ B: e = {public_b[0]}, n = {public_b[1]}")
print(f"Секретний ключ B: d = {private_b[0]}, p = {private_b[1]}, q = {private_b[2]}")


# ---------------- option 4 ----------------------------------------

def encrypt(message, public_key):
    """
    Функція шифрування повідомлення.
    """
    e, n = public_key
    return pow(message, e, n)

def decrypt(ciphertext, private_key):
    """
    Функція розшифрування повідомлення.
    """
    d, p, q = private_key
    n = p * q
    return pow(ciphertext, d, n)

def sign(message, private_key):
    """
    Функція створення цифрового підпису.
    """
    d, p, q = private_key
    n = p * q
    return pow(message, d, n)

def verify(message, signature, public_key):
    """
    Функція перевірки цифрового підпису.
    """
    e, n = public_key
    return pow(signature, e, n) == message

# Приклад використання

# Генерація ключів для абонентів A і B
bit_length = 256
private_a, public_a, private_b, public_b = rsa_setup(bit_length)

# Повідомлення для шифрування та підпису
message = 12345  # Наприклад, текст повідомлення в числовому форматі

# Абонент A шифрує повідомлення для B
ciphertext = encrypt(message, public_b)
print(f"Зашифроване повідомлення: {ciphertext}")

# Абонент B розшифровує повідомлення
decrypted_message = decrypt(ciphertext, private_b)
print(f"Розшифроване повідомлення: {decrypted_message}")

# Абонент A створює цифровий підпис для повідомлення
signature = sign(message, private_a)
print(f"Цифровий підпис: {signature}")

# Абонент B перевіряє цифровий підпис
is_valid = verify(message, signature, public_a)
print(f"Цифровий підпис вірний: {is_valid}")

# ---------------- option 5 ----------------------------------------

def send_key(k, sender_private_key, sender_public_key, recipient_public_key):
    """
    Функція відправника (абонента A), яка формує зашифроване повідомлення з підписом.
    k - секретний ключ, який потрібно передати
    sender_private_key - приватний ключ відправника
    sender_public_key - публічний ключ відправника
    recipient_public_key - публічний ключ одержувача
    """
    # Шифрування ключа k для отримувача
    encrypted_key = encrypt(k, recipient_public_key)
    
    # Створення цифрового підпису для k
    signature = sign(k, sender_private_key)
    
    # Зашифрування підпису для отримувача
    encrypted_signature = encrypt(signature, recipient_public_key)
    
    # Повертається зашифрований ключ та підпис
    return encrypted_key, encrypted_signature

def receive_key(encrypted_key, encrypted_signature, recipient_private_key, sender_public_key):
    """
    Функція отримувача (абонента B), яка приймає зашифроване повідомлення та перевіряє підпис.
    encrypted_key - зашифрований ключ k
    encrypted_signature - зашифрований підпис
    recipient_private_key - приватний ключ отримувача
    sender_public_key - публічний ключ відправника
    """
    # Розшифрування ключа k
    decrypted_key = decrypt(encrypted_key, recipient_private_key)
    
    # Розшифрування підпису
    decrypted_signature = decrypt(encrypted_signature, recipient_private_key)
    
    # Перевірка підпису
    is_valid_signature = verify(decrypted_key, decrypted_signature, sender_public_key)
    
    return decrypted_key, is_valid_signature

# Демонстрація роботи протоколу
bit_length = 256
private_a, public_a, private_b, public_b = rsa_setup(bit_length)

# Випадковий ключ k для передачі
k = random.randint(1, public_b[1] - 1)

print(f"Секретний ключ для передачі: {k}")

# Відправник A формує повідомлення
encrypted_key, encrypted_signature = send_key(k, private_a, public_a, public_b)

print(f"Зашифрований ключ: {encrypted_key}")
print(f"Зашифрований підпис: {encrypted_signature}")

# Одержувач B приймає повідомлення
decrypted_key, is_valid_signature = receive_key(encrypted_key, encrypted_signature, private_b, public_a)

print(f"Розшифрований ключ: {decrypted_key}")
print(f"Підпис коректний: {is_valid_signature}")