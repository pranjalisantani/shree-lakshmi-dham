"""
Workspace File Inventory and Backup Plan Generator
"""

import os
import time

workspace = r'c:\Users\pranjali\OneDrive\Desktop\Divinity_Maa_Laxmi'
items = []

for root, dirs, files in os.walk(workspace):
    for f in files:
        full = os.path.join(root, f)
        rel = os.path.relpath(full, workspace)
        sz = os.path.getsize(full)
        mtime = os.path.getmtime(full)
        mstr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
        items.append((rel, sz, mstr))

items.sort(key=lambda x: x[0])
print(f"Total files in workspace: {len(items)}")
header = f"{'File Path':<55} {'Size (Bytes)':>14} {'Last Modified':>20}"
print(header)
print("-" * len(header))
for rel, sz, mstr in items:
    print(f"{rel:<55} {sz:>14,} {mstr:>20}")

