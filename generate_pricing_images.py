"""
PRINTWORKS PRINT & COPY — Pricing Page Asset Generation Script
Generates all 6 authentic, high-definition commercial photographs for pricing.html
into assets/images/pricing/*.webp with zero duplication and 100% offline local storage.
"""

import os
import io
import time
import urllib.request
import urllib.parse
from PIL import Image

TARGET_DIR = os.path.join("assets", "images", "pricing")
os.makedirs(TARGET_DIR, exist_ok=True)

ITEMS = [
    {
        "filename": "pricing-intro.webp",
        "tw": 1920,
        "th": 850,
        "seed": 4190,
        "prompt": "Wide panoramic commercial photography of a modern high-end print shop pricing consultation desk. Neat stacks of sample paper weights, glossy brochures, transparent cost estimate sheet on clean birchwood counter, digital laser production printer in background, soft natural sunlight, 8k resolution, authentic architectural photography"
    },
    {
        "filename": "pricing-copying.webp",
        "tw": 1000,
        "th": 1200,
        "seed": 6821,
        "prompt": "Vertical commercial photography of a high-speed commercial digital photocopier duplicating documents in a print shop. Automatic document feeder running crisp collated white pages into clean output tray, digital touch screen control panel illuminated, bright modern studio, photorealistic, 8k resolution"
    },
    {
        "filename": "pricing-finishing-main.webp",
        "tw": 1400,
        "th": 900,
        "seed": 8352,
        "prompt": "Studio product photography of assorted professionally bound corporate presentation documents. Silver twin-loop wire bound annual reports, black spiral notebooks, and saddle-stitched event programs displayed on a minimal concrete studio worktable, soft studio lighting, photorealistic, 8k resolution"
    },
    {
        "filename": "pricing-finishing-detail.webp",
        "tw": 900,
        "th": 700,
        "seed": 2715,
        "prompt": "Macro extreme close-up commercial photography of document binding craftsmanship in print shop. Metal twin-loop wire binding coils, frosted translucent protective acetate cover edge, precision guillotine-cut paper borders, crisp paper fiber textures, shallow depth of field, photorealistic, 8k resolution"
    },
    {
        "filename": "pricing-checklist.webp",
        "tw": 1200,
        "th": 800,
        "seed": 5934,
        "prompt": "Overhead flat-lay commercial photography of a print job quote preparation worksheet. Aluminum clipboard with printed specification checklist, stainless steel digital caliper measuring paper thickness, architectural scale ruler, Pantone color swatch cards, and metal pen on clean wooden desk, photorealistic, 8k resolution"
    },
    {
        "filename": "pricing-closing.webp",
        "tw": 1400,
        "th": 900,
        "seed": 9247,
        "prompt": "Warm atmospheric commercial photography of finished corporate print orders and stationery suites in a modern print shop. Packages neatly wrapped in brown kraft paper with baker twine, corporate stationery boxes, and sample print portfolios ready on the customer service counter, warm ambient lighting, photorealistic, 8k resolution"
    }
]

def crop_and_resize(img, tw, th):
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
    print("PRINTWORKS PRINT & COPY — GENERATING PRICING IMAGES")
    print("=" * 70)
    
    success_count = 0
    for idx, item in enumerate(ITEMS):
        filename = item["filename"]
        dest_path = os.path.join(TARGET_DIR, filename)
        tw, th = item["tw"], item["th"]
        prompt = item["prompt"]
        seed = item["seed"]
        
        encoded_prompt = urllib.parse.quote(prompt)
        fetch_w = min(tw, 800)
        fetch_h = int(fetch_w * (th / tw))
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={fetch_w}&height={fetch_h}&nologo=true&seed={seed}"
        
        if idx > 0:
            print("  Waiting 15 seconds to respect rate limits...")
            time.sleep(15)
            
        print(f"[*] Fetching {filename} ({fetch_w}x{fetch_h} -> {tw}x{th})...")
        success = False
        for attempt in range(3):
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=45) as resp:
                    data = resp.read()
                img = Image.open(io.BytesIO(data))
                final_img = crop_and_resize(img, tw, th)
                final_img.save(dest_path, "WEBP", quality=92, method=6)
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
    print(f"Done! {success_count}/{len(ITEMS)} images successfully generated and saved to {TARGET_DIR}.")
    print("=" * 70)

if __name__ == "__main__":
    main()
