"""
PRINTWORKS PRINT & COPY — Blog Editorial Photography Synchronizer
Downloads authentic commercial editorial print shop and paper photography
for all 7 sections of blog.html and optimizes into local assets/images/blog/*.webp.
"""

import os
import io
import time
import urllib.request
from PIL import Image

TARGET_DIR = os.path.join("assets", "images", "blog")
os.makedirs(TARGET_DIR, exist_ok=True)

PHOTO_SPECS = [
    {
        "filename": "blog-masthead.webp",
        "photo_id": "1544717305-2782549b5136",
        "target_w": 1200,
        "target_h": 800,
        "description": "Editorial studio notebook, paper proofs, and stationery on worktable"
    },
    {
        "filename": "blog-featured-paper.webp",
        "photo_id": "1513530534585-c7b1394c6d51",
        "target_w": 1200,
        "target_h": 800,
        "description": "Tactile luxury paper stocks, card envelopes, and stationery sheets"
    },
    {
        "filename": "blog-file-check.webp",
        "photo_id": "1581291518857-4e27b48ff24e",
        "target_w": 1000,
        "target_h": 700,
        "description": "Architectural and graphic drafting desk with layout proofs and rulers"
    },
    {
        "filename": "blog-color-guide.webp",
        "photo_id": "1508739773434-c26b3d09e071",
        "target_w": 1000,
        "target_h": 700,
        "description": "Color swatch cards, CMYK print samples, and paper palettes"
    },
    {
        "filename": "blog-process-file.webp",
        "photo_id": "1531403009284-440f080d1e12",
        "target_w": 1000,
        "target_h": 700,
        "description": "Digital workstation inspecting document layout, safe zones, and margins"
    },
    {
        "filename": "blog-process-paper.webp",
        "photo_id": "1450133064473-71024230f91b",
        "target_w": 1000,
        "target_h": 700,
        "description": "Hands examining and comparing printed proof sheets under studio light"
    },
    {
        "filename": "blog-process-output.webp",
        "photo_id": "1561070791-2526d30994b5",
        "target_w": 1000,
        "target_h": 700,
        "description": "Freshly printed full-color sheets and editorial materials"
    },
    {
        "filename": "blog-paper-notes.webp",
        "photo_id": "1579783900882-c0d3dad7b119",
        "target_w": 1400,
        "target_h": 900,
        "description": "Macro textured artistic paper and layered cardstock with organic fibers"
    },
    {
        "filename": "blog-closing.webp",
        "photo_id": "1516962215378-7fa2e137ae93",
        "target_w": 1200,
        "target_h": 800,
        "description": "Calm editorial reading space with open notebook, coffee, and sunlight"
    },
    {
        "filename": "blog-guide-readiness.webp",
        "photo_id": "1512314889357-e157c22f938d",
        "target_w": 900,
        "target_h": 650,
        "description": "Pre-flight checklist sheets, binder notes, and pen on studio desk"
    },
    {
        "filename": "blog-guide-duplex.webp",
        "photo_id": "1524995997946-a1c2e315a42f",
        "target_w": 900,
        "target_h": 650,
        "description": "Open booklet, catalog, and double-sided printed handbook pages"
    }
]

def download_and_crop(spec):
    filename = spec["filename"]
    pid = spec["photo_id"]
    tw, th = spec["target_w"], spec["target_h"]
    dest_path = os.path.join(TARGET_DIR, filename)

    url = f"https://images.unsplash.com/photo-{pid}?auto=format&fit=crop&w=1800&q=85"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"[*] Downloading {filename} ({spec['description']})...")
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read()

    img = Image.open(io.BytesIO(raw)).convert("RGB")
    orig_w, orig_h = img.size

    target_aspect = tw / th
    current_aspect = orig_w / orig_h

    if current_aspect > target_aspect:
        new_w = int(orig_h * target_aspect)
        left = (orig_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, orig_h))
    else:
        new_h = int(orig_w / target_aspect)
        top = (orig_h - new_h) // 2
        img = img.crop((0, top, orig_w, top + new_h))

    final_img = img.resize((tw, th), Image.Resampling.LANCZOS)
    final_img.save(dest_path, "WEBP", quality=88)

    size_kb = os.path.getsize(dest_path) / 1024
    print(f"  ✓ Saved {dest_path} -> {tw}x{th} ({size_kb:.1f} KB)")
    return True

def main():
    print("=" * 70)
    print("PRINTWORKS PRINT & COPY — SYNCHRONIZING REAL BLOG EDITORIAL PHOTOGRAPHY")
    print("=" * 70)
    
    success = 0
    for spec in PHOTO_SPECS:
        try:
            if download_and_crop(spec):
                success += 1
            time.sleep(0.4)
        except Exception as e:
            print(f"  [ERROR] Failed {spec['filename']}: {e}")

    print("=" * 70)
    print(f"✓ {success}/{len(PHOTO_SPECS)} High-Definition Blog Editorial WebP Assets Synchronized!")
    print("=" * 70)

if __name__ == "__main__":
    main()
