import os
import lzma

path = r"F:\CFFEX.2025\CFFEX.IF.20250101.csv.xz"

print("Checking file...")
print("Path:", path)
print("Exists:", os.path.exists(path))

if os.path.exists(path):
    print("File size:", os.path.getsize(path), "bytes")

print("Reading first lines...")

with lzma.open(path, mode="rt", encoding="utf-8", errors="replace") as f:
    for i in range(20):
        line = f.readline()
        print(f"LINE {i+1}:", repr(line))

print("Done.")