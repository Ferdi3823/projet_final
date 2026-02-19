import xml.etree.ElementTree as ET
import json

tree = ET.parse("books.xml")
root = tree.getroot()

books = []

for book in root.findall("book"):
    title = book.find("title").text
    author = book.find("author").text

    books.append({
        "title": title,
        "author": author
    })

with open("books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, indent=4, ensure_ascii=False)

print("Conversion XML → JSON terminée")
