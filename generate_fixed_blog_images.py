"""
PRINTWORKS PRINT & COPY — Fix Unsuitable Blog Images Script
Generates authentic, highly relevant commercial print shop photography
for the 9 unsuitable images in blog.html.
"""

import os
import io
import time
import urllib.request
import urllib.parse
from PIL import Image

TARGET_DIR = os.path.join("assets", "images", "blog")
os.makedirs(TARGET_DIR, exist_ok=True)

ITEMS_TO_FIX = [
    {
        "filename": "blog-masthead.webp",
        "tw": 1200,
        "th": 800,
        "seed": 91234,
        "prompt": "Editorial flat-lay photography of a commercial print shop design studio table: open hardcover notebook with clean paper, fanned color swatches, printed booklet samples, and graphic designer ruler on light oak wood table, soft natural daylight, shallow depth of field, photorealistic, 8k resolution"
    },
    {
        "filename": "blog-featured-paper.webp",
        "tw": 1200,
        "th": 800,
        "seed": 82341,
        "prompt": "Tactile commercial photography of diverse premium paper stocks, 350gsm silk matte cardstock, textured linen paper, natural kraft card, and smooth cotton rag sheets fanned out on a warm wooden studio table, crisp paper textures and edges, photorealistic, 8k resolution"
    },
    {
        "filename": "blog-file-check.webp",
        "tw": 1000,
        "th": 700,
        "seed": 73412,
        "prompt": "Top-down commercial photography of pre-flight print file inspection desk: printed proof sheet showing clear crop marks, trim bleed margins, registration color bars, precision stainless steel ruler, and cutting mat, crisp photorealistic print shop workbench, 8k resolution"
    },
    {
        "filename": "blog-color-guide.webp",
        "tw": 1000,
        "th": 700,
        "seed": 64123,
        "prompt": "Side-by-side commercial print comparison still life: a vibrant full-color CMYK printed photography catalog page lying next to a crisp high-contrast black-and-white monochrome laser printed text sheet on a clean studio table, sharp details, photorealistic, 8k resolution"
    },
    {
        "filename": "blog-process-file.webp",
        "tw": 1000,
        "th": 700,
        "seed": 51234,
        "prompt": "Commercial photography of modern print shop prepress workstation: desktop computer screen showing high-resolution print document layout with 3mm red bleed lines and safety margins, with fresh printed proof sheets and loupe magnifying glass on clean desk, photorealistic, 8k resolution"
    },
    {
        "filename": "blog-process-output.webp",
        "tw": 1000,
        "th": 700,
        "seed": 42341,
        "prompt": "Commercial photography of heavy-duty digital production color press printer in operation, freshly printed full-color commercial document pages and brochures neatly discharging into the metal output sorter tray, clean modern print shop, photorealistic, 8k resolution"
    },
    {
        "filename": "blog-paper-notes.webp",
        "tw": 1400,
        "th": 900,
        "seed": 33412,
        "prompt": "Overhead flat-lay macro photography of assorted printing paper swatches: textured watercolor card, heavy 300gsm silk cardstock, translucent vellum paper, and smooth uncoated bond paper arranged neatly on a solid light wood surface, precision caliper gauge, warm studio lighting, photorealistic, 8k resolution"
    },
    {
        "filename": "blog-guide-readiness.webp",
        "tw": 900,
        "th": 650,
        "seed": 24123,
        "prompt": "Commercial flat-lay photography of an aluminum clipboard holding a printed Pre-Flight Document Readiness Checklist with checkboxes, technical drafting pen, binder clips, and Pantone color swatches on a clean wooden studio desk, photorealistic, 8k resolution"
    },
    {
        "filename": "blog-guide-duplex.webp",
        "tw": 900,
        "th": 650,
        "seed": 15234,
        "prompt": "Close-up commercial photography of a printed spiral handbook fanned open showing clean double-sided duplex printed pages with back-to-back margin alignment and readable typography, shallow depth of field, photorealistic, 8k resolution"
    }
]

def crop_and_resize(img, tw, th):
    # Strip any watermark from bottom if present (crop 30px off bottom)
    if img.height > 60:
        img = img.crop((0, 0, img.width, img.height - 30))

    target_ratio = tw / th
    img_ratio = img.width / img.height
    
    if img_ratio > target_ratio:
        new_w = int(img.height * target_ratio)
        left = (img.width - new_w) // 2
        img_cropped = img.crop((left, 0, left + new_w, img.height))
    else:
        new_h = int(img.width / target_ratio)
        top = (img.height - new_h) // 2
        img_cropped = img.crop((0, top, img.width, top + new_h))
        
    return img_cropped.resize((tw, th), Image.Resampling.LANCZOS)

def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print("=" * 70)
    print("PRINTWORKS PRINT & COPY — FIXING 9 UNSUITABLE BLOG IMAGES")
    print("=" * 70)
    
    success_count = 0
    for idx, item in enumerate(ITEMS_TO_FIX):
        filename = item["filename"]
        dest_path = os.path.join(TARGET_DIR, filename)
        tw, th = item["tw"], item["th"]
        prompt = item["prompt"]
        seed = item["seed"]
        
        encoded_prompt = urllib.parse.quote(prompt)
        fetch_w = min(tw, 900)
        fetch_h = int(fetch_w * (th / tw)) + 35
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={fetch_w}&height={fetch_h}&nologo=true&seed={seed}"
        
        if idx > 0:
            print("  Pacing 16 seconds to respect rate limits...")
            time.sleep(16)
            
        print(f"[*] Fetching {filename} ({fetch_w}x{fetch_h} -> {tw}x{th})...")
        success = False
        for attempt in range(3):
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=45) as resp:
                    data = resp.read()
                img = Image.open(io.BytesIO(data))
                final_img = crop_and_resize(img, tw, th)
                final_img.save(dest_path, "WEBP", quality=90, method=6)
                kb = os.path.getsize(dest_path) / 1024
                print(f"  ✓ Saved {dest_path} ({kb:.1f} KB)")
                success = True
                success_count += 1
                break
            except Exception as e:
                print(f"  [!] Attempt {attempt+1} failed for {filename}: {e}")
                time.sleep(15)
                
        if not success:
            print(f"  [ERROR] Failed to download {filename}")

    print("=" * 70)
    print(f"Done! {success_count}/{len(ITEMS_TO_FIX)} images successfully generated and saved to {TARGET_DIR}.")
    print("=" * 70)

if __name__ == "__main__":
    main()
