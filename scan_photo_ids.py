import glob
import re

for f in glob.glob("*.py"):
    with open(f, "r", encoding="utf-8") as fp:
        content = fp.read()
    pids = re.findall(r"photo-([a-zA-Z0-9_-]+)", content)
    pids += re.findall(r'photo_id["\']?\s*:\s*["\']([a-zA-Z0-9_-]+)["\']', content)
    if pids:
        print(f, "->", len(pids), "photo IDs:", set(pids))
