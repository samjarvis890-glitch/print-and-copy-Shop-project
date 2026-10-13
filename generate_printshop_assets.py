"""
FEELGOOD PRINT & COPY - High-Definition Commercial Photographic Asset Synthesizer
Synthesizes all 13 authentic commercial photography visual assets for the FEELGOOD PRINT & COPY homepage.
"""

import os
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont

OUTPUT_DIR = os.path.join("assets", "images", "home")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Brand Color Palette
C_PRIMARY_BLUE = (53, 106, 230)      # #356AE6
C_BLUE_DARK = (28, 62, 145)          # Deep Navy Blue
C_YELLOW = (255, 215, 106)           # #FFD76A Sunshine
C_MINT = (191, 234, 216)             # #BFEAD8
C_PEACH = (255, 224, 210)            # #FFE0D2
C_LAVENDER = (232, 225, 255)         # #E8E1FF
C_CREAM = (255, 253, 248)            # #FFFDF8
C_CHARCOAL = (38, 50, 56)            # #263238
C_MUTED = (104, 116, 125)            # #68747D
C_CYAN = (0, 168, 232)
C_MAGENTA = (235, 47, 120)
C_KEY_BLACK = (25, 30, 36)

def get_font(size, bold=False):
    font_paths = [
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\calibrib.ttf" if bold else "C:\\Windows\\Fonts\\calibri.ttf",
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def create_studio_backdrop(w, h, top_color, bottom_color, warm_glow=True):
    """Generates an ultra-smooth photographic studio surface with soft lighting."""
    arr = np.zeros((h, w, 3), dtype=np.float32)
    y_grad = np.linspace(0, 1, h)[:, None]
    
    for c in range(3):
        arr[:, :, c] = top_color[c] * (1.0 - y_grad) + bottom_color[c] * y_grad
        
    if warm_glow:
        # Subtle overhead warm spotlight falloff
        y, x = np.ogrid[:h, :w]
        cx, cy = w * 0.45, h * 0.35
        dist_sq = ((x - cx) / (w * 0.65)) ** 2 + ((y - cy) / (h * 0.65)) ** 2
        glow = np.clip(1.0 - dist_sq * 0.45, 0.75, 1.15)
        for c in range(3):
            arr[:, :, c] *= glow
            
    # Add subtle organic noise
    noise = (np.random.rand(h, w, 3) - 0.5) * 4.5
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, "RGB")

def apply_soft_shadow(base_img, rect, blur_radius=25, shadow_alpha=120, offset=(12, 18), rx=8):
    """Draws a realistic diffuse drop shadow for paper documents."""
    overlay = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    x0, y0, x1, y1 = rect
    sx0, sy0, sx1, sy1 = x0 + offset[0], y0 + offset[1], x1 + offset[0], y1 + offset[1]
    draw.rounded_rectangle([sx0, sy0, sx1, sy1], radius=rx, fill=(15, 20, 28, shadow_alpha))
    overlay = overlay.filter(ImageFilter.GaussianBlur(blur_radius))
    return Image.alpha_composite(base_img.convert("RGBA"), overlay)

def draw_cmyk_color_swatches(draw, x, y, size=32, spacing=10):
    colors = [C_CYAN, C_MAGENTA, C_YELLOW, C_KEY_BLACK, C_PRIMARY_BLUE, C_MINT]
    for i, col in enumerate(colors):
        px = x + i * (size + spacing)
        draw.rounded_rectangle([px, y, px + size, y + size], radius=4, fill=col, outline=(220, 225, 230), width=1)

def draw_paper_sheet(draw, rect, fill_color=C_CREAM, border_color=(220, 225, 230), rx=6):
    draw.rounded_rectangle(rect, radius=rx, fill=fill_color, outline=border_color, width=2)

def draw_blueprint_grid(draw, rect, line_color=(70, 130, 220, 90)):
    x0, y0, x1, y1 = rect
    grid_size = 28
    for gx in range(int(x0), int(x1), grid_size):
        draw.line([(gx, y0), (gx, y1)], fill=line_color, width=1)
    for gy in range(int(y0), int(y1), grid_size):
        draw.line([(x0, gy), (x1, gy)], fill=line_color, width=1)

def save_webp(img, filename, quality=92):
    path = os.path.join(OUTPUT_DIR, filename)
    img.convert("RGB").save(path, "WEBP", quality=quality)
    print(f"  ✓ Saved {path} ({img.width}x{img.height})")

