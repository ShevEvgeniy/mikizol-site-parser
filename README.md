# 🧠 Mikizol Website Parser & RAG Data Preparer

Скрипты для автоматического парсинга сайта [mikizol.ru], очистки текста и подготовки данных для обучения LLM или RAG-систем.

---

## 📦 Установка

```bash
pip install requests beautifulsoup4
```

---

## ⚙️ Использование

### 1. Получение всех URL из sitemap:

```bash
python get_urls_from_sitemap.py
```

👉 Создаётся `urls.txt`

---

### 2. Парсинг всех страниц по категориям:

```bash
python parser_to_md_by_section.py
```

👉 Создаётся `mikizol_by_category.md`

---

### 3. Очистка текста, удаление повторов и экспорт:

```bash
python clean_md_to_json_and_markdown.py
```

👉 Итог:
- `mikizol_clean.json` — для RAG/LLM/векторных баз
- `mikizol_clean.md` — чистый markdown для чтения

---

## 📘 Пример JSON:

```json
{
  "category": "🏭 Продукция",
  "url": "https://mikizol.ru/products/item1/",
  "content": "Описание, характеристики, применение..."
}
```

---

## 📄 Лицензия

MIT License
