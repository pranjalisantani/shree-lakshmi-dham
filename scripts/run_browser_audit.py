"""
Automated Browser Audit Test Runner
Executes browser_audit_harness.html inside real Google Chrome headless (Blink / V8),
captures DOM output, extracts and validates the test suite assertions.
"""

import os
import sys
import json
import subprocess
import re

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
HARNESS_URL = 'file:///' + os.path.join(WORKSPACE, 'tests', 'browser_audit_harness.html').replace('\\', '/')

def run_browser_audit():
    print("=" * 75)
    print("DIVINITY: RUNNING IN-BROWSER AUTOMATED QUALITY AUDIT VIA GOOGLE CHROME")
    print("=" * 75)

    if not os.path.exists(CHROME_PATH):
        print(f"[-] ERROR: Google Chrome not found at {CHROME_PATH}")
        return False

    cmd = [
        CHROME_PATH,
        '--headless=new',
        '--no-sandbox',
        '--disable-gpu',
        '--dump-dom',
        HARNESS_URL
    ]

    print(f"Executing: {' '.join(cmd[:5])} ...")
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=25, encoding='utf-8', errors='replace')
    except subprocess.TimeoutExpired:
        print("[-] ERROR: Chrome execution timed out.")
        return False

    dom_output = proc.stdout
    if not dom_output:
        print("[-] ERROR: No DOM output returned from Chrome.")
        if proc.stderr:
            print("STDERR:", proc.stderr)
        return False

    # Extract JSON inside <pre id="auditOutput">
    match = re.search(r'<pre id="auditOutput">(.*?)</pre>', dom_output, re.DOTALL)
    if not match:
        print("[-] ERROR: Could not find <pre id=\"auditOutput\"> in Chrome DOM dump.")
        return False

    raw_json = match.group(1).strip()
    try:
        audit_data = json.loads(raw_json)
    except json.JSONDecodeError as e:
        print("[-] ERROR: Failed to parse audit JSON report:", e)
        print("Raw text:", raw_json[:300])
        return False

    total = audit_data.get('testsRun', 0)
    passed = audit_data.get('testsPassed', 0)
    failed = audit_data.get('testsFailed', 0)
    results = audit_data.get('results', [])

    print(f"\n--- BROWSER AUDIT RESULTS: {passed}/{total} PASSED ({failed} FAILED) ---\n")

    for idx, r in enumerate(results, 1):
        status = r.get('status')
        test_name = r.get('test')
        details = r.get('details', '')
        symbol = "[✓]" if status == 'PASS' else "[✗]"
        print(f"{symbol} Test {idx:02d}: {test_name}")
        if details:
            print(f"       Details: {details}")

    print("\n" + "=" * 75)
    if failed == 0 and total > 0:
        print(f"ALL {total} REAL BROWSER TESTS PASSED PERFECTLY!")
        print("=" * 75)
        return True
    else:
        print(f"AUDIT FAILED: {failed} tests failed.")
        print("=" * 75)
        return False

if __name__ == '__main__':
    success = run_browser_audit()
    sys.exit(0 if success else 1)

