import re
import os

with open(r'c:\Users\pranjali\OneDrive\Desktop\Divinity_Maa_Laxmi\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find href and src
matches = re.findall(r'(?:href|src)=["\']([^"\']+)["\']', content)
print('Checking local asset paths from index.html:')
all_ok = True
for m in matches:
    if m.startswith('http'):
        continue
    # clean query strings
    clean_path = m.split('?')[0].replace('/', os.sep)
    full_path = os.path.join(r'c:\Users\pranjali\OneDrive\Desktop\Divinity_Maa_Laxmi', clean_path)
    exists = os.path.exists(full_path)
    if exists:
        size_kb = os.path.getsize(full_path) / 1024
        print(f'  [OK] {m} ({size_kb:.1f} KB)')
    else:
        print(f'  [FAIL MISSING] {m}')
        all_ok = False

# Also check srcset
srcset_matches = re.findall(r'srcset=["\']([^"\']+)["\']', content)
for sm in srcset_matches:
    parts = [p.strip().split(' ')[0] for p in sm.split(',')]
    for p_file in parts:
        clean_path = p_file.replace('/', os.sep)
        full_path = os.path.join(r'c:\Users\pranjali\OneDrive\Desktop\Divinity_Maa_Laxmi', clean_path)
        exists = os.path.exists(full_path)
        if exists:
            size_kb = os.path.getsize(full_path) / 1024
            print(f'  [OK srcset] {p_file} ({size_kb:.1f} KB)')
        else:
            print(f'  [FAIL srcset MISSING] {p_file}')
            all_ok = False

print(f'\nOverall asset path integrity: {"PERFECT (ALL ASSETS EXIST)" if all_ok else "ERRORS DETECTED"}')

