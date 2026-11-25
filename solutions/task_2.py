measurements = [12, 15, 11, 18, 18, 9, 21, 15, 7, 18]


# ---------- Один проход: сумма, min, max, чётные ----------
def single_pass_stats(data: list[int]) -> dict:
    """За один проход считает сумму, min, max и количество чётных."""
    if not data:
        return {"sum": 0, "min": None, "max": None, "even": 0}

    total = 0
    mn = data[0]
    mx = data[0]
    even = 0

    for x in data:
        total += x
        if x < mn:
            mn = x
        if x > mx:
            mx = x
        if x % 2 == 0:
            even += 1

    return {"sum": total, "min": mn, "max": mx, "even": even}


# ---------- Второй проход: больше среднего ----------
def count_above_average(data: list[int], average: float) -> int:
    """Считает элементы, строго большие среднего."""
    cnt = 0
    for x in data:
        if x > average:
            cnt += 1
    return cnt


# ---------- Линейный поиск ----------
def linear_search(data: list[int], target: int) -> tuple[int, int]:
    """Возвращает (индекс, число_сравнений). Если нет — (-1, ...)."""
    comparisons = 0
    for i, x in enumerate(data):
        comparisons += 1
        if x == target:
            return i, comparisons
    return -1, comparisons


# ---------- Простое число (до sqrt) ----------
def is_prime(n: int) -> bool:
    """Проверяет простоту перебором делителей до sqrt(n)."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


# ---------- Сортировка выбором ----------
def selection_sort(data: list[int]) -> tuple[list[int], int]:
    """Возвращает (отсортированный_список, число_сравнений)."""
    a = data[:]
    n = len(a)
    comparisons = 0
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a, comparisons


# ---------- Бинарный поиск ----------
def binary_search(data: list[int], target: int) -> tuple[int, int]:
    """Возвращает (индекс, число_сравнений)."""
    lo, hi = 0, len(data) - 1
    comparisons = 0
    while lo <= hi:
        comparisons += 1
        mid = (lo + hi) // 2
        if data[mid] == target:
            return mid, comparisons
        if data[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, comparisons


def main() -> None:
    print("measurements =", measurements)

    stats = single_pass_stats(measurements)
    print(f"сумма={stats['sum']}, min={stats['min']}, "
          f"max={stats['max']}, чётных={stats['even']}")

    avg = stats["sum"] / len(measurements)
    print(f"среднее={avg:.2f}")
    above = count_above_average(measurements, avg)
    print(f"больше среднего: {above}")

    # Линейный поиск
    target = int(input("Введите число для линейного поиска: ") or 15)
    idx, cmp_lin = linear_search(measurements, target)
    print(f"линейный поиск {target}: индекс={idx}, сравнений={cmp_lin}")

    # Простое число
    for n in [1, 2, 17, 25, 97, 100]:
        print(f"{n} простое? {is_prime(n)}")

    # Сравнение сортировки + поиска
    print("\n=== Сравнение линейного и бинарного поиска ===")
    print(f"{'N':>6} | {'линейный':>10} | {'бинарный':>10}")
    for n in [10, 100, 1000]:
        arr = list(range(n))
        target = n - 1  # худший случай
        _, cmp_lin = linear_search(arr, target)
        sorted_arr, _ = selection_sort(arr)
        _, cmp_bin = binary_search(sorted_arr, target)
        print(f"{n:>6} | {cmp_lin:>10} | {cmp_bin:>10}")


if __name__ == "__main__":
    main()