import timeit

def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    lps = compute_lps(pattern)
    i = j = 0

    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == len(pattern):
            return i - j  # Pattern found at index (i - j)
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return -1  # Pattern not found



def build_shift_table(pattern):
    table = {}
    for i, char in enumerate(pattern):
        table[char] = i
    return table

def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    m = len(pattern)
    n = len(text)
    i = m - 1

    while i < n:
        j = m - 1
        while j >= 0 and pattern[j] == text[i - (m - 1 - j)]:
            j -= 1
        if j < 0:
            return i - (m - 1)  # Pattern found at index (i - (m - 1))
        else:
            shift = shift_table.get(text[i], -1)
            i += max(1, j - shift)

    return -1  # Pattern not found


def rabin_karp_search(text, pattern):
    d = 256
    q = 101
    m = len(pattern)
    n = len(text)
    h = pow(d, m-1, q)
    p_hash = 0
    t_hash = 0

    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q

    for i in range(n - m + 1):
        if p_hash == t_hash:
            if text[i:i+m] == pattern:
                return i
        if i < n - m:
            t_hash = (d * (t_hash - ord(text[i]) * h) + ord(text[i+m])) % q
            t_hash = (t_hash + q) % q

    return -1  # Pattern not found

with open("article1.txt", "r", encoding="utf-8") as f:
    text1 = f.read()

with open("article2.txt", "r", encoding="utf-8") as f:
    text2 = f.read()

    # існуючі підрядки (є в текстах)
existing1 = "алгоритм"
existing2 = "рекомендаційної системи"

# вигадані підрядки (немає в текстах)
fake1 = "qwerty123"
fake2 = "абвгдеж"

# Перевірка існуючих підрядків
print("KMP Search:")
print(f"'{existing1}' in text1: {kmp_search(text1, existing1) != -1}")
print(f"'{existing2}' in text2: {kmp_search(text2, existing2) != -1}")

# Перевірка вигаданих підрядків
print("\nKMP Search (Fake Patterns):")
print(f"'{fake1}' in text1: {kmp_search(text1, fake1) != -1}")
print(f"'{fake2}' in text2: {kmp_search(text2, fake2) != -1}")


# Стаття 1 - існуючий підрядок
t1_kmp = timeit.timeit(lambda: kmp_search(text1, existing1), number=100)
t1_bm = timeit.timeit(lambda: boyer_moore_search(text1, existing1), number=100)
t1_rk = timeit.timeit(lambda: rabin_karp_search(text1, existing1), number=100)

print("Стаття 1 - існуючий підрядок:")
print(f"KMP:        {t1_kmp:.4f} сек")
print(f"Боєр-Мур:  {t1_bm:.4f} сек")
print(f"Рабін-Карп: {t1_rk:.4f} сек")

# Стаття 1 - вигаданий підрядок
t1_kmp_f = timeit.timeit(lambda: kmp_search(text1, fake1), number=100)
t1_bm_f = timeit.timeit(lambda: boyer_moore_search(text1, fake1), number=100)
t1_rk_f = timeit.timeit(lambda: rabin_karp_search(text1, fake1), number=100)

print("\nСтаття 1 - вигаданий підрядок:")
print(f"KMP:        {t1_kmp_f:.4f} сек")
print(f"Боєр-Мур:  {t1_bm_f:.4f} сек")
print(f"Рабін-Карп: {t1_rk_f:.4f} сек")

# Стаття 2 - існуючий підрядок
t2_kmp = timeit.timeit(lambda: kmp_search(text2, existing2), number=100)
t2_bm = timeit.timeit(lambda: boyer_moore_search(text2, existing2), number=100)
t2_rk = timeit.timeit(lambda: rabin_karp_search(text2, existing2), number=100)

# Стаття 2 - вигаданий підрядок
t2_kmp_f = timeit.timeit(lambda: kmp_search(text2, fake2), number=100)
t2_bm_f = timeit.timeit(lambda: boyer_moore_search(text2, fake2), number=100)
t2_rk_f = timeit.timeit(lambda: rabin_karp_search(text2, fake2), number=100)

print("\nСтаття 2 - вигаданий підрядок:")
print(f"KMP:        {t2_kmp_f:.4f} сек")
print(f"Боєр-Мур:  {t2_bm_f:.4f} сек")
print(f"Рабін-Карп: {t2_rk_f:.4f} сек")

print("\nСтаття 2 - існуючий підрядок:")
print(f"KMP:        {t2_kmp:.4f} сек")
print(f"Боєр-Мур:  {t2_bm:.4f} сек")
print(f"Рабін-Карп: {t2_rk:.4f} сек")


print("\n" + "="*50)
print("ПІДСУМКОВА ТАБЛИЦЯ")
print("="*50)
print(f"{'Алгоритм':<15} {'С1 існ':>8} {'С1 виг':>8} {'С2 існ':>8} {'С2 виг':>8}")
print("-"*50)
print(f"{'KMP':<15} {t1_kmp:>8.4f} {t1_kmp_f:>8.4f} {t2_kmp:>8.4f} {t2_kmp_f:>8.4f}")
print(f"{'Боєр-Мур':<15} {t1_bm:>8.4f} {t1_bm_f:>8.4f} {t2_bm:>8.4f} {t2_bm_f:>8.4f}")
print(f"{'Рабін-Карп':<15} {t1_rk:>8.4f} {t1_rk_f:>8.4f} {t2_rk:>8.4f} {t2_rk_f:>8.4f}")
print("="*50)

