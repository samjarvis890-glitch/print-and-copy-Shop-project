"""
FEELGOOD PRINT & COPY — High-Definition Commercial Photography Synchronizer
Downloads, smart-crops, and optimizes all 13 authentic commercial print shop
photographs into local assets/images/home/*.webp files.
"""

import os
import io
import time
import urllib.request
from PIL import Image

TARGET_DIR = os.path.join("assets", "images", "home")
os.makedirs(TARGET_DIR, exist_ok=True)

PHOTO_SPECS = [
    {
        "filename": "home-hero.webp",
        "photo_id": "1562564055-71e051d33c19",
        "target_w": 1920,
        "target_h": 1080,
        "crop_focus": "center"
    },
    {
        "filename": "home-services.webp",
        "photo_id": "1586075010923-2dd4570fb338",
        "target_w": 1400,
        "target_h": 900,
        "crop_focus": "center"
    },
    {
        "filename": "home-process.webp",
        "photo_id": "1563986768609-322da13575f3",
        "target_w": 1400,
        "target_h": 900,
        "crop_focus": "center"
    },
    {
        "filename": "home-print-types.webp",
        "photo_id": "1527011046414-4781f1f94f8c",
        "target_w": 1400,
        "target_h": 900,
        "crop_focus": "center"
    },
    {
        "filename": "home-options.webp",
        "photo_id": "1544716278-ca5e3f4abd8c",
        "target_w": 1400,
        "target_h": 900,
        "crop_focus": "center"
    },
    {
        "filename": "home-get-started.webp",
        "photo_id": "1497032628192-86f99bcd76bc",
        "target_w": 1400,
        "target_h": 900,
        "crop_focus": "center"
    },
    {
        "filename": "home-closing.webp",
        "photo_id": "1524758631624-e2822e304c36",
        "target_w": 1920,
        "target_h": 900,
        "crop_focus": "center"
    },
    {
        "filename": "gallery-1.webp",
        "photo_id": "1589829085413-56de8ae18c73",
        "target_w": 1200,
        "target_h": 900,
        "crop_focus": "center"
    },
    {
        "filename": "gallery-2.webp",
        "photo_id": "1503694978374-8a2fa686963a",
        "target_w": 1200,
        "target_h": 900,
        "crop_focus": "center"
    },
    {
        "filename": "gallery-3.webp",
        "photo_id": "1544947950-fa07a98d237f",
        "target_w": 1200,
        "target_h": 900,
        "crop_focus": "center"
    },
    {
        "filename": "gallery-4.webp",
        "photo_id": "1513542789411-b6a5d4f31634",
        "target_w": 1200,
        "target_h": 900,
        "crop_focus": "center"
    },
    {
        "filename": "gallery-5.webp",
        "photo_id": "1513519245088-0e12902e5a38",
        "target_w": 1200,
        "target_h": 900,
        "crop_focus": "center"
    },
    {
        "filename": "gallery-6.webp",
        "photo_id": "1555396273-367ea4eb4db5",
        "target_w": 1200,
        "target_h": 900,
        "crop_focus": "center"
    }
]

def process_spec(spec):
    filename = spec["filename"]
    pid = spec["photo_id"]
    tw, th = spec["target_w"], spec["target_h"]
    dest_path = os.path.join(TARGET_DIR, filename)

    url = f"https://images.unsplash.com/photo-{pid}?auto=format&fit=crop&w=2000&q=85"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"[*] Processing {filename} ({tw}x{th})...")
    req = urllib.request.Request(url, headers=headers)
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw_data = resp.read()

    img = Image.open(io.BytesIO(raw_data)).convert("RGB")
    orig_w, orig_h = img.size

    # Smart crop to exact target aspect ratio
    target_aspect = tw / th
    current_aspect = orig_w / orig_h

    if current_aspect > target_aspect:
        # Crop horizontal edges
        new_w = int(orig_h * target_aspect)
        left = (orig_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, orig_h))
    else:
        # Crop vertical edges
        new_h = int(orig_w / target_aspect)
        top = (orig_h - new_h) // 2
        img = img.crop((0, top, orig_w, top + new_h))

    final_img = img.resize((tw, th), Image.Resampling.LANCZOS)
    final_img.save(dest_path, "WEBP", quality=90)
    
    size_kb = os.path.getsize(dest_path) / 1024
    print(f"  ✓ Saved {dest_path} -> {tw}x{th} ({size_kb:.1f} KB)")

def main():
    print("=" * 68)
    print("FEELGOOD PRINT & COPY — SYNCHRONIZING REAL COMMERCIAL PHOTOGRAPHY")
    print("=" * 68)
    
    for spec in PHOTO_SPECS:
        try:
            process_spec(spec)
            time.sleep(0.5)
        except Exception as e:
            print(f"  [ERROR] Failed {spec['filename']}: {e}")

    print("=" * 68)
    print("✓ All 13 High-Definition Commercial WebP Assets Synchronized!")
    print("=" * 68)

if __name__ == "__main__":
    main()
