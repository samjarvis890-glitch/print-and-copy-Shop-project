"""
PRINTWORKS PRINT & COPY — Blog Page Photographic Asset Generator
Generates high-definition, authentic commercial editorial photography
for all 7 sections of the Blog page (blog.html), saving directly as optimized WebP.
"""

import os
import io
import time
import urllib.request
import urllib.parse
from PIL import Image, ImageDraw, ImageFilter, ImageFont

TARGET_DIR = os.path.join("assets", "images", "blog")
os.makedirs(TARGET_DIR, exist_ok=True)

IMAGES_SPEC = [
    {
        "filename": "blog-masthead.webp",
        "width": 1200,
        "height": 800,
        "prompt": "Authentic commercial editorial photography of premium paper stock samples, printed proofs, an open notebook, and neatly arranged design documents on a clean minimalist creative studio worktable, soft natural morning daylight from window, shallow depth of field, 8k resolution, photorealistic"
    },
    {
        "filename": "blog-featured-paper.webp",
        "width": 1200,
        "height": 800,
        "prompt": "Close-up editorial macro photography of luxury tactile paper stocks, silk matte 350gsm cardstock, organic textured cotton rag paper, and smooth uncoated bond paper arranged in elegant fan layout on wood table, warm studio lighting, crisp paper edges, photorealistic"
    },
    {
        "filename": "blog-file-check.webp",
        "width": 1000,
        "height": 700,
        "prompt": "Top-down commercial flat-lay photography of architectural drafting desk with printed document proof sheets, crop marks, alignment rulers, precision cutting knife, and Pantone color swatches, clean editorial aesthetic, photorealistic"
    },
    {
        "filename": "blog-color-guide.webp",
        "width": 1000,
        "height": 700,
        "prompt": "Professional studio still life comparing vibrant full-color printed catalog page alongside crisp monochrome high-contrast black and white typography proof, neutral studio backdrop, sharp printing details, photorealistic"
    },
    {
        "filename": "blog-process-file.webp",
        "width": 1000,
        "height": 700,
        "prompt": "Clean professional print shop workstation showing computer monitor displaying print layout margins and page boundaries, with fresh printed proof sheets and notebook resting on clean desk, photorealistic"
    },
    {
        "filename": "blog-process-paper.webp",
        "width": 1000,
        "height": 700,
        "prompt": "Artisan printer hands carefully holding and comparing paper swatches of different weights and textures under balanced inspection lamp in print studio, tactile craftsmanship, photorealistic"
    },
    {
        "filename": "blog-process-output.webp",
        "width": 1000,
        "height": 700,
        "prompt": "Commercial photography of crisp printed corporate documents neatly emerging into the output tray of a high-end digital production press printer, sharp detail, clean modern print shop, photorealistic"
    },
    {
        "filename": "blog-paper-notes.webp",
        "width": 1400,
        "height": 900,
        "prompt": "Detailed overhead macro photography of various paper textures, heavy card stock, laid paper with subtle watermarks, and smooth satin finishes overlapping on a solid ash wood surface, soft diffused gallery lighting, photorealistic"
    },
    {
        "filename": "blog-closing.webp",
        "width": 1200,
        "height": 800,
        "prompt": "Warm inviting editorial photography of neatly stacked finished brochures and bound booklets on a clean Scandinavian oak tabletop with coffee mug and stationery, calm afternoon light, photorealistic"
    },
    {
        "filename": "blog-guide-readiness.webp",
        "width": 900,
        "height": 650,
        "prompt": "Editorial still life of pre-flight document checklist sheet, binder clip holding printed sheets, silver metal ruler, and spectacles on studio table, clean organized aesthetic, photorealistic"
    },
    {
        "filename": "blog-guide-duplex.webp",
        "width": 900,
        "height": 650,
        "prompt": "Commercial close-up photograph of double-sided printed manual pages fanned open showing precise back-to-back margin alignment and clean twin-loop wire binding, photorealistic"
    }
]