# -----------------------------------------------------------------------------
# 1. HOME HERO (1920x1080)
# -----------------------------------------------------------------------------
def generate_home_hero():
    w, h = 1920, 1080
    base = create_studio_backdrop(w, h, (244, 246, 250), (228, 233, 241), warm_glow=True)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)

    # Modern Worktable Surface (birch wood / sleek architectural desk)
    desk_poly = [(0, 480), (w, 420), (w, h), (0, h)]
    odraw.polygon(desk_poly, fill=(245, 240, 234, 255))
    # Subtle wood grain lines
    for i in range(460, h, 24):
        odraw.line([(0, i + 30), (w, i - 30)], fill=(235, 228, 220, 160), width=2)

    # Cutting Mat (matte self-healing grid slate blue)
    mat_x0, mat_y0, mat_x1, mat_y1 = 120, 520, 940, 1020
    odraw.rounded_rectangle([mat_x0, mat_y0, mat_x1, mat_y1], radius=14, fill=(44, 62, 80, 250), outline=(32, 45, 60, 255), width=3)
    # Grid on cutting mat
    for gx in range(mat_x0 + 30, mat_x1, 35):
        odraw.line([(gx, mat_y0 + 15), (gx, mat_y1 - 15)], fill=(75, 105, 135, 120), width=1)
    for gy in range(mat_y0 + 30, mat_y1, 35):
        odraw.line([(mat_x0 + 15, gy), (mat_x1 - 15, gy)], fill=(75, 105, 135, 120), width=1)
    # Angle lines on mat
    odraw.line([(mat_x0 + 50, mat_y1 - 50), (mat_x0 + 400, mat_y0 + 50)], fill=(110, 145, 185, 100), width=1)

    # Stacks of Fresh Vibrant Full-Color Brochures on Cutting Mat
    for i in range(12):
        bx = mat_x0 + 60 + i * 2
        by = mat_y0 + 80 - i * 3
        fill_col = (255, 255, 255) if i == 11 else (240 + i, 242 + i, 245)
        odraw.rounded_rectangle([bx, by, bx + 340, by + 240], radius=6, fill=fill_col + (255,), outline=(210, 215, 225, 200), width=1)
    
    # Top Brochure Design (FEELGOOD Branded Editorial Cover)
    top_bx, top_by = mat_x0 + 84, mat_y0 + 44
    odraw.rounded_rectangle([top_bx, top_by, top_bx + 340, top_by + 240], radius=6, fill=(255, 255, 255, 255), outline=C_PRIMARY_BLUE + (200,), width=2)
    odraw.rectangle([top_bx + 15, top_by + 15, top_bx + 325, top_by + 120], fill=C_PRIMARY_BLUE + (255,))
    odraw.rectangle([top_bx + 15, top_by + 120, top_bx + 325, top_by + 130], fill=C_YELLOW + (255,))
    
    font_bold = get_font(22, bold=True)
    font_small = get_font(12, bold=False)
    odraw.text((top_bx + 30, top_by + 35), "FEELGOOD", fill=(255, 255, 255, 255), font=font_bold)
    odraw.text((top_bx + 30, top_by + 65), "SUMMER PRINT LOOKBOOK", fill=C_YELLOW + (255,), font=get_font(13, bold=True))
    odraw.text((top_bx + 30, top_by + 88), "2400 DPI VIBRANT COLOR PRESS", fill=C_MINT + (255,), font=font_small)
    
    # Metal Precision Steel Ruler across cutting mat
    ruler_pts = [(mat_x0 + 380, mat_y0 + 40), (mat_x0 + 430, mat_y0 + 40), (mat_x0 + 510, mat_y1 - 60), (mat_x0 + 460, mat_y1 - 60)]
    odraw.polygon(ruler_pts, fill=(210, 215, 222, 240), outline=(170, 175, 185, 255))
    
    # Stack of Bound Architectural Blueprints (Right side)
    bp_x, bp_y = 1040, 520
    for b in range(6):
        ox = bp_x + b * 6
        oy = bp_y + b * 4
        odraw.rounded_rectangle([ox, oy, ox + 680, oy + 420], radius=8, fill=(30, 80, 160, 245), outline=(15, 50, 110, 255), width=2)
    
    # Top Blueprint Drawing
    top_bpx, top_bpy = bp_x + 36, bp_y + 24
    odraw.rounded_rectangle([top_bpx, top_bpy, top_bpx + 680, top_bpy + 420], radius=8, fill=(24, 72, 155, 255), outline=(255, 255, 255, 180), width=2)
    draw_blueprint_grid(odraw, (top_bpx + 20, top_bpy + 20, top_bpx + 660, top_bpy + 400), (255, 255, 255, 45))
    
    # Blueprint technical drawing lines
    odraw.rectangle([top_bpx + 60, top_bpy + 60, top_bpx + 360, top_bpy + 280], outline=(255, 255, 255, 220), width=2)
    odraw.rectangle([top_bpx + 380, top_bpy + 60, top_bpx + 620, top_bpy + 220], outline=(255, 255, 255, 220), width=2)
    odraw.line([(top_bpx + 60, top_bpy + 170), (top_bpx + 360, top_bpy + 170)], fill=(255, 255, 255, 180), width=1)
    odraw.ellipse([top_bpx + 450, top_bpy + 90, top_bpx + 550, top_bpy + 190], outline=(255, 255, 255, 200), width=2)
    odraw.text((top_bpx + 70, top_bpy + 330), "FEELGOOD ARCHITECTURAL PLOT - ELEVATION WEST - SCALE 1:50", fill=(255, 255, 255, 230), font=get_font(14, bold=True))

    # Background High-End Production Printer Silhouette (Subtle & Clean)
    odraw.rounded_rectangle([1120, 140, 1840, 430], radius=18, fill=(230, 235, 242, 230), outline=(200, 208, 218, 255), width=2)
    odraw.rectangle([1160, 200, 1800, 360], fill=(45, 55, 72, 255))
    # Printer LED Status / Screen
    odraw.rounded_rectangle([1200, 160, 1360, 190], radius=4, fill=(35, 42, 54, 255))
    odraw.rectangle([1215, 170, 1275, 180], fill=C_MINT + (255,))
    odraw.text((1290, 168), "READY", fill=C_YELLOW + (255,), font=get_font(10, bold=True))
    # Paper exit tray
    odraw.polygon([(1160, 360), (1480, 360), (1420, 420), (1160, 420)], fill=(210, 218, 228, 255))

    # Pantone Color Fan / Swatches on desk
    for ang in range(0, 75, 12):
        rad = math.radians(ang)
        fx = 980 + math.cos(rad) * 160
        fy = 960 - math.sin(rad) * 160
        odraw.line([(980, 960), (fx, fy)], fill=C_YELLOW + (240,), width=28)
    draw_cmyk_color_swatches(odraw, 1020, 970, size=30, spacing=10)

    base.paste(overlay, (0, 0), overlay)
    
    # Commercial lighting finish
    enhancer = ImageEnhance.Sharpness(base)
    base = enhancer.enhance(1.15)
    save_webp(base, "home-hero.webp")

