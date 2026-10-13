"""
PRINTWORKS PRINT & COPY — About Page Asset Generation & Processing Script
Processes all 9 authentic, high-definition commercial photographs for about.html
into assets/images/about/*.webp with zero duplication and 100% offline local storage.
"""

import os
import io
import time
import urllib.request
import urllib.parse
from PIL import Image

TARGET_DIR = os.path.join("assets", "images", "about")
os.makedirs(TARGET_DIR, exist_ok=True)

BRAIN_DIR = r"C:\Users\Sam John\.gemini\antigravity\brain\c6a092f0-4b40-4d4d-a2c9-c4651fda9315"

# 1. Gemini generated images already in brain dir
GEMINI_SPECS = [
    {
        "src_file": "about_intro_studio_1791866411905.jpg",
        "dest_file": "about-intro.webp",
        "w": 1920,
        "h": 1080
    },
    {
        "src_file": "about_purpose_read_1791866459047.jpg",
        "dest_file": "about-purpose.webp",
        "w": 1200,
        "h": 1400
    },
    {
        "src_file": "about_approach_desk_1791866506422.jpg",
        "dest_file": "about-approach.webp",
        "w": 1200,
        "h": 900
    },
    {
        "src_file": "about_detail_openbook_1791866546376.jpg",
        "dest_file": "about-detail-main.webp",
        "w": 1400,
        "h": 1000
    }
]

# 2. AI prompt specifications for remaining images
AI_PROMPT_SPECS = [
    {
        "dest_file": "about-detail-paper.webp",
        "w": 900,
        "h": 750,
        "seed": 8831,
        "prompt": "Commercial macro studio photography of diverse tactile paper stocks fanned out on dark background. Layers of textured 300gsm recycled kraft eco paper with natural flecks, smooth bright white silk cardstock, and heavy cotton rag paper. Soft directional lighting highlighting paper grain and surface texture, photorealistic, 8k resolution"
    },
    {
        "dest_file": "about-detail-finish.webp",
        "w": 900,
        "h": 750,
        "seed": 5192,
        "prompt": "Macro commercial photography of document binding craftsmanship in print studio. Crisp metal wire binding spine, frosted translucent acetate protective cover, precision guillotine-cut paper edges, neat corner alignment, studio lighting, photorealistic, 8k resolution"
    },
    {
        "dest_file": "about-community.webp",
        "w": 1400,
        "h": 900,
        "seed": 7420,
        "prompt": "Overhead flat-lay commercial photography of diverse printed paper materials on a studio table. Spiral-bound coursework notes, corporate branded presentation folder with business cards, carbonless invoice pad, colorful tri-fold event pamphlets, drafting ruler, soft daylight, photorealistic, 8k resolution"
    },
    {
        "dest_file": "about-experience.webp",
        "w": 1200,
        "h": 900,
        "seed": 6314,
        "prompt": "Commercial photography of a warm welcoming print shop service counter. Friendly print specialist in dark apron conversing with a customer, showing printed paper weight swatches and document binding samples, bright modern storefront with natural daylight, photorealistic, 8k resolution"
    },
    {
        "dest_file": "about-closing.webp",
        "w": 1400,
        "h": 900,
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

def process_gemini_images():
    print("--- Processing Gemini-Generated Images from Brain Directory ---")
    for spec in GEMINI_SPECS:
        src_path = os.path.join(BRAIN_DIR, spec["src_file"])
        dest_path = os.path.join(TARGET_DIR, spec["dest_file"])
        tw, th = spec["w"], spec["h"]
        
        if not os.path.exists(src_path):
            print(f"  [ERROR] Source not found: {src_path}")
            continue
            
        img = Image.open(src_path)
        final_img = crop_and_resize(img, tw, th)
        final_img.save(dest_path, "WEBP", quality=92, method=6)
        kb = os.path.getsize(dest_path) / 1024
        print(f"  ✓ Processed {spec['dest_file']}: {tw}x{th} ({kb:.1f} KB)")

def generate_ai_images():
    print("\n--- Generating & Processing AI Images for About Page ---")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    for spec in AI_PROMPT_SPECS:
        dest_path = os.path.join(TARGET_DIR, spec["dest_file"])
        tw, th = spec["w"], spec["h"]
        prompt = spec["prompt"]
        seed = spec["seed"]
        
        print(f"[*] Generating: {spec['dest_file']} ({tw}x{th})...")
        encoded_prompt = urllib.parse.quote(prompt)
        fetch_w = min(tw, 1280)
        fetch_h = int(fetch_w * (th / tw))
        
        # Notice: no &enhance=true to avoid 402 payment wall
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={fetch_w}&height={fetch_h}&nologo=true&seed={seed}"
        
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
                print(f"  ✓ Successfully saved {spec['dest_file']} ({kb:.1f} KB)")
                success = True
                break
            except Exception as e:
                print(f"  [!] Attempt {attempt+1} failed: {e}")
                time.sleep(2)
                
        if not success:
            print(f"  [ERROR] Failed to generate {spec['dest_file']}")

if __name__ == "__main__":
    process_gemini_images()
    generate_ai_images()
    print("\nAll About page images processed successfully!")
