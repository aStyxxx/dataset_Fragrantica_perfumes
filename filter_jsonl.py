import json

input_file = r"C:\Users\pinel\.cache\kagglehub\datasets\ledecanteur\fragrantica-perfumes\versions\3\perfumes.jsonl"
output_file = "perfumes_actual.jsonl"

# Мінімальна кількість відгуків/голосів
min_votes = 50


def get_votes_count(record):
    """Шукає кількість голосів/відгуків у структурі запису"""
    # 1. Якщо є rating
    r = record.get("rating")
    if isinstance(r, dict):
        for k in ["votes", "count", "total", "reviews_count", "rating_count"]:
            if k in r and r[k] is not None:
                try:
                    return int(float(r[k]))
                except (ValueError, TypeError):
                    pass
    elif isinstance(r, (int, float)):
        return int(r)

    # 2. Якщо є popularity
    p = record.get("popularity")
    if isinstance(p, dict):
        for k in ["votes", "count", "magnitude"]:
            if k in p and p[k] is not None:
                try:
                    return int(float(p[k]))
                except (ValueError, TypeError):
                    pass

    # 3. Перевірка верхньорівневих полів
    for k in ["vote_count", "votes", "reviews_count", "rating_count"]:
        if k in record and record[k] is not None:
            try:
                return int(float(record[k]))
            except (ValueError, TypeError):
                pass

    return 0


def is_valid_field(val):
    """Перевіряє, що список або словник нот/акордів не порожній"""
    if not val:
        return False
    if isinstance(val, str):
        return val.strip().lower() not in ["", "none", "null", "[]", "{}"]
    if isinstance(val, (list, dict)):
        return len(val) > 0
    return True


total_count = 0
saved_count = 0

print("Фільтрація датасету (зберігаємо повну структуру)...")

with open(input_file, "r", encoding="utf-8") as infile, open(
    output_file, "w", encoding="utf-8"
) as outfile:

    for line in infile:
        if not line.strip():
            continue
        total_count += 1

        record = json.loads(line)

        # 1. Фільтр: наявність акордів
        if not is_valid_field(record.get("accords")):
            continue

        # 2. Фільтр: наявність нот
        if not is_valid_field(record.get("notes")):
            continue

        # 3. Фільтр: мінімальна кількість відгуків
        votes = get_votes_count(record)
        if votes < min_votes:
            continue

        # Записуємо ОРИГІНАЛЬНИЙ рядок без жодних змін структури
        outfile.write(line.strip() + "\n")
        saved_count += 1

print(f"Всього оброблено: {total_count:,}")
print(f"Збережено якісних парфумів: {saved_count:,}")
print(f"Файл збережено: {output_file}")