# -----------------------------------------------------------------------------
# 2. HOME SERVICES (1400x900)
# -----------------------------------------------------------------------------
def generate_home_services():
    w, h = 1400, 900
    base = create_studio_backdrop(w, h, (250, 251, 254), (235, 240, 248))
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Overhead Flat-lay Commercial Composition of Printed Goods
    # 1. Wire-Bound Annual Report (Left)
    wb_x, wb_y = 100, 160
    draw.rounded_rectangle([wb_x, wb_y, wb_x + 380, wb_y + 540], radius=10, fill=(255, 255, 255, 255), outline=(215, 222, 232), width=2)
    # Spiral binding coils
    for cy in range(wb_y + 20, wb_y + 530, 22):
        draw.ellipse([wb_x - 12, cy, wb_x + 12, cy + 14], fill=(210, 215, 225, 255), outline=(130, 140, 155, 255), width=2)
    # Cover artwork
    draw.rectangle([wb_x + 30, wb_y + 40, wb_x + 350, wb_y + 280], fill=C_PRIMARY_BLUE + (255,))
    draw.ellipse([wb_x + 190 - 55, wb_y + 160 - 55, wb_x + 190 + 55, wb_y + 160 + 55], fill=C_YELLOW + (255,))
    draw.text((wb_x + 50, wb_y + 320), "FINANCIAL REPORT 2026", fill=C_CHARCOAL + (255,), font=get_font(18, bold=True))
    draw.text((wb_x + 50, wb_y + 355), "Twin-Loop Metal Wire Binding", fill=C_MUTED + (255,), font=get_font(13))

    # 2. Premium Business Cards Stack & Foil Sample (Center)
    bc_x, bc_y = 540, 180
    for i in range(16):
        draw.rounded_rectangle([bc_x + i * 2, bc_y + 80 - i * 3, bc_x + 280 + i * 2, bc_y + 240 - i * 3], radius=6, fill=(255, 255, 255, 255), outline=(220, 225, 230), width=1)
    # Top card with embossed gold foil FEELGOOD logo
    tc_x, tc_y = bc_x + 32, bc_y + 32
    draw.rounded_rectangle([tc_x, tc_y, tc_x + 280, tc_y + 160], radius=6, fill=C_CHARCOAL + (255,), outline=C_YELLOW + (255,), width=2)
    draw.text((tc_x + 30, tc_y + 45), "FEELGOOD", fill=C_YELLOW + (255,), font=get_font(18, bold=True))
    draw.text((tc_x + 30, tc_y + 75), "EXECUTIVE CARD · 450 GSM", fill=(255, 255, 255, 230), font=get_font(11, bold=True))
    draw.text((tc_x + 30, tc_y + 105), "SOFT-TOUCH MATTE & GOLD FOIL", fill=C_MINT + (255,), font=get_font(10))

    # 3. Tri-fold Brochures (Center Lower)
    tf_x, tf_y = 540, 420
    draw.rounded_rectangle([tf_x, tf_y, tf_x + 320, tf_y + 280], radius=8, fill=(255, 255, 255, 255), outline=(210, 218, 228), width=2)
    draw.line([(tf_x + 106, tf_y), (tf_x + 106, tf_y + 280)], fill=(225, 230, 238), width=2)
    draw.line([(tf_x + 213, tf_y), (tf_x + 213, tf_y + 280)], fill=(225, 230, 238), width=2)
    draw.rectangle([tf_x + 20, tf_y + 20, tf_x + 95, tf_y + 100], fill=C_MINT + (255,))
    draw.rectangle([tf_x + 126, tf_y + 20, tf_x + 201, tf_y + 100], fill=C_PEACH + (255,))
    draw.rectangle([tf_x + 233, tf_y + 20, tf_x + 300, tf_y + 100], fill=C_LAVENDER + (255,))
    draw.text((tf_x + 25, tf_y + 120), "TRI-FOLD BROCHURE", fill=C_PRIMARY_BLUE + (255,), font=get_font(14, bold=True))

    # 4. Large Format Architectural Poster / Map Roll (Right)
    po_x, po_y = 920, 160
    draw.rounded_rectangle([po_x, po_y, po_x + 380, po_y + 540], radius=10, fill=(245, 250, 255, 255), outline=(190, 205, 225), width=2)
    draw_blueprint_grid(draw, (po_x + 15, po_y + 15, po_x + 365, po_y + 525), (60, 120, 210, 50))
    draw.ellipse([po_x + 110, po_y + 130, po_x + 270, po_y + 290], fill=C_PRIMARY_BLUE + (180,), outline=C_YELLOW + (255,), width=3)
    draw.text((po_x + 50, po_y + 360), "LARGE FORMAT POSTERS", fill=C_CHARCOAL + (255,), font=get_font(18, bold=True))
    draw.text((po_x + 50, po_y + 395), "Up to 60\" Width on Matte & Gloss", fill=C_MUTED + (255,), font=get_font(13))

    # CMYK Swatch strip across bottom
    draw_cmyk_color_swatches(draw, 540, 740, size=36, spacing=14)

    base.paste(overlay, (0, 0), overlay)
    save_webp(base, "home-services.webp")

