"""
PRINTWORKS PRINT & COPY — Remaining About Page Visual Assets Generator
Generates and optimizes:
- about-detail-finish.webp (900x750)
- about-community.webp (1400x900)
- about-experience.webp (1200x900)
- about-closing.webp (1400x900)
"""

import os
import io
import time
import urllib.request
import urllib.parse
from PIL import Image

TARGET_DIR = os.path.join("assets", "images", "about")
os.makedirs(TARGET_DIR, exist_ok=True)

ITEMS = [
    {
        "filename": "about-detail-finish.webp",
        "tw": 900,
        "th": 750,
        "seed": 5192,
        "prompt": "Macro commercial photography of document binding craftsmanship in print studio. Crisp metal wire binding spine, frosted translucent acetate protective cover, precision guillotine-cut paper edges, neat corner alignment, studio lighting, photorealistic, 8k resolution"
    },
    {
        "filename": "about-community.webp",
        "tw": 1400,
        "th": 900,
        "seed": 7420,
        "prompt": "Overhead flat-lay commercial photography of diverse printed paper materials on a studio table. Spiral-bound coursework notes, corporate branded presentation folder with business cards, carbonless invoice pad, colorful tri-fold event pamphlets, drafting ruler, soft daylight, photorealistic, 8k resolution"
    },
    {
        "filename": "about-experience.webp",
        "tw": 1200,
        "th": 900,
        "seed": 6314,
        "prompt": "Commercial photography of a warm welcoming print shop service counter. Friendly print specialist in dark apron conversing with a customer, showing printed paper weight swatches and document binding samples, bright modern storefront with natural daylight, photorealistic, 8k resolution"
    },
    {
        "filename": "about-closing.webp",
        "tw": 1400,
        "th": 900,
        "seed": 9523,
        "prompt": "Warm atmospheric commercial photography of completed print orders and stationery ready for customer pickup on a wooden dispatch counter in a modern print shop. Packages neatly wrapped in brown kraft paper tied with baker twine, crisp stacks of brochures, warm ambient studio lighting, photorealistic, 8k resolution"
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
    
    print("Generating remaining About page images with polite pacing...")
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
        
        # Pacing: wait 15 seconds before each request
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
                break
            except Exception as e:
                print(f"  [!] Attempt {attempt+1} failed: {e}")
                time.sleep(15)
                
        if not success:
            print(f"  [ERROR] Failed to download {filename}")

    print("\nGeneration complete!")

if __name__ == "__main__":
    main()
