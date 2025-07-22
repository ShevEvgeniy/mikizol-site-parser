import requests
from bs4 import BeautifulSoup

sitemaps = [
    "https://mikizol.ru/sitemap-files.xml",
    "https://mikizol.ru/sitemap-iblock-1.xml",
    "https://mikizol.ru/sitemap-iblock-2.xml",
    "https://mikizol.ru/sitemap-iblock-7.xml",
    "https://mikizol.ru/sitemap-iblock-8.xml",
    "https://mikizol.ru/sitemap-iblock-9.xml"
]

headers = {"User-Agent": "Mozilla/5.0"}
all_urls = []

for sm in sitemaps:
    r = requests.get(sm, headers=headers)
    soup = BeautifulSoup(r.text, "xml")
    urls = [loc.text for loc in soup.find_all("loc")]
    all_urls.extend(urls)

# Теперь можно обработать каждый URL и извлечь текст
print(f"Найдено {len(all_urls)} страниц")

# Сохраняем список URL в файл
with open("urls.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(all_urls))
print("Файл urls.txt успешно сохранён.")