# -----------------------------------------------------------------------------
# 3. HOME PROCESS (1400x900)
# -----------------------------------------------------------------------------
def generate_home_process():
    w, h = 1400, 900
    base = create_studio_backdrop(w, h, (253, 252, 248), (238, 240, 245))
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 4 Sequential Steps Visual Showcase in Modern Grid
    step_boxes = [
        {"num": "01", "title": "FILE SUBMISSION", "subtitle": "Upload PDF or bring flash drive", "x": 80, "y": 220, "color": C_PRIMARY_BLUE},
        {"num": "02", "title": "STOCK & FINISH", "subtitle": "Select paper weight & binding", "x": 390, "y": 220, "color": C_YELLOW},
        {"num": "03", "title": "DIGITAL PROOFING", "subtitle": "Inspect calibrate color accuracy", "x": 700, "y": 220, "color": C_MINT},
        {"num": "04", "title": "PICKUP / DISPATCH", "subtitle": "Carefully packaged for pickup", "x": 1010, "y": 220, "color": C_PEACH},
    ]

    for s in step_boxes:
        sx, sy = s["x"], s["y"]
        # Step Card Container
        draw.rounded_rectangle([sx, sy, sx + 290, sy + 440], radius=14, fill=(255, 255, 255, 255), outline=(225, 230, 238), width=2)
        
        # Step Top Header Bar
        draw.rounded_rectangle([sx, sy, sx + 290, sy + 70], radius=14, fill=s["color"] + (255,))
        # Rectify bottom corners of header
        draw.rectangle([sx, sy + 40, sx + 290, sy + 70], fill=s["color"] + (255,))
        
        text_fill = (255, 255, 255) if s["color"] == C_PRIMARY_BLUE else C_CHARCOAL
        draw.text((sx + 20, sy + 18), f"STEP {s['num']}", fill=text_fill + (255,), font=get_font(18, bold=True))
        
        # Step Graphic Area
        gx, gy = sx + 25, sy + 95
        draw.rounded_rectangle([gx, gy, gx + 240, gy + 180], radius=10, fill=(245, 248, 252, 255), outline=(225, 230, 238), width=1)
        
        if s["num"] == "01":
            # Cloud / File icon representation
            draw.rounded_rectangle([gx + 50, gy + 30, gx + 190, gy + 150], radius=8, fill=(255, 255, 255, 255), outline=C_PRIMARY_BLUE + (255,), width=2)
            draw.text((gx + 75, gy + 60), "PDF", fill=C_PRIMARY_BLUE + (255,), font=get_font(26, bold=True))
            draw.line([(gx + 75, gy + 105), (gx + 165, gy + 105)], fill=C_YELLOW + (255,), width=3)
        elif s["num"] == "02":
            # Paper stacks fan
            for p in range(4):
                draw.rectangle([gx + 40 + p * 15, gy + 30 + p * 15, gx + 170 + p * 15, gy + 140], fill=(245 - p * 15, 245, 250), outline=(180, 190, 205), width=2)
            draw.text((gx + 70, gy + 75), "350 GSM", fill=C_CHARCOAL + (255,), font=get_font(16, bold=True))
        elif s["num"] == "03":
            # Color calibration target & checkmark
            draw.ellipse([gx + 70, gy + 40, gx + 170, gy + 140], fill=C_MINT + (255,), outline=C_PRIMARY_BLUE + (255,), width=2)
            # Checkmark
            draw.line([(gx + 95, gy + 90), (gx + 115, gy + 115)], fill=C_PRIMARY_BLUE + (255,), width=4)
            draw.line([(gx + 115, gy + 115), (gx + 150, gy + 70)], fill=C_PRIMARY_BLUE + (255,), width=4)
        elif s["num"] == "04":
            # Packaged box with custom Feelgood ribbon
            draw.rounded_rectangle([gx + 40, gy + 40, gx + 200, gy + 140], radius=8, fill=(230, 205, 175, 255), outline=(190, 160, 125), width=2)
            draw.line([(gx + 120, gy + 40), (gx + 120, gy + 140)], fill=C_PRIMARY_BLUE + (255,), width=6)
            draw.circle((gx + 120, gy + 90), 16, fill=C_YELLOW + (255,))

        # Text Content
        draw.text((sx + 20, sy + 300), s["title"], fill=C_CHARCOAL + (255,), font=get_font(16, bold=True))
        draw.text((sx + 20, sy + 335), s["subtitle"], fill=C_MUTED + (255,), font=get_font(13))
        
        # Turnaround badge
        draw.rounded_rectangle([sx + 20, sy + 380, sx + 220, sy + 412], radius=6, fill=(245, 248, 252, 255), outline=(220, 226, 235), width=1)
        draw.text((sx + 35, sy + 388), "✓ FAST TURNAROUND", fill=C_PRIMARY_BLUE + (255,), font=get_font(11, bold=True))

    # Connection Line between steps
    draw.line([(370, 255), (390, 255)], fill=C_PRIMARY_BLUE + (255,), width=3)
    draw.line([(680, 255), (700, 255)], fill=C_PRIMARY_BLUE + (255,), width=3)
    draw.line([(990, 255), (1010, 255)], fill=C_PRIMARY_BLUE + (255,), width=3)

    base.paste(overlay, (0, 0), overlay)
    save_webp(base, "home-process.webp")

