import kagglehub

# Завантажити останню версію датасету
path = kagglehub.dataset_download("ledecanteur/fragrantica-perfumes")
print("Шлях до завантажених файлів:", path)
# Файл perfumes.csv знаходитиметься за цим шляхом