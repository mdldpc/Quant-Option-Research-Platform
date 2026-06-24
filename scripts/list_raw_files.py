from pathlib import Path

ROOTS = [
    Path(r"F:\CFFEX.2025"),
    Path(r"F:\CFFEX.2026"),
]

all_files = []

for root in ROOTS:
    files = sorted(root.glob("*.csv.xz"))
    all_files.extend(files)

print("Total files:", len(all_files))

print("\nFirst 20:")
for f in all_files[:20]:
    print(f)

print("\nLast 20:")
for f in all_files[-20:]:
    print(f)