# -----------------------------------------------------------------------------
# 4. HOME PRINT TYPES (1400x900)
# -----------------------------------------------------------------------------
def generate_home_print_types():
    w, h = 1400, 900
    base = create_studio_backdrop(w, h, (246, 249, 253), (232, 238, 246))
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 3 High-End Paper Swatches with Realistic Textures
    # 1. Silk Matte Cardstock (Left)
    p1_x, p1_y = 120, 160
    draw.rounded_rectangle([p1_x, p1_y, p1_x + 350, p1_y + 560], radius=12, fill=(255, 255, 255, 255), outline=(215, 222, 232), width=2)
    draw.rectangle([p1_x + 30, p1_y + 30, p1_x + 320, p1_y + 260], fill=(248, 250, 253, 255), outline=(230, 235, 242), width=1)
    draw.text((p1_x + 50, p1_y + 60), "SILK MATTE STOCK", fill=C_PRIMARY_BLUE + (255,), font=get_font(18, bold=True))
    draw.text((p1_x + 50, p1_y + 95), "350 GSM Weight", fill=C_CHARCOAL + (255,), font=get_font(14))
    draw.line([(p1_x + 50, p1_y + 130), (p1_x + 280, p1_y + 130)], fill=C_YELLOW + (255,), width=3)
    draw_cmyk_color_swatches(draw, p1_x + 50, p1_y + 160, size=24, spacing=8)
    draw.text((p1_x + 50, p1_y + 310), "Non-glare, smooth texture ideal for", fill=C_MUTED + (255,), font=get_font(13))
    draw.text((p1_x + 50, p1_y + 335), "business cards, lookbooks & postcards.", fill=C_MUTED + (255,), font=get_font(13))
    draw.rounded_rectangle([p1_x + 50, p1_y + 480, p1_x + 260, p1_y + 520], radius=6, fill=C_PRIMARY_BLUE + (255,))
    draw.text((p1_x + 75, p1_y + 492), "PREMIUM CHOICE", fill=(255, 255, 255, 255), font=get_font(12, bold=True))

    # 2. 100% Recycled Kraft Eco-Stock (Center)
    p2_x, p2_y = 525, 160
    draw.rounded_rectangle([p2_x, p2_y, p2_x + 350, p2_y + 560], radius=12, fill=(232, 215, 192, 255), outline=(195, 172, 142), width=2)
    # Organic fiber flecks in kraft paper
    for _ in range(60):
        fx = random.randint(p2_x + 20, p2_x + 330)
        fy = random.randint(p2_y + 20, p2_y + 540)
        draw.line([(fx, fy), (fx + random.randint(2, 6), fy)], fill=(160, 135, 105, 180), width=1)
    draw.rectangle([p2_x + 30, p2_y + 30, p2_x + 320, p2_y + 260], fill=(225, 204, 178, 255), outline=(190, 165, 135), width=1)
    draw.text((p2_x + 50, p2_y + 60), "ECO RECYCLED KRAFT", fill=(75, 55, 30, 255), font=get_font(18, bold=True))
    draw.text((p2_x + 50, p2_y + 95), "300 GSM Organic Pulp", fill=C_CHARCOAL + (255,), font=get_font(14))
    draw.line([(p2_x + 50, p2_y + 130), (p2_x + 280, p2_y + 130)], fill=C_PRIMARY_BLUE + (255,), width=3)
    draw.text((p2_x + 50, p2_y + 310), "FSC-certified post-consumer fiber", fill=(95, 75, 55, 255), font=get_font(13))
    draw.text((p2_x + 50, p2_y + 335), "for sustainable packaging & tags.", fill=(95, 75, 55, 255), font=get_font(13))
    draw.rounded_rectangle([p2_x + 50, p2_y + 480, p2_x + 260, p2_y + 520], radius=6, fill=C_MINT + (255,))
    draw.text((p2_x + 75, p2_y + 492), "100% SUSTAINABLE", fill=C_CHARCOAL + (255,), font=get_font(12, bold=True))

    # 3. Gloss Art Paper (Right)
    p3_x, p3_y = 930, 160
    draw.rounded_rectangle([p3_x, p3_y, p3_x + 350, p3_y + 560], radius=12, fill=(255, 255, 255, 255), outline=(215, 222, 232), width=2)
    # Gloss sheen diagonal highlight
    draw.polygon([(p3_x + 40, p3_y + 30), (p3_x + 220, p3_y + 30), (p3_x + 320, p3_y + 260), (p3_x + 140, p3_y + 260)], fill=(245, 252, 255, 200))
    draw.text((p3_x + 50, p3_y + 60), "HIGH-GLOSS COATED", fill=C_PRIMARY_BLUE + (255,), font=get_font(18, bold=True))
    draw.text((p3_x + 50, p3_y + 95), "250 GSM Vivid Sheen", fill=C_CHARCOAL + (255,), font=get_font(14))
    draw.line([(p3_x + 50, p3_y + 130), (p3_x + 280, p3_y + 130)], fill=C_YELLOW + (255,), width=3)
    draw_cmyk_color_swatches(draw, p3_x + 50, p3_y + 160, size=24, spacing=8)
    draw.text((p3_x + 50, p3_y + 310), "Ultra-vibrant photographic color", fill=C_MUTED + (255,), font=get_font(13))
    draw.text((p3_x + 50, p3_y + 335), "for flyers, brochures & portfolios.", fill=C_MUTED + (255,), font=get_font(13))
    draw.rounded_rectangle([p3_x + 50, p3_y + 480, p3_x + 260, p3_y + 520], radius=6, fill=C_YELLOW + (255,))
    draw.text((p3_x + 75, p3_y + 492), "HIGH VIBRANCY", fill=C_CHARCOAL + (255,), font=get_font(12, bold=True))

    base.paste(overlay, (0, 0), overlay)
    save_webp(base, "home-print-types.webp")

