import timeit
import os


# 1. Алгоритм Кнута-Морріса-Пратта (KMP)
def compute_lps(pattern: str) -> int:
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


def kmp_search(main_string: str, pattern: str) -> int:
    M = len(pattern)
    N = len(main_string)
    lps = compute_lps(pattern)
    i = j = 0
    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        if j == M:
            return i - j  # Знайдено входження
        elif i < N and pattern[j] != main_string[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1


# 2. Алгоритм Боєра-Мура (Спрощений, використовує таблицю зсувів)
def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for i in range(length - 1):
        table[pattern[i]] = length - 1 - i
    return table


def boyer_moore_search(main_string, pattern):
    shift_table = build_shift_table(pattern)
    M = len(pattern)
    N = len(main_string)
    i = 0
    while i <= N - M:
        j = M - 1
        while j >= 0 and main_string[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i  # Знайдено входження

        # Зсув на основі символу тексту, який спричинив неспівпадіння
        # Якщо символу немає в таблиці, зсуваємо на довжину патерну
        shift = shift_table.get(main_string[i + M - 1], M)
        i += shift
    return -1


# 3. Алгоритм Рабіна-Карпа
def rabin_karp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)
    base = 256
    modulus = 101  # Просте число
    pattern_hash = 0
    current_hash = 0
    h = 1

    # Обчислення значення h = pow(base, M-1) % modulus
    for i in range(M - 1):
        h = (h * base) % modulus

    # Обчислення хешу для патерну і першого вікна тексту
    for i in range(M):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % modulus
        current_hash = (base * current_hash + ord(main_string[i])) % modulus

    for i in range(N - M + 1):
        if pattern_hash == current_hash:
            # Якщо хеші співпадають, перевіряємо символи
            if main_string[i:i + M] == pattern:
                return i

        if i < N - M:
            current_hash = (base * (current_hash - ord(main_string[i]) * h) + ord(main_string[i + M])) % modulus
            if current_hash < 0:
                current_hash += modulus
    return -1


# --- Функція для читання файлу ---
def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Файл {filepath} не знайдено.")
        return ""


def main():
    script_dir = os.path.dirname(__file__)
    file1_path = os.path.join(script_dir, "data/file1.txt")
    file2_path = os.path.join(script_dir, "data/file2.txt")

    text1 = read_file(file1_path)
    if not text1:
        return

    text2 = read_file(file2_path)
    if not text2:
        return

    # Реальний підрядок (беремо з середини тексту)
    existing_sub1 = "if (previousStep == Math.min(jumpStep, arrayLength));"
    existing_sub2 = "Крок 6. Здійснюється пошук усіх сесій, вподобання яких мають перетин із вподобаннями контрольної сесії. На цьому етапі є можливість відфільтрувати сесії за розміром перетину."

    # Вигаданий підрядок
    fake_sub = "fake substring for the test 123 xyz"

    patterns = [
        ("Text 1 (Real)", text1, existing_sub1, "file1.txt"),
        ("Text 1 (Fake)", text1, fake_sub, "file1.txt"),
        ("Text 2 (Real)", text2, existing_sub2, "file2.txt"),
        ("Text 2 (Fake)", text2, fake_sub, "file2.txt"),
    ]

    algorithms = [
        ("Boyer-Moore", boyer_moore_search),
        ("KMP", kmp_search),
        ("Rabin-Karp", rabin_karp_search),
    ]

    print(f"\n{'Algorithm':<15} | {'Scenario':<15} | {'Time (sec)':<15}")
    print("-" * 60)

    results = {}
    for scenario_name, text, pattern, f_name in patterns:
        for alg_name, func in algorithms:
            # для быльшої точності виконаємо пошук 100 раз
            time = timeit.timeit(lambda: func(text, pattern), number=100)
            print(f"{alg_name:<15} | {scenario_name:<15} | {time:.5f}")

            if f_name not in results:
                results[f_name] = {}
            if alg_name not in results[f_name]:
                results[f_name][alg_name] = 0
            results[f_name][alg_name] += time

        print(f"{"":<15} | {"":<15} |")

    print("-" * 60)
    print("Results")
    print("-" * 60)

    for text_key, alg_times in results.items():
        fastest_alg = min(alg_times, key=alg_times.get)
        print(f"For {text_key} faster alghoritm: {fastest_alg}")
    print("-" * 60)


if __name__ == "__main__":
    main()
