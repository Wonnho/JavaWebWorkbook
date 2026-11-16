from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parents[2]
rendered = root / "tmp" / "pdfs" / "rendered"
pages = sorted(rendered.glob("page-*.png"))

thumb_w = 150
thumb_h = 212
label_h = 20
cols = 5
rows = 4
per_sheet = cols * rows

for sheet_index in range((len(pages) + per_sheet - 1) // per_sheet):
    subset = pages[sheet_index * per_sheet:(sheet_index + 1) * per_sheet]
    sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), "#DCE3EC")
    draw = ImageDraw.Draw(sheet)
    for index, page_path in enumerate(subset):
        image = Image.open(page_path).convert("RGB")
        image.thumbnail((thumb_w - 6, thumb_h - 6))
        col = index % cols
        row = index // cols
        x = col * thumb_w + (thumb_w - image.width) // 2
        y = row * (thumb_h + label_h) + 3
        sheet.paste(image, (x, y))
        page_number = int(page_path.stem.split("-")[-1])
        label = f"Page {page_number}"
        draw.text((col * thumb_w + 7, row * (thumb_h + label_h) + thumb_h), label, fill="#102A56")
    first = sheet_index * per_sheet + 1
    last = min((sheet_index + 1) * per_sheet, len(pages))
    out = rendered / f"contact-{first:03d}-{last:03d}.png"
    sheet.save(out)
    print(out)
