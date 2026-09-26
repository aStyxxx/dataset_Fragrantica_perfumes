import pandas as pd

# 1. Шлях до завантаженого файлу (префікс r запобігає помилкам зі слешами у Windows)
file_path = r"C:\Users\pinel\.cache\kagglehub\datasets\ledecanteur\fragrantica-perfumes\versions\3\perfumes.csv"

print("1. Зчитування даних з perfumes.csv (це може зайняти кілька секунд)...")
df = pd.read_csv(file_path, low_memory=False)
print(f"Початкова кількість ароматів: {len(df):,}")

# 2. Фільтрація неактуальних ароматів
print("2. Фільтрація ароматів...")

# А. Відсіюємо невідомі/рідкісні парфуми: мінімум 50 оцінок
# (Якщо база вийде завеликою — можна підняти поріг до 100 або 200)
min_votes = 50
filtered_df = df[df["vote_count"] >= min_votes].copy()

# Б. Тільки сучасні аромати (наприклад, від 2000 року і новіші)
filtered_df = filtered_df[filtered_df["year"] >= 2000]

# В. Прибираємо «биті» рядки, де взагалі немає піраміди акордів
filtered_df = filtered_df.dropna(subset=["accords"])

# 3. Сортування за популярністю на Fragrantica (найпопулярніші будуть зверху)
filtered_df = filtered_df.sort_values(by="magnitude", ascending=False)

# 4. Видаляємо зайві технічні стовпці (розбивки гістограм оцінок),
# залишаючи тільки найважливішу інформацію про аромат
columns_to_keep = [
    "id",
    "name",
    "brand",
    "year",
    "gender",
    "rating_avg",
    "vote_count",
    "longevity_avg",
    "sillage_avg",
    "price_value_avg",
    "magnitude",
    "recent_magnitude",
    "accords",
    "notes_top",
    "notes_middle",
    "notes_base",
    "notes_flat",
    "perfumers",
    "url",
]

# Залишаємо лише ті колонки, які реально є у вашому CSV
existing_columns = [col for col in columns_to_keep if col in filtered_df.columns]
filtered_df = filtered_df[existing_columns]

print(f"Залишилося актуальних ароматів: {len(filtered_df):,}")

# 5. Збереження результату у вашу робочу папку
output_file = "perfumes_actual.csv"
filtered_df.to_csv(output_file, index=False, encoding="utf-8")

print(f"Готово! Нова база збережена поруч зі скриптом: {output_file}")