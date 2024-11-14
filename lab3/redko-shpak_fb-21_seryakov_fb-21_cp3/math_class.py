def extended_gcd(a, b):
    """ Розширений алгоритм Евкліда. """
    u = [1, 0]
    v = [0, 1]
    r = [a, b]
    
    i = 1
    while r[i] != 0:
        q = r[i-1] // r[i]
        r.append(r[i-1] - q * r[i])
        u.append(u[i-1] - q * u[i])
        v.append(v[i-1] - q * v[i])
        i += 1

    return r[i-1], u[i-1], v[i-1]

def mod_inverse(a, m):
    """ Знаходить мультиплікативний обернений елемент a^1 mod m. """
    d, u, v = extended_gcd(a, m)

    if d != 1:
        return None
    
    return u % m

def solve_linear_congruence(a, b, n):
    """ Розв'язує лінійне порівняння ax == b (mod n). """
    d, u, v = extended_gcd(a, n)
    
    if b % d != 0:
        return []
    
    if d > 1:
        a_1 = a // d
        b_1 = b // d
        n_1 = n // d
        a_1_inv = mod_inverse(a_1, n_1)
        x_0 = (a_1_inv * b_1) % n_1

        return [(x_0 + i * n_1) % n for i in range(d)]

    a_inv = mod_inverse(a, n)
    return [(a_inv * b) % n]

def test_math_utils():
    # тестую розширеий алгоритм Евкліда
    d, u, v = extended_gcd(30, 18)
    assert d == 6  # НСД(30,18) = 6
    assert 30*u + 18*v == 6  # перевіряємо лінійне представлення
    
    # тестую знаходження оберненого елемента
    assert mod_inverse(7, 31) == 9  # 7 * 9 == 1 (mod 31)
    assert mod_inverse(15, 961) is not None  # має існувати для афінного шифру
    
    # тестую розв'язання лінійних порівнянь
    solutions = solve_linear_congruence(6, 3, 9)
    assert len(solutions) == 3  # має бути 3 розв'язки
    for x in solutions:
        assert (6 * x - 3) % 9 == 0  # перевіряємо кожнен розв'язок
    
    print("всі тести пройдено успішно!")

if __name__ == "__main__":
    test_math_utils()