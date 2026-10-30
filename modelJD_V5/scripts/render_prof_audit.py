import pymupdf

doc = pymupdf.open('บทที่1_อาจารย์audit.pdf')

for pno, page in enumerate(doc):
    print(f'============================== PAGE {pno+1} ==============================')
    pix = page.get_pixmap(dpi=150)
    pix.save(f'HELPME/images/prof_audit_p{pno+1}.png')
    
    annots = list(page.annots())
    print(f'Annotations on page {pno+1}: {len(annots)}')
    for a in annots:
        info = a.info
        content = info.get('content', '')
        title = info.get('title', '')
        print(f"  - [{a.type[1]}] by {title}: '{content}' at Rect {a.rect}")
