"""
FEELGOOD PRINT & COPY — Photorealistic Commercial Photography Generator
Generates high-definition, authentic print-shop commercial photography
for all homepage sections and gallery items, saving directly as optimized WebP.
"""

import os
import io
import time
import urllib.request
import urllib.parse
from PIL import Image

TARGET_DIR = os.path.join("assets", "images", "home")
os.makedirs(TARGET_DIR, exist_ok=True)

IMAGES_SPEC = [
    {
        "filename": "home-hero.webp",
        "width": 1920,
        "height": 1080,
        "prompt": "Commercial photography of a modern bright friendly print and copy shop interior, high-tech digital production laser press printer, neatly stacked colorful brochures and paper, warm natural sunlight through floor-to-ceiling windows, birch wood service counter, clean organized workspace, 8k resolution, award-winning architectural photography"
    },
    {
        "filename": "home-services.webp",
        "width": 1400,
        "height": 900,
        "prompt": "Commercial overhead flat-lay photography of professional printed goods, wire-bound corporate annual reports, luxury foil-stamped business cards, tri-fold colorful brochures, drafting cutting mat, precision metal ruler, sharp focus, vibrant brand colors with warm sunshine yellow and royal blue accents, photorealistic"
    },
    {
        "filename": "home-process.webp",
        "width": 1400,
        "height": 900,
        "prompt": "Commercial photography of a high-speed production digital color printer running in a clean print studio, crisp printed pages emerging smoothly into the output tray, illuminated status panel, professional printing equipment, shallow depth of field, photorealistic, 8k"
    },
    {
        "filename": "home-print-types.webp",
        "width": 1400,
        "height": 900,
        "prompt": "Macro close-up photography of tactile premium paper stocks, 350gsm silk matte cardstock, natural kraft eco paper with organic fibers, and glossy coated sheets fanned out on a designer workbench, beautiful paper textures, natural soft studio lighting, photorealistic, 8k"
    },
    {
        "filename": "home-options.webp",
        "width": 1400,
        "height": 900,
        "prompt": "Commercial product photography of document binding and finishing, silver twin-loop wire bound booklet, spiral coil notebook, gold foil embossed details, velvet matte laminated covers on a clean studio table, photorealistic, 8k"
    },
    {
        "filename": "home-get-started.webp",
        "width": 1400,
        "height": 900,
        "prompt": "Clean modern design studio desk with a laptop displaying a digital print layout, color swatch cards, paper weight samples, metal precision ruler, bright daylight, organized professional workspace, photorealistic, 8k"
    },
    {
        "filename": "home-closing.webp",
        "width": 1920,
        "height": 900,
        "prompt": "Atmospheric evening photography of a welcoming local print and photocopy shop storefront, warm glowing interior lights, neatly arranged shelves of packaged print orders, friendly professional feel-good ambiance, photorealistic, 8k"
    },
    {
        "filename": "gallery-1.webp",
        "width": 1200,
        "height": 900,
        "prompt": "Studio photography of a corporate branding stationery suite, letterhead, business cards, envelopes, presentation folders neatly arranged on a minimal background, elegant and clean, photorealistic, 8k"
    },
    {
        "filename": "gallery-2.webp",
        "width": 1200,
        "height": 900,
        "prompt": "Detailed architectural blueprints and engineering technical drawings rolled and laid flat on an architect drafting table, steel ruler, drafting compass, crisp line weights, photorealistic, 8k"
    },
    {
        "filename": "gallery-3.webp",
        "width": 1200,
        "height": 900,
        "prompt": "High-end editorial photography of an open perfect-bound art exhibition catalog and photography lookbook, thick matte art paper, rich colors, soft studio lighting, photorealistic, 8k"
    },
    {
        "filename": "gallery-4.webp",
        "width": 1200,
        "height": 900,
        "prompt": "Commercial product photography of custom die-cut vinyl stickers and glossy packaging labels on a colorful clean surface, water-resistant finish, vibrant colors, photorealistic, 8k"
    },
    {
        "filename": "gallery-5.webp",
        "width": 1200,
        "height": 900,
        "prompt": "Professional studio shot of mounted large format event posters and foam-board signage displayed on easels, saturated vivid colors, crisp typography, photorealistic, 8k"
    },
    {
        "filename": "gallery-6.webp",
        "width": 1200,
        "height": 900,
        "prompt": "Close-up commercial photography of luxury restaurant dining menus with velvet soft-touch matte lamination, elegant leather trim, water-resistant finish on a dark wooden table, photorealistic, 8k"
    }
]

def generate_and_save(item, seed_offset=200):
    filename = item["filename"]
    tw, th = item["width"], item["height"]
    prompt = item["prompt"]
    target_path = os.path.join(TARGET_DIR, filename)

    print(f"[*] Generating: {filename} ({tw}x{th})...")
    encoded_prompt = urllib.parse.quote(prompt)
    
    # Request high-definition aspect ratio
    fetch_w = min(tw, 1280)
    fetch_h = int(fetch_w * (th / tw))
    
    seed = seed_offset + hash(filename) % 9999
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={fetch_w}&height={fetch_h}&nologo=true&seed={seed}&enhance=true"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = resp.read()
                
            img = Image.open(io.BytesIO(data))
            
            # Smart crop and resize to target dimensions
            target_ratio = tw / th
            img_ratio = img.width / img.height

            if img_ratio > target_ratio:
                # Crop sides
                new_w = int(img.height * target_ratio)
                left = (img.width - new_w) // 2
                img = img.crop((left, 0, left + new_w, img.height))
            else:
                # Crop top/bottom
                new_h = int(img.width / target_ratio)
                top = (img.height - new_h) // 2
                img = img.crop((0, top, img.width, top + new_h))

            final_img = img.resize((tw, th), Image.Resampling.LANCZOS)
            final_img.save(target_path, "WEBP", quality=90)
            
            file_kb = os.path.getsize(target_path) / 1024
            print(f"  ✓ Successfully saved {target_path} ({file_kb:.1f} KB)")
            return True
        except Exception as e:
            print(f"  [!] Attempt {attempt+1} failed: {e}")
            time.sleep(2)

    print(f"  [ERROR] Failed to download {filename} after {max_retries} attempts.")
    return False

def main():
    print("=" * 65)
    print("FEELGOOD PRINT & COPY — PHOTOREALISTIC COMMERCIAL IMAGE GENERATION")
    print("=" * 65)
    
    success_count = 0
    for idx, item in enumerate(IMAGES_SPEC):
        if generate_and_save(item, seed_offset=300 + idx * 37):
            success_count += 1
        time.sleep(1) # Polite pacing

    print("=" * 65)
    print(f"Done! {success_count}/{len(IMAGES_SPEC)} photorealistic images generated and saved.")
    print("=" * 65)

if __name__ == "__main__":
    main()