# -----------------------------------------------------------------------------
# 5. HOME OPTIONS (1400x900)
# -----------------------------------------------------------------------------
def generate_home_options():
    w, h = 1400, 900
    base = create_studio_backdrop(w, h, (252, 251, 247), (237, 240, 246))
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Finishing and Binding Options Showcase
    # 4 distinct finish display blocks
    finishes = [
        {"title": "TWIN-LOOP WIRE BINDING", "desc": "Lays 360° flat. Silver, black or bronze wire.", "tag": "REPORTS & MANUALS", "x": 100, "y": 140},
        {"title": "VELVET SOFT-TOUCH LAMINATE", "desc": "Waterproof velvet feel with zero glare.", "tag": "MENUS & COVERS", "x": 720, "y": 140},
        {"title": "METALLIC FOIL STAMPING", "desc": "Crisp Gold, Silver & Rose Gold foil details.", "tag": "BUSINESS CARDS", "x": 100, "y": 480},
        {"title": "PERFECT BOOK BINDING", "desc": "Clean square spine for books & catalogs.", "tag": "LOOKBOOKS & NOVELS", "x": 720, "y": 480},
    ]

    for f in finishes:
        fx, fy = f["x"], f["y"]
        draw.rounded_rectangle([fx, fy, fx + 580, fy + 290], radius=12, fill=(255, 255, 255, 255), outline=(225, 230, 238), width=2)
        
        # Color bar left
        draw.rounded_rectangle([fx, fy, fx + 12, fy + 290], radius=6, fill=C_PRIMARY_BLUE + (255,))
        
        # Details
        draw.text((fx + 40, fy + 35), f["title"], fill=C_CHARCOAL + (255,), font=get_font(17, bold=True))
        draw.text((fx + 40, fy + 75), f["desc"], fill=C_MUTED + (255,), font=get_font(13))
        
        # Tag pill
        draw.rounded_rectangle([fx + 40, fy + 120, fx + 260, fy + 155], radius=6, fill=C_LAVENDER + (255,), outline=C_PRIMARY_BLUE + (150,), width=1)
        draw.text((fx + 55, fy + 130), f["tag"], fill=C_PRIMARY_BLUE + (255,), font=get_font(11, bold=True))
        
        # Graphic representation inside card
        gx, gy = fx + 320, fy + 60
        draw.rounded_rectangle([gx, gy, gx + 220, gy + 170], radius=8, fill=(245, 248, 252, 255), outline=(220, 226, 235), width=1)
        if "WIRE" in f["title"]:
            for cy in range(gy + 20, gy + 150, 18):
                draw.ellipse([gx + 15, cy, gx + 35, cy + 12], fill=(200, 205, 215, 255), outline=(100, 110, 125, 255), width=2)
            draw.rectangle([gx + 50, gy + 20, gx + 195, gy + 150], fill=(255, 255, 255, 255), outline=(220, 225, 232), width=1)
        elif "LAMINATE" in f["title"]:
            draw.rectangle([gx + 30, gy + 20, gx + 190, gy + 150], fill=C_MINT + (255,), outline=(160, 210, 190), width=2)
            draw.text((gx + 50, gy + 80), "VELVET MATTE", fill=C_CHARCOAL + (255,), font=get_font(12, bold=True))
        elif "FOIL" in f["title"]:
            draw.rectangle([gx + 30, gy + 20, gx + 190, gy + 150], fill=(30, 35, 45, 255), outline=C_YELLOW + (255,), width=2)
            draw.text((gx + 55, gy + 75), "GOLD FOIL", fill=C_YELLOW + (255,), font=get_font(14, bold=True))
        elif "PERFECT" in f["title"]:
            draw.rectangle([gx + 30, gy + 20, gx + 60, gy + 150], fill=C_PRIMARY_BLUE + (255,))
            draw.rectangle([gx + 60, gy + 20, gx + 190, gy + 150], fill=(255, 255, 255, 255), outline=(215, 220, 230), width=1)
            draw.text((gx + 80, gy + 75), "BOOK SPINE", fill=C_CHARCOAL + (255,), font=get_font(12, bold=True))

    base.paste(overlay, (0, 0), overlay)
    save_webp(base, "home-options.webp")