def synthesize_fallback(item):
    """Fallback generator in case network request fails."""
    filename = item["filename"]
    tw, th = item["width"], item["height"]
    target_path = os.path.join(TARGET_DIR, filename)

    img = Image.new("RGB", (tw, th), (245, 247, 250))
    draw = ImageDraw.Draw(img)

    # Gradient background
    for y in range(th):
        factor = y / th
        r = int(245 * (1 - factor) + 235 * factor)
        g = int(247 * (1 - factor) + 240 * factor)
        b = int(250 * (1 - factor) + 245 * factor)
        draw.line([(0, y), (tw, y)], fill=(r, g, b))

    # Decorative geometric paper sheets
    sheet_w = int(tw * 0.45)
    sheet_h = int(th * 0.6)
    
    # Shadow
    draw.rounded_rectangle(
        [(tw//4 + 8, th//5 + 10), (tw//4 + sheet_w + 8, th//5 + sheet_h + 10)],
        radius=8, fill=(210, 215, 225)
    )
    # Main sheet
    draw.rounded_rectangle(
        [(tw//4, th//5), (tw//4 + sheet_w, th//5 + sheet_h)],
        radius=8, fill=(255, 253, 248), outline=(230, 233, 238), width=2
    )

    # Accent lines
    for i in range(5):
        line_y = th//5 + 40 + i * 28
        draw.line([(tw//4 + 30, line_y), (tw//4 + sheet_w - 30, line_y)], fill=(220, 226, 235), width=3)

    img = img.filter(ImageFilter.SMOOTH)
    img.save(target_path, "WEBP", quality=88)
    print(f"  [Fallback] Generated synthetic {filename} ({os.path.getsize(target_path)//1024} KB)")
    return True

def generate_and_save(item, seed_offset=100):
    filename = item["filename"]
    tw, th = item["width"], item["height"]
    prompt = item["prompt"]
    target_path = os.path.join(TARGET_DIR, filename)

    print(f"[*] Generating: {filename} ({tw}x{th})...")
    encoded_prompt = urllib.parse.quote(prompt)
    
    fetch_w = min(tw, 1024)
    fetch_h = int(fetch_w * (th / tw))
    
    seed = seed_offset + abs(hash(filename)) % 9999
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={fetch_w}&height={fetch_h}&nologo=true&seed={seed}&enhance=true"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    max_retries = 2
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
                
            img = Image.open(io.BytesIO(data))
            
            target_ratio = tw / th
            img_ratio = img.width / img.height

            if img_ratio > target_ratio:
                new_w = int(img.height * target_ratio)
                left = (img.width - new_w) // 2
                img = img.crop((left, 0, left + new_w, img.height))
            else:
                new_h = int(img.width / target_ratio)
                top = (img.height - new_h) // 2
                img = img.crop((0, top, img.width, top + new_h))

            final_img = img.resize((tw, th), Image.Resampling.LANCZOS)
            final_img.save(target_path, "WEBP", quality=88)
            
            file_kb = os.path.getsize(target_path) / 1024
            print(f"  ✓ Successfully saved {target_path} ({file_kb:.1f} KB)")
            return True
        except Exception as e:
            print(f"  [!] Attempt {attempt+1} failed for {filename}: {e}")
            time.sleep(2)

    print(f"  [!] Falling back to local synthesizer for {filename}...")
    return synthesize_fallback(item)

def main():
    print("=" * 65)
    print("PRINTWORKS PRINT & COPY — BLOG PHOTOGRAPHIC ASSET GENERATION")
    print("=" * 65)
    
    success_count = 0
    for idx, item in enumerate(IMAGES_SPEC):
        if generate_and_save(item, seed_offset=500 + idx * 43):
            success_count += 1
        time.sleep(1)

    print("=" * 65)
    print(f"Completed! {success_count}/{len(IMAGES_SPEC)} blog images generated and saved.")
    print("=" * 65)

if __name__ == "__main__":
    main()
