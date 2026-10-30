import pymupdf

doc = pymupdf.open('บทที่1test.pdf')
print(f'Total pages in บทที่1test.pdf: {len(doc)}')

for i, page in enumerate(doc):
    print(f'==================== PAGE {i+1} ====================')
    print(page.get_text())