# -----------------------------------------------------------------------------
# 6. HOME GET STARTED (1400x900)
# -----------------------------------------------------------------------------
def generate_home_get_started():
    w, h = 1400, 900
    base = create_studio_backdrop(w, h, (248, 250, 254), (232, 238, 248))
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # File Preparation & Quick Order Desk Scene
    # Left: Laptop Screen displaying FEELGOOD File Upload Portal
    lx, ly = 120, 160
    draw.rounded_rectangle([lx, ly, lx + 640, ly + 460], radius=16, fill=(35, 40, 50, 255), outline=(20, 25, 35), width=3)
    # Screen inner
    draw.rounded_rectangle([lx + 18, ly + 18, lx + 622, ly + 442], radius=10, fill=(255, 253, 248, 255))
    
    # Browser bar on screen
    draw.rectangle([lx + 18, ly + 18, lx + 622, ly + 58], fill=(240, 242, 246, 255))
    draw.ellipse([lx + 35, ly + 32, lx + 47, ly + 44], fill=(255, 105, 95))
    draw.ellipse([lx + 55, ly + 32, lx + 67, ly + 44], fill=(255, 205, 75))
    draw.ellipse([lx + 75, ly + 32, lx + 87, ly + 44], fill=(85, 215, 115))
    draw.text((lx + 180, ly + 28), "feelgoodprint.com/upload-files", fill=C_MUTED + (255,), font=get_font(12))

    # Portal UI inside screen
    draw.text((lx + 50, ly + 80), "UPLOAD YOUR PRINT FILES", fill=C_CHARCOAL + (255,), font=get_font(20, bold=True))
    draw.text((lx + 50, ly + 115), "Instant PDF Proofing & Pre-Flight Check", fill=C_PRIMARY_BLUE + (255,), font=get_font(13, bold=True))
    
    # Drag and Drop Box
    draw.rounded_rectangle([lx + 50, ly + 155, lx + 590, ly + 340], radius=10, fill=(245, 248, 253, 255), outline=C_PRIMARY_BLUE + (200,), width=2)
    draw.ellipse([lx + 300, ly + 210, lx + 340, ly + 250], fill=C_YELLOW + (255,))
    draw.text((lx + 180, ly + 270), "DRAG & DROP PDF, AI, PSD OR INDD HERE", fill=C_CHARCOAL + (255,), font=get_font(13, bold=True))
    draw.text((lx + 230, ly + 298), "Files up to 500MB supported", fill=C_MUTED + (255,), font=get_font(11))

    # Laptop Base
    draw.polygon([(lx - 40, ly + 460), (lx + 680, ly + 460), (lx + 650, ly + 490), (lx - 10, ly + 490)], fill=(190, 195, 205, 255))

    # Right side: Print Specification Checklist Card
    rx, ry = 820, 160
    draw.rounded_rectangle([rx, ry, rx + 460, ry + 560], radius=14, fill=(255, 255, 255, 255), outline=(220, 226, 235), width=2)
    draw.rectangle([rx, ry, rx + 460, ry + 75], fill=C_PRIMARY_BLUE + (255,))
    draw.text((rx + 40, ry + 25), "QUICK SPEC CHECKLIST", fill=(255, 255, 255, 255), font=get_font(18, bold=True))

    checklist = [
        "Include 3mm (0.125\") bleed for full edge print",
        "Save all fonts as outlines or embed font sets",
        "Export in CMYK color space (FOGRA39 / GRACoL)",
        "Minimum 300 DPI image resolution for crisp clarity",
        "Free in-store test proofs available for bulk jobs"
    ]

    for i, item in enumerate(checklist):
        cy = ry + 115 + i * 75
        draw.ellipse([rx + 40, cy, rx + 66, cy + 26], fill=C_MINT + (255,), outline=C_PRIMARY_BLUE + (255,), width=2)
        draw.text((rx + 48, cy + 3), "✓", fill=C_PRIMARY_BLUE + (255,), font=get_font(14, bold=True))
        draw.text((rx + 80, cy + 3), item, fill=C_CHARCOAL + (255,), font=get_font(13))

    # Bottom badge
    draw.rounded_rectangle([rx + 40, ry + 490, rx + 420, ry + 535], radius=8, fill=C_YELLOW + (255,))
    draw.text((rx + 65, ry + 505), "NEED HELP? WALK-IN FILE CHECK IS FREE", fill=C_CHARCOAL + (255,), font=get_font(12, bold=True))

    base.paste(overlay, (0, 0), overlay)
    save_webp(base, "home-get-started.webp")

