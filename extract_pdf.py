import fitz
import sys

pdf_path = r"C:\Users\Lenovo\Desktop\（已压缩）SC3 prof2.pdf"
doc = fitz.open(pdf_path)
print(f"Total pages: {doc.page_count}")

# Extract text from all pages
all_text = []
for i in range(doc.page_count):
    page = doc[i]
    text = page.get_text()
    if text.strip():
        all_text.append(f"=== Page {i+1} ===\n{text}")
    else:
        all_text.append(f"=== Page {i+1}: [IMAGE ONLY - NO TEXT LAYER] ===")

doc.close()

# Save to file
with open(r"D:\CC\cc\sc3_prof2_text.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(all_text))

print(f"Extracted text from {len([t for t in all_text if '[IMAGE ONLY]' not in t])} pages with text")
print(f"Image-only pages: {len([t for t in all_text if '[IMAGE ONLY]' in t])}")
print("Text saved to sc3_prof2_text.txt")
