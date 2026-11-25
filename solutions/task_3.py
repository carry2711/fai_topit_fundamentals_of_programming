# Исходные данные: список записей о сдаче лабораторных работ
# Каждый кортеж: (имя_студента, название_лабы, оценка)
submissions = [
    ("anna", "lab_01", 5),
    ("boris", "lab_01", 4),
    ("anna", "lab_02", 5),
    ("daria", "lab_01", 3),
    ("boris", "lab_02", 5),
    ("anna", "lab_01", 4),  # Анна пыталась сдать лабу 1 дважды
]


def build_structures(records: list[tuple]) -> dict:
    """
    Строит все требуемые структуры данных из списка записей.
    Проходит по списку один раз и наполняет 5 разных "полочек" для данных.
    """
    # Структура 1: Множество всех уникальных студентов
    students = set()
    # Структура 2: Множество всех уникальных лабораторных работ
    labs = set()
    # Структура 3: Словарь "студент → список всех его попыток"
    attempts = {}

    # Структура 4: Словарь лучших результатов
    # Ключ — кортеж (студент, лаба), значение — лучшая оценка
    best = {}

    # Структура 5: Словарь количества попыток
    # Ключ — кортеж (студент, лаба), значение — сколько раз пытался
    attempts_count = {}

    # Проходим по всем записям один раз
    for student, lab, score in records:
        # Добавляем студента в множество (если уже есть — не добавится)
        students.add(student)
        # Добавляем лабу в множество
        labs.add(lab)

        # Добавляем попытку в список попыток студента
        # setdefault: если ключа нет, создаёт пустой список []
        # Затем в этот список добавляем новую попытку (lab, score)
        attempts.setdefault(student, []).append((lab, score))

        # Создаём составной ключ: (студент, лаба)
        key = (student, lab)

        # Обновляем лучший результат:
        # Если ключа ещё нет ИЛИ новая оценка лучше текущей — обновляем
        if key not in best or score > best[key]:
            best[key] = score

        # Увеличиваем счётчик попыток на 1
        # get(key, 0): если ключа нет, считаем что там 0, иначе берём текущее значение
        attempts_count[key] = attempts_count.get(key, 0) + 1

    # Возвращаем все структуры в одном словаре
    return {
        "students": students,
        "labs": labs,
        "attempts": attempts,
        "best": best,
        "attempts_count": attempts_count,
    }


def students_with_both(structs: dict) -> set:
    """
    Находит студентов, которые сдавали и lab_01, и lab_02.
    Использует операции над множествами (пересечение).
    """
    # Создаём множество студентов, сдавших lab_01
    # Перебираем ключи словаря best, где lab == "lab_01"
    s1 = {st for st, lab in structs["best"] if lab == "lab_01"}

    # Создаём множество студентов, сдавших lab_02
    s2 = {st for st, lab in structs["best"] if lab == "lab_02"}

    # Находим пересечение: кто есть и в s1, и в s2
    return s1 & s2


def add_record(structs: dict, record: tuple) -> None:
    """
    Добавляет одну новую запись без полного перестроения всех структур.
    Это эффективно: мы обновляем только то, что изменилось.
    """
    student, lab, score = record

    # Добавляем студента в множество (если уже есть — не добавится)
    structs["students"].add(student)
    # Добавляем лабу в множество
    structs["labs"].add(lab)
    # Добавляем попытку в список попыток студента
    structs["attempts"].setdefault(student, []).append((lab, score))

    # Создаём составной ключ
    key = (student, lab)

    # Обновляем лучший результат, если новая оценка лучше
    if key not in structs["best"] or score > structs["best"][key]:
        structs["best"][key] = score

    # Увеличиваем счётчик попыток
    structs["attempts_count"][key] = structs["attempts_count"].get(key, 0) + 1


def handle_query(structs: dict, query: str) -> str:
    """
    Обрабатывает текстовый запрос от пользователя.
    Разбирает строку на части и выполняет соответствующую команду.
    Защищена от ошибок: не упадёт при неизвестной команде или отсутствующем ключе.
    """
    # Разбиваем строку на части по пробелам
    # "best anna lab_01" → ["best", "anna", "lab_01"]
    parts = query.strip().split()

    # Если строка пустая
    if not parts:
        return "пустой запрос"

    # Первая часть — это команда
    cmd = parts[0]

    # Оборачиваем в try/except — страховка от непредвиденных ошибок
    try:
        # Команда "student <имя>" — показать все попытки студента
        if cmd == "student" and len(parts) == 2:
            name = parts[1]
            # Проверяем, есть ли такой студент
            if name not in structs["students"]:
                return f"студент {name} не найден"
            # Возвращаем список его попыток
            return f"попытки {name}: {structs['attempts'][name]}"

        # Команда "best <студент> <лаба>" — показать лучшую оценку
        if cmd == "best" and len(parts) == 3:
            # Создаём составной ключ из частей запроса
            key = (parts[1], parts[2])
            # get(key, "нет данных"): если ключа нет, возвращаем "нет данных"
            # Это безопаснее, чем structs["best"][key], которое упало бы с ошибкой
            return str(structs["best"].get(key, "нет данных"))

        # Команда "attempts <студент> <лаба>" — показать количество попыток
        if cmd == "attempts" and len(parts) == 3:
            key = (parts[1], parts[2])
            # Если ключа нет, возвращаем 0 (студент не пытался)
            return str(structs["attempts_count"].get(key, 0))

        # Команда "completed <лаба>" — показать всех, кто сдавал эту лабу
        if cmd == "completed" and len(parts) == 2:
            lab = parts[1]
            # Создаём множество студентов, у которых есть эта лаба в best
            res = {st for (st, l) in structs["best"] if l == lab}
            # Сортируем для красивого вывода
            return str(sorted(res))

        # Если команда не распознана
        return "неизвестная команда"

    # Если произошла какая-то ошибка — ловим её и возвращаем текст
    except Exception as e:
        return f"ошибка: {e}"


def main() -> None:
    """Главная функция: строит структуры, добавляет запись, обрабатывает запросы."""

    # Строим все структуры из исходных данных
    structs = build_structures(submissions)

    # Выводим результаты
    print("Студенты:", sorted(structs["students"]))
    print("Лабы:", sorted(structs["labs"]))
    print("Лучшие результаты:", structs["best"])
    print("Число попыток:", structs["attempts_count"])
    print("Сдали обе работы:", sorted(students_with_both(structs)))

    # Добавляем новую запись
    print("\n--- Добавляем новую запись ---")
    add_record(structs, ("daria", "lab_02", 4))
    print("Обновлённые лучшие:", structs["best"])
    print("Обновлённые попытки:", structs["attempts_count"])

    # Тестируем текстовые запросы
    print("\n--- Текстовые запросы ---")
    queries = [
        "student anna",  # Все попытки Анны
        "best anna lab_01",  # Лучшая оценка Анны за лабу 1
        "attempts boris lab_02",  # Сколько раз Борис пытался сдать лабу 2
        "completed lab_01",  # Кто сдавал лабу 1
        "student unknown",  # Несуществующий студент (проверка защиты)
        "foo bar",  # Неизвестная команда (проверка защиты)
    ]

    # Обрабатываем каждый запрос и выводим результат
    for q in queries:
        print(f"{q!r:30} -> {handle_query(structs, q)}")


if __name__ == "__main__":
    main()