def classify_score(score: int) -> str:
    """Возвращает базовый уровень по баллу."""
    if score >= 90:
        return "отличный"
    if score >= 75:
        return "хороший"
    if score >= 60:
        return "удовлетворительный"
    return "недостаточный"


def downgrade(level: str) -> str:
    """Снижает уровень на одну ступень, не ниже 'недостаточный'."""
    order = ["отличный", "хороший", "удовлетворительный", "недостаточный"]
    idx = order.index(level)
    if idx + 1 < len(order):
        return order[idx + 1]
    return level


def describe_work(work_type: str) -> str:
    """Пояснение для типа работы через match/case."""
    match work_type:
        case "exam":
            return "экзаменационная работа"
        case "project":
            return "проектная работа"
        case "practice":
            return "практическая работа"
        case _:
            return "неизвестный тип работы"


def process_record(score: int, work_type: str, absences: int) -> str:
    """Обрабатывает одну запись и возвращает строку результата."""
    if not (0 <= score <= 100):
        return f"[ошибка] балл {score} вне диапазона 0..100"
    if not (0 <= absences <= 5):
        return f"[ошибка] пропуски {absences} вне диапазона 0..5"

    level = classify_score(score)
    if absences > 3:
        level = downgrade(level)

    work_desc = describe_work(work_type)
    return f"балл={score}, пропуски={absences} → уровень: {level} ({work_desc})"


def main() -> None:
    # --- Часть 4: тестовые сценарии (границы диапазонов) ---
    test_cases = [
        (0,   "exam",    0),
        (59,  "practice",1),
        (60,  "project", 2),
        (74,  "exam",    3),
        (75,  "practice",4),   # пропуски > 3 → понижение
        (89,  "project", 5),   # пропуски > 3 → понижение
        (90,  "exam",    0),
        (100, "practice",3),
        (101, "exam",    0),   # некорректный балл
        (50,  "unknown", 0),   # неизвестный тип
    ]

    print("=== Тестовые сценарии ===")
    for sc in test_cases:
        print(process_record(*sc))

    # --- Практическое расширение ---
    print("\n=== Обработка списка студентов ===")
    records = [
        (92, "exam", 1), (78, "project", 2), (65, "practice", 4),
        (55, "exam", 0), (88, "project", 5), (70, "practice", 1),
        (45, "exam", 2), (95, "project", 0), (82, "practice", 3),
        (60, "exam", 4), (73, "project", 0),
    ]

    results = [process_record(*r) for r in records]
    for r in results:
        print(r)

    # Подсчёт по уровням (вручную, без list.count)
    levels = {
        "отличный": 0, "хороший": 0,
        "удовлетворительный": 0, "недостаточный": 0,
        "ошибка": 0,
    }
    for i, r in enumerate(records):
        line = results[i]
        if "[ошибка]" in line:
            levels["ошибка"] += 1
        else:
            for key in levels:
                if f"уровень: {key}" in line:
                    levels[key] += 1
                    break

    print("\n=== Итоговая сводка ===")
    for k, v in levels.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()