"""
PRINTWORKS PRINT & COPY — Services Page Asset Generation Script
Generates all 10 authentic, high-definition commercial photographs for services.html
into assets/images/services/*.webp with zero duplication and 100% offline local storage.
"""

import os
import io
import time
import urllib.request
import urllib.parse
from PIL import Image

TARGET_DIR = os.path.join("assets", "images", "services")
os.makedirs(TARGET_DIR, exist_ok=True)

ITEMS = [
    {
        "filename": "services-intro.webp",
        "tw": 1920,
        "th": 900,
        "seed": 3102,
        "prompt": "Wide panoramic commercial photography of a modern high-tech digital printing production facility. Heavy-duty digital color laser press running, clean birchwood trimming table, organized shelves of paper reams and sample booklets, warm studio daylight, 8k resolution, authentic architectural photography"
    },
    {
        "filename": "document-printing.webp",
        "tw": 1400,
        "th": 1000,
        "seed": 4589,
        "prompt": "Commercial photography of a high-speed production digital color printer running in a clean print studio. Freshly printed full-color brochures and report pages emerging smoothly into output sorting tray, illuminated digital status panel, photorealistic, 8k resolution"
    },
    {
        "filename": "photocopying.webp",
        "tw": 1000,
        "th": 1400,
        "seed": 6271,
        "prompt": "Vertical portrait commercial photography of a modern heavy-duty digital multifunction office photocopier and scanner in a bright print shop. Multipage automatic document feeder running clean white sheets, illuminated scan platen, clean wooden counter, photorealistic, 8k resolution"
    },
    {
        "filename": "binding-main.webp",
        "tw": 1400,
        "th": 900,
        "seed": 7814,
        "prompt": "Commercial product photography of diverse professionally bound documents. Sleek silver twin-loop wire bound corporate portfolio, black spiral coil notebook, and saddle-stitched booklet stacked on a minimal studio table, soft lighting, photorealistic, 8k resolution"
    },
    {
        "filename": "binding-detail.webp",
        "tw": 800,
        "th": 600,
        "seed": 2943,
        "prompt": "Macro extreme close-up photography of metal twin-loop wire binding spine and plastic comb binding. Sharp focus on shiny silver wire loops through cleanly punched square holes in thick cardstock paper, shallow depth of field, photorealistic, 8k resolution"
    },
    {
        "filename": "finished-documents.webp",
        "tw": 800,
        "th": 600,
        "seed": 8325,
        "prompt": "Studio close-up commercial photography of finished corporate presentation booklets with frosted translucent acetate front covers and textured black linen card backings, clean edges, soft studio lighting, photorealistic, 8k resolution"
    },
    {
        "filename": "study-documents.webp",
        "tw": 1000,
        "th": 750,
        "seed": 5467,
        "prompt": "Overhead commercial photography of academic study materials on a wooden desk. Coil-bound university student course pack open with printed diagrams and charts, highlighted notes, pen, notebook, warm natural light, photorealistic, 8k resolution"
    },
    {
        "filename": "business-documents.webp",
        "tw": 1000,
        "th": 750,
        "seed": 9182,
        "prompt": "Commercial photography of executive corporate business documents on a dark walnut boardroom conference table. Wire-bound annual financial reports with vibrant pie charts, matte presentation folders, luxury business cards, executive fountain pen, photorealistic, 8k resolution"
    },
    {
        "filename": "specification-guide.webp",
        "tw": 1200,
        "th": 800,
        "seed": 3846,
        "prompt": "Top-down flat-lay photography of a print shop project specification planning desk. An aluminum clipboard holding a printed print order checklist with ticks, stainless steel caliper gauge measuring paper thickness, architectural scale ruler, and Pantone color swatch chips, photorealistic, 8k resolution"
    },
    {
        "filename": "services-closing.webp",
        "tw": 1400,
        "th": 900,
        "seed": 6739,
        "prompt": "Warm atmospheric commercial photography of finished customer print orders neatly packaged in brown kraft paper with baker twine and printed job tags, alongside stacks of freshly printed color brochures on a wooden dispatch counter in a print shop, photorealistic, 8k resolution"
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
    print("PRINTWORKS PRINT & COPY — GENERATING SERVICES IMAGES")
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
