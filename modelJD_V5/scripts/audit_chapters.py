import pypdf

with open('HELPME/ch1_dump.txt', encoding='utf-8') as f: ch1 = f.read()
with open('HELPME/ch2_dump.txt', encoding='utf-8') as f: ch2 = f.read()
with open('HELPME/ch3_dump.txt', encoding='utf-8') as f: ch3 = f.read()

print('=== 1. CHAPTER 1 AUDIT ===')
print('Has 1.6.4 in Ch1?:', '1.6.4' in ch1)
p6_start = ch1.find('--- PAGE 6 ---')
if p6_start != -1:
    print('Ch1 Page 6 content length:', len(ch1[p6_start:].strip()))

print('\n=== 2. CHAPTER 2 TITLE AUDIT ===')
for line in ch2.split('\n')[:15]:
    if any(k in line for k in ['โครงงาน', 'ระบบ', 'บทที่ 2']):
        print('  Ch2 Title line:', line.strip())

print('\n=== 3. CHAPTER 2 COSINE SIMILARITY AUDIT ===')
for idx, line in enumerate(ch2.split('\n')):
    if any(k in line.lower() for k in ['cosine', 'โคไซน์', '6.85']):
        print(f'  Line {idx+1}: {line.strip()[:100]}')

print('\n=== 4. CHAPTER 2 HYBRID AUDIT ===')
for idx, line in enumerate(ch2.split('\n')):
    if 'ผสมผสาน' in line:
        print(f'  Line {idx+1}: {line.strip()[:100]}')

print('\n=== 5. CITATION IN CHAPTER 3 AUDIT ===')
for idx, line in enumerate(ch3.split('\n')):
    if any(k in line for k in ['Ali', 'Sangkatip', 'สังฆทิพย์']):
        print(f'  Ch3 Line {idx+1}: {line.strip()[:100]}')

print('\n=== 6. CHAPTER 3 FORMAT AUDIT ===')
reader3 = pypdf.PdfReader('HELPME/บทที่3.pdf')
print('Ch3 total pages:', len(reader3.pages))
for i, page in enumerate(reader3.pages):
    txt = page.extract_text()
    caps = [l.strip() for l in txt.split('\n') if any(k in l for k in ['ภาพที่', 'ตารางที่'])]
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    first_l = lines[0] if lines else ''
    last_l = lines[-1] if lines else ''
    print(f'P{i+1} ({len(lines)} lines) | Caps: {caps}')
    print(f'   First: {first_l[:60]}')
    print(f'   Last:  {last_l[:60]}')
