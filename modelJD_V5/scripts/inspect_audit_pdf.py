import pymupdf
import difflib

doc = pymupdf.open('บทที่1_อาจารย์audit.pdf')
print(f'Total pages in บทที่1_อาจารย์audit.pdf: {len(doc)}')

annots_found = []
for pno, page in enumerate(doc):
    for a in page.annots():
        info = a.info
        annots_found.append((pno + 1, a.type[1], info.get("content", ""), info.get("title", ""), a.rect))

print(f'Total annotations: {len(annots_found)}')
for pno, atype, content, title, rect in annots_found:
    print(f'Page {pno} [{atype}] by {title}: {content} (at {rect})')

# Extract full text
full_text_audit = '\n'.join([f'=== PAGE {i+1} ===\n' + page.get_text() for i, page in enumerate(doc)])
with open('HELPME/ch1_audit_dump.txt', 'w', encoding='utf-8') as f:
    f.write(full_text_audit)

# Compare with HELPME/บทที่1.pdf if exists
doc_orig = pymupdf.open('HELPME/บทที่1.pdf')
full_text_orig = '\n'.join([f'=== PAGE {i+1} ===\n' + page.get_text() for i, page in enumerate(doc_orig)])

print('\n=== TEXT COMPARISON (Audit vs Orig) ===')
audit_lines = [l.strip() for l in full_text_audit.splitlines() if l.strip()]
orig_lines = [l.strip() for l in full_text_orig.splitlines() if l.strip()]

diff = list(difflib.unified_diff(orig_lines, audit_lines, fromfile='บทที่1_orig', tofile='บทที่1_audit', lineterm=''))
print(f'Total diff lines: {len(diff)}')
for line in diff[:60]:
    print(line)
if len(diff) > 60:
    print(f'... and {len(diff)-60} more lines')
