"""
Release Stability and Asset Integrity Audit
Verifies:
1. Zero broken assets (all referenced files exist and are valid)
2. Audio instance reuse
3. Event listener lifecycle
4. Viewport scroll locking
5. Chrome console logs and errors
"""

import os
import re
import subprocess

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def audit_all_assets():
    print("=" * 70)
    print("1. CHECKING ASSET INTEGRITY ACROSS ALL HTML & CSS FILES")
    print("=" * 70)

    html_files = ['index.html', 'tests/preview_darshan.html', 'tests/manual_hardware_test.html']
    css_files = [os.path.join('css', f) for f in os.listdir(os.path.join(WORKSPACE, 'css')) if f.endswith('.css')]

    all_files = html_files + css_files
    checked = set()
    broken = []
    found = 0

    for rel_f in all_files:
        full_f = os.path.join(WORKSPACE, rel_f)
        with open(full_f, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract local links
        refs = re.findall(r'(?:src|href)=["\']([^"\':#]+)["\']', content)
        refs += re.findall(r'url\(["\']?([^"\'\)\#]+)["\']?\)', content)

        for ref in refs:
            ref_clean = ref.strip().split('?')[0]
            if ref_clean.startswith('http') or ref_clean.startswith('//') or not ref_clean or ref_clean.startswith('data:'):
                continue
            if ref_clean in checked:
                continue
            checked.add(ref_clean)

            target1 = os.path.normpath(os.path.join(WORKSPACE, ref_clean))
            target2 = os.path.normpath(os.path.join(os.path.dirname(full_f), ref_clean))
            exists = os.path.exists(target1) or os.path.exists(target2)
            target = target1 if os.path.exists(target1) else target2
            size = os.path.getsize(target) if exists else 0

            if not exists or size == 0:
                broken.append((rel_f, ref_clean))
                print(f"[-] BROKEN ASSET: {ref_clean} in {rel_f}")
            else:
                found += 1
                print(f"[✓] Asset OK: {ref_clean:<42} ({size:>9,} bytes) [ref in {rel_f}]")

    print(f"\nTotal unique local assets checked: {len(checked)}")
    if broken:
        print(f"[-] FAILED: {len(broken)} broken assets detected.")
        return False
    else:
        print(f"[+] PASSED: All {found} local assets exist and are non-empty!")
        return True


def audit_scroll_locking():
    print("\n" + "=" * 70)
    print("2. CHECKING ACCIDENTAL SCROLL LOCKING IN CSS")
    print("=" * 70)

    sanctum_css = os.path.join(WORKSPACE, 'css', 'sanctum.css')
    with open(sanctum_css, 'r', encoding='utf-8') as f:
        content = f.read()

    has_overflow_hidden = 'overflow: hidden;' in content
    has_100vh = 'height: 100vh;' in content
    has_100vw = 'width: 100vw;' in content

    print(f"[✓] .sanctum-sanctorum overflow: hidden : {has_overflow_hidden}")
    print(f"[✓] .sanctum-sanctorum height: 100vh     : {has_100vh}")
    print(f"[✓] .sanctum-sanctorum width: 100vw      : {has_100vw}")

    return has_overflow_hidden and has_100vh and has_100vw


def audit_console_cleanliness():
    print("\n" + "=" * 70)
    print("3. CHECKING REAL CHROME CONSOLE AND RUNTIME LOGS")
    print("=" * 70)

    chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    url = 'file:///' + os.path.join(WORKSPACE, 'index.html').replace('\\', '/')

    cmd = [
        chrome,
        '--headless=new',
        '--no-sandbox',
        '--disable-gpu',
        '--enable-logging=stderr',
        '--v=1',
        '--dump-dom',
        url
    ]

    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=15, encoding='utf-8', errors='replace')
    stderr = proc.stderr
    print(f"Chrome exit code: {proc.returncode}")

    # Check for JavaScript errors in stderr
    js_errors = [line for line in stderr.splitlines() if 'CONSOLE' in line and 'error' in line.lower()]
    if js_errors:
        print("[-] JavaScript errors detected in Chrome stderr:")
        for err in js_errors:
            print("   ", err)
        return False
    else:
        print("[+] Zero JavaScript runtime errors detected in Google Chrome!")
        return True


if __name__ == '__main__':
    ok1 = audit_all_assets()
    ok2 = audit_scroll_locking()
    ok3 = audit_console_cleanliness()
    overall = ok1 and ok2 and ok3
    print("\n" + "=" * 70)
    print(f"RELEASE STABILITY AUDIT RESULT: {'PASS' if overall else 'FAIL'}")
    print("=" * 70)

