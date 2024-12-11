import random

# Алгоритм Евкліда для знаходження найбільшого спільного дільника (gcd)
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Оптимізована функція для обчислення функції Ейлера φ(n) для n = p * q
def phi_optimized(p, q):
    return (p - 1) * (q - 1)

# Зворотне значення за модулем
def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

# Функція для піднесення до степеня за модулем із використанням схеми Горнера
def modular_exponentiation(base, exponent, mod):
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exponent //= 2
    return result

# Генерація e, яке задовольняє умови для RSA
# def generate_e(phi_n):
#     e = random.randint(2, phi_n - 1)
#     while gcd(e, phi_n) != 1:
#         e = random.randint(2, phi_n - 1)
#     return e

# Функція RSA_GEN
def RSA_GEN(p, q, e):
    n = p * q
    phi_n = phi_optimized(p, q)
    d = mod_inverse(e, phi_n)
    if (e * d) % phi_n == 1:
        print(f"Коректно: e * d = 1 mod φ(n) для e = {e}, d = {d}")
    else:
        print(f"Помилка: e * d != 1 mod φ(n) для e = {e}, d = {d}")
    return n, e, d

# Шифрування повідомлення
def encrypt_message(m, e, n):
    return modular_exponentiation(m, e, n)

# Розшифрування повідомлення
def decrypt_message(c, d, n):
    return modular_exponentiation(c, d, n)

# Створення цифрового підпису
def create_signature(m, d, n):
    return modular_exponentiation(m, d, n)

# Перевірка цифрового підпису
def verify_signature(s, e, n):
    return modular_exponentiation(s, e, n)

# Задані прості числа
p = 36646164541686624240937833154972327964008617161515222144838114780214993351409
q = 31539962308096287988814609326825756936315439947047156766760061841746726548927
p1 = 73431616661604875049686928558414853172421655489331888049826565905174368641603
q1 = 82976583645640818895092178503362825123374069319439494124111219775406714256373
e = 65537

# Генерація ключів для A
n, e, d = RSA_GEN(p, q, e)
print(f"Для A: n = {n}, \ne = {e}, \nd = {d}\n")

# Генерація ключів для B
n1, e1, d1 = RSA_GEN(p1, q1, e)
print(f"Для B: n1 = {n1}, \ne1 = {e1}, \nd1 = {d1}\n")
print("\n" , "="*300, "\n")

# Створення відкритого повідомлення
M = random.randint(1, n - 1)
M1 = random.randint(1, n1 - 1)

print(f"Повідомлення для A: M = {M}")

# Шифрування повідомлення для A
C = encrypt_message(M, e, n)
print(f"Зашифроване повідомлення для A: C = {C}")

# Розшифрування повідомлення для A
M_dec = decrypt_message(C, d, n)
print(f"Розшифроване повідомлення для A: M = {M_dec}")

# Цифровий підпис для A
S = create_signature(M, d, n)
print(f"Цифровий підпис для A: S = {S}")

# Перевірка цифрового підпису для A
M_verify = verify_signature(S, e, n)
print(f"Перевірка підпису для A: M = {M_verify}")

print(f"\nПовідомлення для B: M1 = {M1}")

# Шифрування повідомлення для B
C1 = encrypt_message(M1, e1, n1)
print(f"Зашифроване повідомлення для B: C1 = {C1}")

# Розшифрування повідомлення для B
M1_dec = decrypt_message(C1, d1, n1)
print(f"Розшифроване повідомлення для B: M1 = {M1_dec}")

# Цифровий підпис для B
S1 = create_signature(M1, d1, n1)
print(f"Цифровий підпис для B: S1 = {S1}")

# Перевірка цифрового підпису для B
M1_verify = verify_signature(S1, e1, n1)
print(f"Перевірка підпису для B: M1 = {M1_verify}")

print("\n" , "="*300, "\n")

#Повідомлення згенероване рандомно
k = 1138871245103717467790293341541266222372696957810768120515208988767366165699249917157999604271883662770956240389270967991142452518801509339383355463954446
print (f"Повідомлення, k = {k}")

# Цифровий підпис для A
s = create_signature(k, d, n)
print(f"Цифровий підпис для A: S = {s}")

#Передача абоненту B k1, s1
k1 = encrypt_message(k, e1, n1)
s1 = encrypt_message(s, e1, n1)
print(f"Абонент А формує повідомлення k1, s1 і відправляє його B \n k1 = {k1} \n S1 = {s1}")

print("\n" , "-"*300, "\n")

#Абонент B знаходить ключ за допомогою свого d1
k = create_signature(k1, d1, n1)
s = create_signature(s1, d1, n1)
print(f"Абонент B за допомогою свого секретного ключа d1 знаходить (конфіденційність): \n k = {k} \n S = {s}")

s = create_signature(k, d, n)
k = verify_signature(s, e, n)
print(f"І за допомогою відкритого ключа e абонента А перевіряє підпис А (автентифікація): k = {k}")