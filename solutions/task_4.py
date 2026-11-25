
# ---------- 1. arithmetic_mean ----------
# Функция вычисляет среднее арифметическое списка чисел.
# Контракт: принимает список, возвращает float.
def arithmetic_mean(values: list[float]) -> float:
    """Возвращает среднее арифметическое непустого списка."""
    # Ранний return: если список пустой, сразу возвращаем 0.0
    # Это спасает от деления на ноль и делает код плоским
    if not values:
        return 0.0

    # Считаем сумму вручную
    total = 0.0
    for v in values:
        total += v

    # Делим сумму на количество элементов
    return total / len(values)


# Проверки через assert: если условие ложно, программа упадёт с AssertionError
# Это способ убедиться, что функция работает корректно
assert arithmetic_mean([1, 2, 3]) == 2.0  # (1+2+3)/3 = 2.0
assert arithmetic_mean([10]) == 10.0  # 10/1 = 10.0
assert arithmetic_mean([]) == 0.0  # пустой список → 0.0


# ---------- 2. normalize_name ----------
# Функция чистит имя: убирает лишние пробелы и приводит к правильному регистру.
def normalize_name(name: str) -> str:
    # Ранний return: если строка пустая или состоит только из пробелов
    if not name or not name.strip():
        return ""

    # .strip() убирает пробелы с краёв
    # .split() без аргументов — "умный": режет по любому количеству пробелов
    parts = name.strip().split()

    # .capitalize() делает первую букву заглавной, остальные — строчными
    # " ".join(...) склеивает список обратно в строку через один пробел
    return " ".join(p.capitalize() for p in parts)


assert normalize_name("  anna   maria  ") == "Anna Maria"
assert normalize_name("IVAN") == "Ivan"
assert normalize_name("   ") == ""


# ---------- 3. build_report ----------

def build_report(
        student: str,
        results: list[int],
        *,  # ← всё после * — только именованные
        precision: int = 2,  # количество знаков после запятой
        prefix: str = "Результат",  # префикс строки
) -> str:
    # Ранний return: если список результатов пустой
    if not results:
        return f"{prefix}: {student} — нет данных"

    # Вычисляем средний балл
    avg = arithmetic_mean(results)

    # Формируем строку с нужным количеством знаков после запятой
    # {avg:.{precision}f} — форматирование с динамической точностью
    return f"{prefix}: {student} — средний балл {avg:.{precision}f}"


# Проверки:
assert build_report("Anna", [80, 90]) == "Результат: Anna — средний балл 85.00"
assert build_report("Anna", [80, 90], precision=0) == "Результат: Anna — средний балл 85"
assert build_report("Anna", [], prefix="Итог") == "Итог: Anna — нет данных"


# ---------- 4. collect_tags ----------
# Функция принимает произвольное число тегов и возвращает кортеж уникальных тегов.
# *tags означает: "собери все позиционные аргументы в кортеж".
# lowercase — именованный параметр (после *), поэтому передаётся только по имени.
def collect_tags(*tags: str, lowercase: bool = True) -> tuple[str, ...]:
    """Возвращает очищенные теги без пустых значений и повторов."""
    # Множество для отслеживания уже встреченных тегов
    # Проверка "if cleaned not in seen" работает за O(1)
    seen: set[str] = set()

    # Список для сохранения порядка (множество не сохраняет порядок)
    out: list[str] = []

    for t in tags:
        if not isinstance(t, str):
            continue
        # Убираем пробелы с краёв
        cleaned = t.strip()
        # Пропускаем пустые строки
        if not cleaned:
            continue
        # Если нужно, приводим к нижнему регистру
        if lowercase:
            cleaned = cleaned.lower()
        # Добавляем только если ещё не встречали (убираем повторы)
        if cleaned not in seen:
            seen.add(cleaned)
            out.append(cleaned)

    # Возвращаем кортеж
    return tuple(out)


assert collect_tags("Python", "python", "  ") == ("python",)
assert collect_tags("A", "B", lowercase=False) == ("A", "B")
assert collect_tags() == ()


def demo_unpack() -> None:
    # Позиционные аргументы в списке
    args = ["Anna", [80, 90, 100]]
    # Именованные аргументы в словаре
    kwargs = {"precision": 1, "prefix": "Отчёт"}

    # *args разворачивает список в позиционные аргументы:
    # build_report("Anna", [80, 90, 100], precision=1, prefix="Отчёт")
    # **kwargs разворачивает словарь в именованные аргументы
    print(build_report(*args, **kwargs))

    # Аналогично для collect_tags:
    # *tags разворачивает список в отдельные аргументы
    tags = ["Python", "AI", "python", "  "]
    print(collect_tags(*tags, lowercase=True))


# ---------- LEGB: nonlocal ----------
# LEGB — это порядок, в котором Python ищет переменную по имени:
# L (Local) → E (Enclosing) → G (Global) → B (Built-in)

course = "Python"  # G — глобальная переменная (на уровне модуля)

def outer():
    # E — локальная для outer, но объёмлющая для inner
    course = "Advanced Python"

    def inner():
        nonlocal course
        # Меняем переменную из outer, а не глобальную
        course = "Inner: " + course

    inner()
    return course


print("LEGB demo:")
print("  global course =", course)  # → Python
print("  after outer() =", outer())  # → Inner: Advanced Python
print("  global course после =", course)  # → Python (не изменилась!)
# Вывод: nonlocal поднимается только на один уровень (в E), а не до G


def add_result_broken(value, results=[]):
    results.append(value)
    return results


def add_result_fixed(value, results=None):
    # Если results не передан (None), создаём НОВЫЙ список
    if results is None:
        results = []  # новый список на каждый вызов
    results.append(value)
    return results


print("\n--- mutable default ---")
print(add_result_broken(1))  # [1]
print(add_result_broken(2))  # [1, 2] ← ОШИБКА! ожидалось [2]
# Список "помнит" все предыдущие вызовы, потому что он общий

print(add_result_fixed(1))  # [1]
print(add_result_fixed(2))  # [2]  ← правильно, каждый раз новый список


# ---------- Практическое расширение ----------
# Функции высшего порядка: функции могут принимать другие функции как аргументы.

def apply_to_results(operation, values):
    """Применяет operation к каждому элементу values."""
    # operation — это функция, которую нам передали
    # Мы не знаем, что именно она делает, просто вызываем её для каждого элемента
    return [operation(v) for v in values]


# Фабрика функций: функция, которая создаёт и возвращает другую функцию.
def make_threshold_checker(threshold):
    """Фабрика: возвращает функцию, проверяющую, что результат >= threshold."""

    # Внутренняя функция, которая "замыкает" переменную threshold
    def checker(value):
        return value >= threshold

    # Возвращаем функцию (не вызываем её, а возвращаем как объект)
    return checker


print("\n--- apply_to_results ---")
# Передаём lambda-функцию (анонимная функция)
print(apply_to_results(lambda x: x * 2, [1, 2, 3]))  # → [2, 4, 6]

# Передаём именованную функцию
print(apply_to_results(arithmetic_mean, [[1, 2], [10, 20]]))  # → [1.5, 15.0]

# Создаём две независимые проверки с разными порогами
check_50 = make_threshold_checker(50)
check_80 = make_threshold_checker(80)

# Каждая функция "помнит" свой threshold благодаря замыканию
print("check_50(60) =", check_50(60))  # True (60 >= 50)
print("check_80(60) =", check_80(60))  # False (60 >= 80)

# В замыкании сохраняется значение threshold, переданное при создании функции.

if __name__ == "__main__":
    demo_unpack()