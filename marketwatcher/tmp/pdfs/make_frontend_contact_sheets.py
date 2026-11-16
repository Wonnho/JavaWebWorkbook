from pathlib import Path
from PIL import Image, ImageDraw


root = Path(__file__).resolve().parents[2]
rendered = root / "tmp" / "pdfs" / "frontend-rendered"
pages = sorted(rendered.glob("page-*.png"))
thumb_w, thumb_h, label_h = 150, 212, 20
cols, rows = 5, 4
per_sheet = cols * rows

for sheet_index in range((len(pages) + per_sheet - 1) // per_sheet):
    subset = pages[sheet_index * per_sheet:(sheet_index + 1) * per_sheet]
    sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), "#DCE3EC")
    draw = ImageDraw.Draw(sheet)
    for index, page_path in enumerate(subset):
        page = Image.open(page_path).convert("RGB")
        page.thumbnail((thumb_w - 6, thumb_h - 6))
        col, row = index % cols, index // cols
        x = col * thumb_w + (thumb_w - page.width) // 2
        y = row * (thumb_h + label_h) + 3
        sheet.paste(page, (x, y))
        number = int(page_path.stem.split("-")[-1])
        draw.text((col * thumb_w + 7, row * (thumb_h + label_h) + thumb_h),
                  f"Page {number}", fill="#102A56")
    first = sheet_index * per_sheet + 1
    last = min((sheet_index + 1) * per_sheet, len(pages))
    output = rendered / f"contact-{first:03d}-{last:03d}.png"
    sheet.save(output)
    print(output)
