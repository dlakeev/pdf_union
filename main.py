import re
from collections import defaultdict
from pypdf import PdfWriter

folder = input("Введите путь с файлами")
out_dir = folder
out_dir.mkdir(exist_ok=True)

PART_RE = re.compile(r"\s*ч\s*\d+$", re.IGNORECASE)


def natkey(p):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", p.name)]


groups = defaultdict(list)
skipped = []
for pdf in folder.glob("*.pdf"):
    if PART_RE.search(pdf.stem):
        base = PART_RE.sub("", pdf.stem).strip()
        groups[base].append(pdf)
    else:
        skipped.append(pdf)

for base, files in groups.items():
    files = sorted(files, key=natkey)
    out_path = out_dir / f"{base}.pdf"
    writer = PdfWriter()
    for f in files:
        writer.append(str(f))
    writer.write(str(out_path))
    writer.close()
    print(f"СКЛЕЕНО: {out_path.name}  ←  {len(files)} ч.")

print(f"\nОбъединено документов: {len(groups)}")
print("Не тронуто (singles):")
for f in skipped:
    print(f"  – {f.name}")
