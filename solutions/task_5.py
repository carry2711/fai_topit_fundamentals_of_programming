
students = {
    "Анна": [78, 91, 84, 88],
    "Борис": [60, 72, 68],
    "Дарья": [95, 93, 97, 90],
    "Илья": [55, 61],
}


# ---------- базовые функции ----------
def mean(values: list[int | float]) -> float:
    """Среднее арифметическое. Для пустого списка возвращает 0.0."""
    if not values:
        return 0.0
    total = 0.0
    for v in values:
        total += v
    return total / len(values)


def minimum(values: list[int | float]):
    """Минимум без min(). Для пустого списка — None."""
    if not values:
        return None
    m = values[0]
    for v in values[1:]:
        if v < m:
            m = v
    return m


def maximum(values: list[int | float]):
    """Максимум без max(). Для пустого списка — None."""
    if not values:
        return None
    m = values[0]
    for v in values[1:]:
        if v > m:
            m = v
    return m


def classify(score: float) -> str:
    """Категория по среднему баллу."""
    if score >= 90:
        return "отличный"
    if score >= 75:
        return "хороший"
    if score >= 60:
        return "удовлетворительный"
    return "недостаточный"


# ---------- сводки ----------
def student_summary(name: str, results: list[int]) -> dict:
    """Итоги одного студента."""
    if not results:
        return {
            "name": name, "mean": 0.0, "min": None, "max": None,
            "category": "нет данных",
        }
    m = mean(results)
    return {
        "name": name,
        "mean": m,
        "min": minimum(results),
        "max": maximum(results),
        "category": classify(m),
    }


def group_summary(students: dict[str, list[int]]) -> dict:
    """Общая статистика группы."""
    if not students:
        return {
            "count": 0, "group_mean": 0.0,
            "categories": {}, "summaries": [],
        }

    summaries = [student_summary(n, r) for n, r in students.items()]
    all_values = [v for r in students.values() for v in r]

    categories = {
        "отличный": 0, "хороший": 0,
        "удовлетворительный": 0, "недостаточный": 0,
    }
    for s in summaries:
        cat = s["category"]
        if cat in categories:
            categories[cat] += 1

    return {
        "count": len(students),
        "group_mean": mean(all_values),
        "categories": categories,
        "summaries": summaries,
    }


def find_top_students(students: dict[str, list[int]]) -> list[str]:
    """Студенты с наибольшим средним (может быть несколько)."""
    if not students:
        return []
    avgs = {n: mean(r) for n, r in students.items() if r}
    if not avgs:
        return []
    top_val = maximum(list(avgs.values()))
    return [n for n, v in avgs.items() if v == top_val]


def format_report(student_data: dict, group_data: dict) -> str:
    """Итоговый текстовый отчёт."""
    lines = ["=" * 40, "ОТЧЁТ ПО ГРУППЕ", "=" * 40]
    for s in student_data["summaries"]:
        lines.append(
            f"{s['name']:>8}: ср={s['mean']:6.2f}, "
            f"min={s['min']}, max={s['max']}, "
            f"категория={s['category']}"
        )
    lines.append("-" * 40)
    lines.append(f"Студентов: {student_data['count']}")
    lines.append(f"Средний балл группы: {student_data['group_mean']:.2f}")
    lines.append("Категории:")
    for k, v in student_data["categories"].items():
        lines.append(f"  {k}: {v}")
    return "\n".join(lines)


# ---------- главная ----------
def main() -> None:
    group = group_summary(students)
    print(format_report(group, None))

    print("\nЛидеры:", find_top_students(students))

    # --- Граничные сценарии ---
    print("\n--- Сценарий: один студент ---")
    print(format_report(group_summary({"Анна": [85]}), None))

    print("\n--- Сценарий: несколько лидеров ---")
    data = {"А": [90, 90], "Б": [90, 90], "В": [80]}
    print("Лидеры:", find_top_students(data))

    print("\n--- Сценарий: пустая группа ---")
    print(format_report(group_summary({}), None))

    print("\n--- Сценарий: студент без результатов ---")
    data = {"Анна": [80], "Борис": []}
    print(format_report(group_summary(data), None))

    print("\n--- Сценарий: границы категорий ---")
    for score in [59, 60, 74, 75, 89, 90, 100]:
        print(f"  {score} -> {classify(score)}")


if __name__ == "__main__":
    main()