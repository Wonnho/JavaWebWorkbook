from pathlib import Path
import re

import pdfplumber
from pypdf import PdfReader


root = Path(__file__).resolve().parents[2]
pdf_path = root / "output" / "pdf" / "spring-authentication-beginners-guide.pdf"
reader = PdfReader(str(pdf_path))
texts = []
out_of_bounds = []

with pdfplumber.open(str(pdf_path)) as pdf:
    for page_number, page in enumerate(pdf.pages, 1):
        text = page.extract_text() or ""
        texts.append(text)
        chars = page.chars
        if not chars:
            continue
        if (
            min(char["x0"] for char in chars) < -0.1
            or max(char["x1"] for char in chars) > page.width + 0.1
            or min(char["top"] for char in chars) < -0.1
            or max(char["bottom"] for char in chars) > page.height + 0.1
        ):
            out_of_bounds.append(page_number)

joined = " ".join(texts)
words = re.findall(r"[A-Za-z0-9_{}@./'-]+", joined)

print("pages", len(reader.pages))
print("words", len(words))
print("empty_text_pages", [i + 1 for i, text in enumerate(texts) if len(text.strip()) < 20])
print("out_of_bounds_pages", out_of_bounds)
print("replacement_chars", joined.count("\ufffd"))
print("chapters_found", sum(1 for number in range(1, 16) if f"CHAPTER {number} " in joined))
print("outline_entries", len(reader.outline))
print("file_bytes", pdf_path.stat().st_size)

assert len(reader.pages) == 120
assert not out_of_bounds
assert "\ufffd" not in joined
assert len(words) > 10_000
assert all(f"CHAPTER {number} " in joined for number in range(1, 16))
