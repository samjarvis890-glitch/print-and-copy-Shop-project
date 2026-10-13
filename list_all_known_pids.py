import os
import re

used_pids = set()
for root, dirs, files in os.walk("."):
    for f in files:
        if f.endswith((".py", ".html")):
            with open(os.path.join(root, f), "r", encoding="utf-8", errors="ignore") as fp:
                txt = fp.read()
            pids = re.findall(r"photo-([a-zA-Z0-9_-]{10,25})", txt)
            pids += re.findall(r'photo_id["\']?\s*:\s*["\']([a-zA-Z0-9_-]{10,25})["\']', txt)
            for pid in pids:
                used_pids.add(pid)

print(f"Total known photo IDs in codebase: {len(used_pids)}")
for pid in sorted(used_pids):
    print(" ", pid)
