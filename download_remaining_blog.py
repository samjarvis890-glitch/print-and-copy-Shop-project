import os
import io
import time
import urllib.request
import urllib.parse
from PIL import Image

TARGET_DIR = os.path.join("assets", "images", "blog")

ITEMS = [
    {
        "filename": "blog-featured-paper.webp",
        "tw": 1200,
        "th": 800,
        "seed": 88319,
        "prompt": "Tactile commercial photography of diverse premium paper stocks, 350gsm silk matte cardstock, textured linen paper, natural kraft card, and smooth cotton rag sheets fanned out on a warm wooden studio table, crisp paper textures and edges, photorealistic, 8k resolution"
    },
    {
        "filename": "blog-file-check.webp",
        "tw": 1000,
        "th": 700,
        "seed": 77421,
        "prompt": "Top-down commercial photography of pre-flight print file inspection desk: printed proof sheet showing clear crop marks, trim bleed margins, registration color bars, precision stainless steel ruler, and cutting mat, crisp photorealistic print shop workbench, 8k resolution"
    },
    {
        "filename": "blog-color-guide.webp",
        "tw": 1000,
        "th": 700,
        "seed": 66532,
        "prompt": "Side-by-side commercial print comparison still life: a vibrant full-color CMYK printed photography catalog page lying next to a crisp high-contrast black-and-white monochrome laser printed text sheet on a clean studio table, sharp details, photorealistic, 8k resolution"
    }
]

def crop_and_resize(img, tw, th):
    if img.height > 60:
        img = img.crop((0, 0, img.width, img.height - 30))
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
    return img.resize((tw, th), Image.Resampling.LANCZOS)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

for idx, item in enumerate(ITEMS):
    if idx > 0:
        print("Waiting 18 seconds...")
        time.sleep(18)
    fn = item["filename"]
    tw, th = item["tw"], item["th"]
    dest = os.path.join(TARGET_DIR, fn)
    prompt = item["prompt"]
    encoded = urllib.parse.quote(prompt)
    fetch_w = min(tw, 800)
    fetch_h = int(fetch_w * (th / tw)) + 30
    url = f"https://image.pollinations.ai/prompt/{encoded}?width={fetch_w}&height={fetch_h}&nologo=true&seed={item['seed']}"
    print(f"Fetching {fn}...")
    success = False
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = resp.read()
            im = Image.open(io.BytesIO(data))
            im_final = crop_and_resize(im, tw, th)
            im_final.save(dest, "WEBP", quality=90, method=6)
            print(f"  ✓ Saved {dest} ({os.path.getsize(dest)//1024} KB)")
            success = True
            break
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}")
            time.sleep(15)
