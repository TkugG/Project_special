import fitz

doc = fitz.open("HELPME/บทที่3.pdf")
print(f"Total pages: {len(doc)}")

with open("HELPME/บทที่3_extracted.txt", "w", encoding="utf-8") as out:
    for i, page in enumerate(doc):
        text = page.get_text()
        out.write(f"\n--- PAGE {i+1} ---\n")
        out.write(text)
        print(f"Page {i+1}: length={len(text)}, first_line={repr(text.splitlines()[0] if text.splitlines() else '')}")
