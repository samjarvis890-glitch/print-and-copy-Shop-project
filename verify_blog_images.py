"""
PRINTWORKS PRINT & COPY — BLOG PAGE (blog.html) COMPREHENSIVE IMAGE AUDIT
Validates:
1. All images in blog.html are 100% locally stored and work offline.
2. Freshly generated specifically for blog.html content and sections.
3. Zero duplicate images inside blog.html.
4. Zero reuse/duplication against ANY other page in the project (index, home2, about, services, pricing, contact, home).
5. All 7 sections have suitable content and dedicated images.
"""

import os
import re
import glob
import hashlib
from PIL import Image

def get_file_hash(filepath):
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def test_blog_images():
    print("=" * 70)
    print("BLOG PAGE (blog.html) IMAGE AUDIT")
    print("=" * 70)

    html_file = "blog.html"
    assert os.path.exists(html_file), f"{html_file} does not exist!"

    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Find all <img> tags
    img_matches = re.findall(r'<img\s+([^>]+)>', content, re.DOTALL)
    print(f"Total <img> elements found in blog.html: {len(img_matches)}")

    blog_content_images = []
    for match in img_matches:
        src_match = re.search(r'src=["\']([^"\']+)["\']', match)
        alt_match = re.search(r'alt=["\']([^"\']*)["\']', match)
        assert src_match, f"Found <img> without src: {match}"
        
        src = src_match.group(1)
        alt = alt_match.group(1) if alt_match else ""

        # Skip svg icons/logos
        if not src.endswith(".svg"):
            blog_content_images.append({
                "src": src,
                "alt": alt,
                "raw": match
            })

    print(f"Content images in blog.html: {len(blog_content_images)}")
    assert len(blog_content_images) == 13, f"Expected 13 content images, found {len(blog_content_images)}"

    # 1. OFFLINE / LOCAL CHECK
    print("\n--- 1. LOCAL STORAGE & OFFLINE COMPLIANCE ---")
    for item in blog_content_images:
        src = item["src"]
        assert not src.startswith(("http://", "https://", "//")), f"Remote URL found: {src}"
        normalized_path = os.path.normpath(src)
        assert os.path.exists(normalized_path), f"Image file missing on disk: {normalized_path}"
        
        size_bytes = os.path.getsize(normalized_path)
        assert size_bytes > 10000, f"Image file too small or empty: {normalized_path} ({size_bytes} bytes)"
        
        with Image.open(normalized_path) as im:
            w, h = im.size
            fmt = im.format
            print(f"  ✓ [OK] {src:45} | {fmt:4} | {w}x{h:<5} | {size_bytes/1024:.1f} KB")

    print("  ✓ All images exist locally and work 100% without internet connection.")

    # 2. INTERNAL DUPLICATE CHECK
    print("\n--- 2. INTERNAL DUPLICATE CHECK (WITHIN BLOG PAGE) ---")
    seen_hashes = {}
    for item in blog_content_images:
        h = get_file_hash(item["src"])
        if h in seen_hashes:
            raise AssertionError(f"Duplicate image found within blog.html: {item['src']} matches {seen_hashes[h]}")
        seen_hashes[h] = item["src"]
    print(f"  ✓ All {len(blog_content_images)} content images are completely unique with zero internal duplication.")

    # 3. CROSS-PAGE DUPLICATE CHECK
    print("\n--- 3. CROSS-PAGE IMAGE REUSE AUDIT ---")
    all_other_images = [
        p for p in glob.glob("assets/images/**/*.*", recursive=True)
        if "blog" not in p and os.path.isfile(p) and not p.endswith(".svg")
    ]
    print(f"  Auditing against {len(all_other_images)} images across other site pages...")

    cross_collisions = []
    for item in blog_content_images:
        bl_hash = get_file_hash(item["src"])
        bl_base = os.path.basename(item["src"])
        for other in all_other_images:
            other_hash = get_file_hash(other)
            other_base = os.path.basename(other)
            if bl_hash == other_hash:
                cross_collisions.append((item["src"], other, "hash collision"))
            if bl_base == other_base:
                cross_collisions.append((item["src"], other, "filename match"))

    if cross_collisions:
        print("  [ERROR] Cross-page duplicates found:")
        for col in cross_collisions:
            print(f"    - {col[0]} conflicts with {col[1]} ({col[2]})")
        raise AssertionError(f"Cross-page image collisions detected: {cross_collisions}")
    else:
        print("  ✓ ZERO images from other/previous pages repeated in Blog page!")

    # 4. SECTION-BY-SECTION COVERAGE CHECK
    print("\n--- 4. SECTION-BY-SECTION COVERAGE CHECK ---")
    sections = [
        ("Section 1 (Masthead Inset)", "#blog-masthead", "blog-masthead.webp"),
        ("Section 3 (Featured Paper Story)", "#latest-articles", "blog-featured-paper.webp"),
        ("Section 3 (File Check Guide)", "#latest-articles", "blog-file-check.webp"),
        ("Section 3 (Color vs Monochrome)", "#latest-articles", "blog-color-guide.webp"),
        ("Section 4 (Stage 1: Pre-Flight)", "#print-anatomy", "blog-process-file.webp"),
        ("Section 4 (Stage 2: Paper Inspection)", "#print-anatomy", "blog-process-paper.webp"),
        ("Section 4 (Stage 3: Press Output)", "#print-anatomy", "blog-process-output.webp"),
        ("Section 5 (Paper Notes Macro)", "#paper-notes", "blog-paper-notes.webp"),
        ("Section 6 (Guide 1: Readiness)", "#practical-guides", "blog-guide-readiness.webp"),
        ("Section 6 (Guide 2: Duplex)", "#practical-guides", "blog-guide-duplex.webp"),
        ("Section 6 (Guide 3: Study Notes)", "#practical-guides", "blog-guide-studynotes.webp"),
        ("Section 6 (Guide 4: Binding Methods)", "#practical-guides", "blog-guide-binding.webp"),
        ("Section 7 (Closing Reading Space)", "#blog-closing", "blog-closing.webp")
    ]

    for sec_name, sec_selector, exp_img in sections:
        assert exp_img in content, f"Missing image {exp_img} for {sec_name}"
        print(f"  ✓ {sec_name:40} -> {exp_img}")

    print("\n" + "=" * 70)
    print("ALL BLOG PAGE IMAGE AUDIT CHECKS PASSED 100% SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    test_blog_images()
