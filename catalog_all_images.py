import os
import hashlib
import glob
from PIL import Image

image_dirs = [
    "assets/images/index",
    "assets/images/home2",
    "assets/images/about",
    "assets/images/services",
    "assets/images/pricing",
    "assets/images/blog",
    "assets/images/contact"
]

all_images = {}
for d in image_dirs:
    if not os.path.exists(d):
        continue
    for f in os.listdir(d):
        if not f.endswith(('.webp', '.jpg', '.png')):
            continue
        p = os.path.join(d, f).replace("\\", "/")
        with open(p, "rb") as fp:
            data = fp.read()
        h = hashlib.md5(data).hexdigest()
        try:
            with Image.open(p) as im:
                w, h_dim = im.size
                all_images[p] = {
                    "hash": h,
                    "size": len(data),
                    "dims": f"{w}x{h_dim}",
                    "dir": d
                }
        except Exception as e:
            all_images[p] = {"hash": h, "size": len(data), "dims": "unknown", "dir": d}

print(f"Total images found on disk: {len(all_images)}")
# Check duplicate hashes
hash_to_paths = {}
for p, meta in all_images.items():
    hash_to_paths.setdefault(meta["hash"], []).append(p)

dups = {h: paths for h, paths in hash_to_paths.items() if len(paths) > 1}
if dups:
    print(f"DUPLICATE IMAGES BY HASH ({len(dups)}):")
    for h, paths in dups.items():
        print(f"  Hash {h[:8]}: {paths}")
else:
    print("Zero byte-for-byte duplicates across all folders.")
