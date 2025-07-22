import json
import hashlib
from pathlib import Path
from collections import defaultdict


# 🔹 Абсолютный путь к папке скрипта
SCRIPT_DIR = Path(__file__).parent

# 🔹 Полные пути к файлам
INPUT_MD = SCRIPT_DIR / "mikizol_by_category.md"
OUTPUT_JSON = SCRIPT_DIR / "mikizol_clean.json"
OUTPUT_MD = SCRIPT_DIR / "mikizol_clean.md"

# 🔸 Фразы, которые нужно вырезать
stop_phrases = [
    "ООО Микизол", "©", "Все права защищены", "Главная", "Телефон", "Факс",
    "E-mail", "О компании", "Контакты", "Новости", "Политика конфиденциальности"
]

# 🔸 Удаляем лишние строки
def remove_redundant_lines(text, stop_phrases):
    lines = text.split("\n")
    return "\n".join(
        line for line in lines
        if not any(phrase.lower() in line.lower() for phrase in stop_phrases)
    )

# 🔹 Загрузка исходного Markdown-файла
with open(INPUT_MD, "r", encoding="utf-8") as f:
    lines = f.readlines()

data = []
seen_hashes = set()
current_category = ""
current_url = ""
current_content = []

# 🔹 Основной парсинг
for line in lines:
    stripped = line.strip()

    if not stripped:
        continue

    if stripped.startswith("# ") and not stripped.startswith("# http"):
        current_category = stripped[2:].strip()
        continue

    if stripped.startswith("# http"):
        if current_url and current_content:
            raw_text = "\n".join(current_content).strip()
            cleaned_text = remove_redundant_lines(raw_text, stop_phrases)
            text_hash = hashlib.md5(cleaned_text.encode("utf-8")).hexdigest()
            if text_hash not in seen_hashes:
                seen_hashes.add(text_hash)
                data.append({
                    "category": current_category,
                    "url": current_url,
                    "content": cleaned_text
                })
            current_content = []
        current_url = stripped[2:].strip()
        continue

    current_content.append(stripped)

# 🔸 Последний блок
if current_url and current_content:
    raw_text = "\n".join(current_content).strip()
    cleaned_text = remove_redundant_lines(raw_text, stop_phrases)
    text_hash = hashlib.md5(cleaned_text.encode("utf-8")).hexdigest()
    if text_hash not in seen_hashes:
        data.append({
            "category": current_category,
            "url": current_url,
            "content": cleaned_text
        })

# ✅ Сохраняем JSON (для RAG)
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# ✅ Сохраняем Markdown (для просмотра)
with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    grouped = defaultdict(list)
    for item in data:
        grouped[item["category"]].append(item)

    for category, items in grouped.items():
        f.write(f"# {category}\n\n")
        for item in items:
            f.write(f"# {item['url']}\n\n{item['content']}\n\n---\n\n")

print("✅ Готово: mikizol_clean.json и mikizol_clean.md")
