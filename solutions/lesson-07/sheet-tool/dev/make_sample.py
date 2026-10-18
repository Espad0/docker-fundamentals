"""Write a test spreadsheet to stdout.

    python make_sample.py 20 > comments.xlsx              20 rows of comments
    python make_sample.py 232000 --random > big.xlsx      random text that barely compresses: about 9.9 MB
"""
import io
import os
import sys

from openpyxl import Workbook

rows = int(sys.argv[1])
book = Workbook()
sheet = book.active
if "--random" in sys.argv:
    for i in range(rows):
        sheet.append([os.urandom(12).hex(), os.urandom(8).hex(), i])
else:
    sheet.append(["Customer comment", "Region"])
    for i in range(rows):
        sheet.append([f"Comment number {i}: the delivery was late but the product works well", "EU"])
buffer = io.BytesIO()
book.save(buffer)
sys.stdout.buffer.write(buffer.getvalue())
size = buffer.tell()
print(f"wrote {rows} rows, " + (f"{size / 1e6:.1f} MB" if size > 1e6 else f"{size / 1e3:.0f} kB"), file=sys.stderr)
