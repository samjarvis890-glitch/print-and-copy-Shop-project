import os
import re
from PIL import Image

pages = ["services.html", "blog.html", "pricing.html", "contact.html"]

for p in pages:
    if not os.path.exists(p):
        print(f"File {p} does not exist")
        continue
    with open(p, "r", encoding="utf-8") as f:
        content = f.read()
    imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content)
    print(f"\n=================== {p} ({len(imgs)} images) ===================")
    for img in imgs:
        if "logo" in img or "icon" in img or img.endswith(".svg"):
            continue
        exists = os.path.exists(img)
        if exists:
            sz = os.path.getsize(img)
            try:
                with Image.open(img) as im:
                    w, h = im.size
                    fmt = im.format
                print(f"  {img} | {sz/1024:.1f} KB | {w}x{h} ({fmt})")
            except Exception as e:
                print(f"  {img} | {sz/1024:.1f} KB | Error opening: {e}")
        else:
            print(f"  {img} | MISSING!")