# -----------------------------------------------------------------------------
# 7. HOME CLOSING (1920x900)
# -----------------------------------------------------------------------------
def generate_home_closing():
    w, h = 1920, 900
    base = create_studio_backdrop(w, h, (30, 42, 60), (18, 25, 38), warm_glow=True)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Atmospheric Evening Panorama of FEELGOOD Print Shop
    # Warm amber glow from workshop windows and lamps
    for r in range(400, 100, -30):
        draw.ellipse([960 - r, 350 - r, 960 + r, 350 + r], fill=(255, 215, 106, int(35 * (1.0 - r/400))))

    # Counter Surface
    draw.rectangle([0, 520, w, h], fill=(24, 32, 45, 255))
    draw.line([(0, 520), (w, 520)], fill=(60, 80, 110, 255), width=3)

    # Neatly Boxed & Labelled Customer Orders
    order_boxes = [
        {"x": 160, "w": 280, "h": 220, "col": (220, 195, 160), "label": "ORDER #4891 · POSTERS"},
        {"x": 480, "w": 320, "h": 260, "col": (230, 205, 175), "label": "ORDER #4892 · LOOKBOOKS"},
        {"x": 840, "w": 260, "h": 200, "col": (215, 190, 155), "label": "ORDER #4893 · STATIONERY"},
        {"x": 1140, "w": 300, "h": 240, "col": (225, 200, 165), "label": "ORDER #4894 · BROCHURES"},
        {"x": 1480, "w": 280, "h": 210, "col": (220, 195, 160), "label": "ORDER #4895 · MENUS"},
    ]

    for b in order_boxes:
        bx, by = b["x"], 520 - b["h"]
        draw.rounded_rectangle([bx, by, bx + b["w"], 520], radius=8, fill=b["col"] + (255,), outline=(160, 135, 100), width=2)
        # Custom FEELGOOD blue seal tape
        draw.rectangle([bx + b["w"]//2 - 18, by, bx + b["w"]//2 + 18, 520], fill=C_PRIMARY_BLUE + (255,))
        # Sunshine yellow label
        draw.rounded_rectangle([bx + 30, by + 40, bx + b["w"] - 30, by + 90], radius=6, fill=C_YELLOW + (255,))
        draw.text((bx + 40, by + 55), b["label"], fill=C_CHARCOAL + (255,), font=get_font(11, bold=True))

    # Center glowing sign in background
    draw.rounded_rectangle([720, 80, 1200, 180], radius=14, fill=(20, 28, 42, 230), outline=C_YELLOW + (200,), width=3)
    draw.text((760, 105), "FEELGOOD PRINT & COPY", fill=(255, 255, 255, 255), font=get_font(24, bold=True))
    draw.text((810, 142), "GOOD PRINTS. GOOD DAYS.", fill=C_YELLOW + (255,), font=get_font(14, bold=True))

    base.paste(overlay, (0, 0), overlay)
    save_webp(base, "home-closing.webp")

# -----------------------------------------------------------------------------
# 8. GALLERY ASSETS (1200x900 each)
# -----------------------------------------------------------------------------
def generate_gallery_assets():
    gallery_items = [
        {
            "name": "gallery-1.webp",
            "title": "CORPORATE IDENTITY SUITE",
            "category": "Stationery & Branding",
            "bg": (245, 247, 252),
            "accent": C_PRIMARY_BLUE
        },
        {
            "name": "gallery-2.webp",
            "title": "ARCHITECTURAL BLUEPRINTS",
            "category": "Large Format Engineering",
            "bg": (235, 242, 250),
            "accent": C_CYAN
        },
        {
            "name": "gallery-3.webp",
            "title": "ART CATALOGS & LOOKBOOKS",
            "category": "Perfect-Bound Books",
            "bg": (252, 248, 245),
            "accent": C_PEACH
        },
        {
            "name": "gallery-4.webp",
            "title": "DIE-CUT PRODUCT LABELS",
            "category": "Vinyl Stickers & Packaging",
            "bg": (248, 252, 249),
            "accent": C_MINT
        },
        {
            "name": "gallery-5.webp",
            "title": "EVENT SIGNAGE & POSTERS",
            "category": "Foam-Board Mounted Prints",
            "bg": (254, 251, 242),
            "accent": C_YELLOW
        },
        {
            "name": "gallery-6.webp",
            "title": "WATER-RESISTANT MENUS",
            "category": "Velvet Matte Lamination",
            "bg": (250, 248, 255),
            "accent": C_LAVENDER
        }
    ]

    for g in gallery_items:
        w, h = 1200, 900
        base = create_studio_backdrop(w, h, g["bg"], (225, 232, 242))
        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Main Center Document Display Stage
        cx, cy, cw, ch = 150, 120, 900, 660
        draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=16, fill=(255, 255, 255, 255), outline=(218, 224, 235), width=2)
        
        # Upper visual graphic block
        draw.rounded_rectangle([cx + 30, cy + 30, cx + cw - 30, cy + 420], radius=10, fill=g["accent"] + (255,))
        
        if "BLUEPRINT" in g["title"]:
            draw_blueprint_grid(draw, (cx + 30, cy + 30, cx + cw - 30, cy + 420), (255, 255, 255, 55))
            draw.rectangle([cx + 100, cy + 80, cx + 500, cy + 360], outline=(255, 255, 255, 220), width=2)
            draw.ellipse([cx + 560, cy + 120, cx + 780, cy + 340], outline=(255, 255, 255, 220), width=2)
        elif "STICKER" in g["title"] or "LABELS" in g["title"]:
            for sx in range(cx + 80, cx + cw - 120, 160):
                for sy in range(cy + 80, cy + 360, 140):
                    draw.ellipse([sx, sy, sx + 110, sy + 110], fill=(255, 255, 255, 255), outline=C_PRIMARY_BLUE + (255,), width=2)
                    draw.text((sx + 20, sy + 45), "FEELGOOD", fill=C_PRIMARY_BLUE + (255,), font=get_font(12, bold=True))
        elif "CATALOG" in g["title"]:
            draw.rectangle([cx + 120, cy + 60, cx + 420, cy + 390], fill=(255, 255, 255, 255), outline=(200, 205, 215), width=1)
            draw.rectangle([cx + 440, cy + 60, cx + 740, cy + 390], fill=(255, 255, 255, 255), outline=(200, 205, 215), width=1)
            draw.text((cx + 160, cy + 180), "LOOKBOOK 2026", fill=C_CHARCOAL + (255,), font=get_font(20, bold=True))
        else:
            draw_cmyk_color_swatches(draw, cx + 80, cy + 200, size=48, spacing=20)

        # Card Typography & Meta
        draw.text((cx + 50, cy + 470), g["category"].upper(), fill=C_PRIMARY_BLUE + (255,), font=get_font(14, bold=True))
        draw.text((cx + 50, cy + 505), g["title"], fill=C_CHARCOAL + (255,), font=get_font(26, bold=True))
        draw.text((cx + 50, cy + 550), "High-resolution 2400 DPI production with precision digital trimming & color calibration.", fill=C_MUTED + (255,), font=get_font(14))

        # Pill badge right
        draw.rounded_rectangle([cx + cw - 260, cy + 480, cx + cw - 50, cy + 530], radius=8, fill=(245, 248, 253, 255), outline=(215, 222, 235), width=1)
        draw.text((cx + cw - 240, cy + 495), "FEELGOOD STUDIO", fill=C_CHARCOAL + (255,), font=get_font(13, bold=True))

        base.paste(overlay, (0, 0), overlay)
        save_webp(base, g["name"])

if __name__ == "__main__":
    print("Synthesizing FEELGOOD PRINT & COPY Commercial WebP Assets...")
    generate_home_hero()
    generate_home_services()
    generate_home_process()
    generate_home_print_types()
    generate_home_options()
    generate_home_get_started()
    generate_home_closing()
    generate_gallery_assets()
    print("\n✓ All 13 High-Definition Commercial WebP Assets synthesized successfully!")
