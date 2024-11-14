import random
import math

YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Функція для перевірки числа на простоту за допомогою тесту Міллера-Рабіна
def is_prime_miller_rabin(p, k=10):
    if p < 2 or p % 2 == 0:
        return p == 2

    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    for prime in small_primes:
        if p % prime == 0 and p != prime:
            return False

    s = 0
    d = p - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    def check_composite(a):
        x = pow(a, d, p)
        if x == 1 or x == p - 1:
            return False
        for _ in range(s - 1):
            x = pow(x, 2, p)
            if x == p - 1:
                return False
        return True

    for _ in range(k):
        a = random.randint(2, p - 2)
        if math.gcd(a, p) != 1 or check_composite(a):
            return False

    return True

# Функція для пошуку випадкового простого числа з заданого інтервалу
def find_random_prime(start, end, k=10):
    attempts = 0
    while attempts < 1000:
        candidate = random.randint(start, end)
        if is_prime_miller_rabin(candidate, k):
            return candidate
        attempts += 1
    return None

# Функція для генерації випадкового простого числа довжини щонайменше n біт
def generate_prime(bits, k=10):
    while True:
        candidate = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_prime_miller_rabin(candidate, k):
            return candidate

# Функція для генерації двох пар простих чисел
def generate_prime_pairs(bits=256):
    while True:
        # Генерація простих чисел для абонента A
        p = generate_prime(bits)
        q = generate_prime(bits)
        pq = p * q

        # Генерація простих чисел для абонента B
        p1 = generate_prime(bits)
        q1 = generate_prime(bits)
        p1q1 = p1 * q1

        if pq <= p1q1:
            return (p, q), (p1, q1)

# Функція для розширеного алгоритму Евкліда
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

# Функція для знаходження оберненого елемента
def mod_inverse(e, phi):
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("Обернений елемент не існує.")
    return x % phi

# Функція для генерації ключової пари RSA
def generate_rsa_key_pair(bits=256):
    # Генерація простих чисел p і q
    p = generate_prime(bits)
    q = generate_prime(bits)

    # Обчислення n та функції Ойлера phi(n)
    n = p * q
    phi = (p - 1) * (q - 1)

    # Вибір відкритого експонента e
    e = 2**16 + 1
    if math.gcd(e, phi) != 1:
        raise ValueError("Невдалий вибір e, знайдено спільний дільник з phi.")

    # Обчислення секретного експонента d
    d = mod_inverse(e, phi)

    # Повернення ключів
    public_key = (e, n)
    private_key = (d, p, q)

    return public_key, private_key

# Функція для генерації ключових пар для абонентів A і B
def generate_rsa_keys_for_users(bits=256):
    # Генерація ключів для абонента A
    public_key_a, private_key_a = generate_rsa_key_pair(bits)

    # Генерація ключів для абонентів B
    public_key_b, private_key_b = generate_rsa_key_pair(bits)

    return (public_key_a, private_key_a), (public_key_b, private_key_b)

def main():
    while True:
        print(YELLOW + "\n♥Меню♥" + RESET)
        print("1. Вибір випадкового простого числа")
        print("2. Генерація двох пар простих чисел")
        print("3. Генерація ключових пар RSA для абонентів A та B")
        print("4. ...")
        print("5. ...")
        print("6. Вийти")
        user_choice = input("Виберіть опцію: ").strip()
        if user_choice == '6':
            print(BLUE + " /}___/}❀\n( • . •)\n/ >    > Byeee" + RESET)
            break
        if user_choice == '1':
            start_interval = 2
            end_interval = 10 ** 4
            random_prime = find_random_prime(start_interval, end_interval)
            if random_prime:
                print(f"Випадкове просте число з інтервалу [{start_interval}, {end_interval}]: {random_prime}")
            else:
                print(f"Просте число не знайдено в інтервалі [{start_interval}, {end_interval}].")
        elif user_choice == '2':
            bits = 256
            (p, q), (p1, q1) = generate_prime_pairs(bits)
            print(f"Пара простих чисел для абонента A: p = {p}, q = {q}")
            print(f"Пара простих чисел для абонента B: p1 = {p1}, q1 = {q1}")
        elif user_choice == '3':
            bits = 256
            (public_a, private_a), (public_b, private_b) = generate_rsa_keys_for_users(bits)
            print(f"Відкритий ключ абонента A: {public_a}")
            print(f"Секретний ключ абонента A: {private_a}")
            print(f"Відкритий ключ абонента B: {public_b}")
            print(f"Секретний ключ абонента B: {private_b}")
        elif user_choice == '4':
            print("краказябра")
        elif user_choice == '5':
            print("краказябра")
        else:
            print("Неправильний вибір. Спробуйте знову.")

if __name__ == "__main__":
    main()
