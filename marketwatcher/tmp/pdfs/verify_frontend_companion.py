from pathlib import Path
import re

import pdfplumber
from pypdf import PdfReader


root = Path(__file__).resolve().parents[2]
pdf_path = root / "output" / "pdf" / "thymeleaf-mustache-frontend-companion.pdf"
reader = PdfReader(str(pdf_path))
texts = []
out_of_bounds = []
image_occurrences = 0

with pdfplumber.open(str(pdf_path)) as pdf:
    for page_number, page in enumerate(pdf.pages, 1):
        text = page.extract_text() or ""
        texts.append(text)
        chars = page.chars
        if chars and (
            min(char["x0"] for char in chars) < -0.1
            or max(char["x1"] for char in chars) > page.width + 0.1
            or min(char["top"] for char in chars) < -0.1
            or max(char["bottom"] for char in chars) > page.height + 0.1
        ):
            out_of_bounds.append(page_number)

for page in reader.pages:
    resources = page.get("/Resources") or {}
    xobjects = resources.get("/XObject") or {}
    for value in xobjects.values():
        obj = value.get_object()
        if obj.get("/Subtype") == "/Image":
            image_occurrences += 1

joined = " ".join(texts)
words = re.findall(r"[A-Za-z0-9_{}@./'<>=?-]+", joined)
cross_reference_pages = sum("BACKEND COMPANION" in text for text in texts)

print("pages", len(reader.pages))
print("words", len(words))
print("empty_text_pages", [i + 1 for i, text in enumerate(texts) if len(text.strip()) < 20])
print("out_of_bounds_pages", out_of_bounds)
print("replacement_chars", joined.count("\ufffd"))
print("chapters_found", sum(1 for number in range(1, 13) if f"CHAPTER {number} " in joined))
print("outline_entries", len(reader.outline))
print("backend_cross_reference_pages", cross_reference_pages)
print("embedded_image_occurrences", image_occurrences)
print("file_bytes", pdf_path.stat().st_size)

assert len(reader.pages) == 116
assert not out_of_bounds
assert "\ufffd" not in joined
assert len(words) > 10_000
assert all(f"CHAPTER {number} " in joined for number in range(1, 13))
assert len(reader.outline) == 12
assert cross_reference_pages == 108
assert image_occurrences >= 6
