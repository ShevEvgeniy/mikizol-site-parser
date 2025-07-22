import requests
from bs4 import BeautifulSoup
from collections import defaultdict

headers = {"User-Agent": "Mozilla/5.0"}

with open("urls.txt", "r", encoding="utf-8") as f:
    all_urls = [line.strip() for line in f if line.strip()]

# Категории по URL
def categorize(url):
    if "/products/" in url:
        return "🏭 Продукция"
    elif "/company/" in url:
        return "🏢 О компании"
    elif "/contacts/" in url:
        return "📍 Контакты"
    elif "/articles/" in url:
        return "📰 Статьи"
    elif "/support/" in url:
        return "⚙️ Поддержка"
    elif "/objects/" in url:
        return "🏗 Объекты"
    elif "/services/" in url:
        return "🧰 Услуги"
    elif "/media/" in url:
        return "📸 Медиа"
    else:
        return "📋 Другое"

sections = defaultdict(list)

for url in all_urls:
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        section = categorize(url)

        page_md = [f"# {url}\n"]
        for tag in soup.find_all(["h1", "h2", "h3", "ol", "ul", "p"]):
            text = tag.get_text(strip=True)
            if not text:
                continue
            if tag.name == "h1":
                page_md.append(f"# {text}")
            elif tag.name == "h2":
                page_md.append(f"## {text}")
            elif tag.name == "h3":
                page_md.append(f"### {text}")
            elif tag.name == "p":
                page_md.append(f"{text}")
            elif tag.name in ["ul", "ol"]:
                for i, li in enumerate(tag.find_all("li"), start=1):
                    li_text = li.get_text(strip=True)
                    if li_text:
                        if tag.name == "ol":
                            page_md.append(f"{i}. {li_text}")
                        else:
                            page_md.append(f"- {li_text}")
        page_md.append("\n---\n")
        sections[section].extend(page_md)
        print(f"✅ {url}")
    except Exception as e:
        sections[section].append(f"# {url}\nОшибка: {str(e)}\n---\n")

# Сохраняем результат
with open("mikizol_by_category.md", "w", encoding="utf-8") as f:
    for category, content in sections.items():
        f.write(f"# {category}\n\n")
        f.write("\n".join(content))
        f.write("\n\n")

print("✅ Готово: mikizol_by_category.md")
