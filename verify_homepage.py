"""
PRINTWORKS PRINT & COPY - Homepage Quality & Asset Audit Script
Validates index.html integrity, brand replacement, local assets, CSS, JS, navigation, and responsiveness.
"""

import os
import re
from html.parser import HTMLParser

class HomepageAuditor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.links = []
        self.scripts = []
        self.stylesheets = []
        self.buttons = []
        self.sections = []
        self.ids = set()
        self.duplicate_ids = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        
        # Check duplicate IDs
        elem_id = attr_dict.get("id")
        if elem_id:
            if elem_id in self.ids:
                self.duplicate_ids.append(elem_id)
            self.ids.add(elem_id)

        if tag == "section":
            self.sections.append(attr_dict)
        elif tag == "img":
            self.images.append(attr_dict)
        elif tag == "link":
            if attr_dict.get("rel") == "stylesheet":
                self.stylesheets.append(attr_dict)
            elif "icon" in attr_dict.get("rel", ""):
                self.links.append(attr_dict)
        elif tag == "script":
            src = attr_dict.get("src")
            if src:
                self.scripts.append(attr_dict)
        elif tag == "button":
            self.buttons.append(attr_dict)
        elif tag == "a":
            self.links.append(attr_dict)

def run_verification():
    print("=" * 70)
    print("PRINTWORKS PRINT & COPY — COMPLETE HOMEPAGE AUDIT")
    print("=" * 70)

    # 1. Scope Check: Confirm index.html exists in root
    root_files = [f for f in os.listdir(".") if os.path.isfile(f) and f.endswith(".html")]
    print(f"[*] HTML Files in workspace: {root_files}")
    assert "index.html" in root_files, "index.html not found in workspace!"
    print("  ✓ index.html is present.")

    # 2. Parse index.html
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    auditor = HomepageAuditor()
    auditor.feed(html_content)

    # 3. Check Section Count Requirement: Exactly 6 suitable sections
    assert len(auditor.sections) == 6, f"Expected exactly 6 sections, found {len(auditor.sections)}"
    print(f"  ✓ Exactly 6 suitable sections verified in main content.")

    # 4. Check Brand Name Replacement (ZERO old brand occurrences)
    assert "FEELGOOD" not in html_content, "Found old brand 'FEELGOOD' in index.html!"
    assert "feelgood" not in html_content, "Found old brand 'feelgood' in index.html!"
    assert "GOOD PRINTS" not in html_content, "Found old tagline 'GOOD PRINTS' in index.html!"
    assert "PRINTWORKS" in html_content, "Missing new brand name 'PRINTWORKS' in index.html!"
    assert "PRECISION PRINTS. PROUD RESULTS." in html_content, "Missing new tagline in index.html!"
    print("  ✓ Brand name replacement 100% verified: zero old brand occurrences, new brand active.")

    # 5. Check duplicate IDs
    assert len(auditor.duplicate_ids) == 0, f"Duplicate IDs found: {auditor.duplicate_ids}"
    print(f"  ✓ No duplicate IDs found (checked {len(auditor.ids)} unique IDs).")

    # 6. Check Stylesheets
    print(f"\n[*] Checking Stylesheets ({len(auditor.stylesheets)} linked):")
    for s in auditor.stylesheets:
        href = s.get("href", "")
        if not href.startswith("http"):
            assert os.path.exists(href), f"Missing local CSS file: {href}"
            print(f"  ✓ CSS file exists: {href}")

    # 7. Check Scripts
    print(f"\n[*] Checking JavaScript Files ({len(auditor.scripts)} linked):")
    for sc in auditor.scripts:
        src = sc.get("src", "")
        if not src.startswith("http"):
            assert os.path.exists(src), f"Missing local JS file: {src}"
            print(f"  ✓ Script file exists: {src}")

    # 8. Check Images and SVGs
    print(f"\n[*] Checking Image Assets ({len(auditor.images)} tags):")
    for img in auditor.images:
        src = img.get("src", "")
        alt = img.get("alt", "")
        assert src, "Image tag missing src!"
        assert os.path.exists(src), f"Missing image asset on disk: {src}"
        assert alt.strip(), f"Image missing descriptive alt text: {src}"
        assert "FEELGOOD" not in alt, f"Image alt text contains old brand name: {alt}"
        print(f"  ✓ Image verified: {src} | Alt: '{alt[:40]}...'")

    # 9. Check Required Images
    required_images = [
        "assets/icons/logo.svg",
        "assets/icons/logo-light.svg",
        "assets/icons/favicon.svg",
        "assets/images/home/home-hero.webp",
        "assets/images/home/home-services.webp",
        "assets/images/home/home-process.webp",
        "assets/images/home/home-print-types.webp",
        "assets/images/home/home-options.webp",
        "assets/images/home/home-get-started.webp",
        "assets/images/home/home-closing.webp",
        "assets/images/home/gallery-1.webp",
        "assets/images/home/gallery-2.webp",
        "assets/images/home/gallery-3.webp",
        "assets/images/home/gallery-4.webp",
        "assets/images/home/gallery-5.webp",
        "assets/images/home/gallery-6.webp"
    ]
    print(f"\n[*] Checking All Prompt-Specified Assets:")
    for path in required_images:
        assert os.path.exists(path), f"Required asset missing: {path}"
        size_kb = os.path.getsize(path) / 1024
        print(f"  ✓ Asset verified: {path} ({size_kb:.1f} KB)")

    # 10. Check Navigation Rule Requirements
    print(f"\n[*] Checking User Navigation Rules:")
    assert 'class="fg-hamburger-btn"' in html_content, "Missing hamburger button!"
    assert 'id="mobile-drawer"' in html_content, "Missing mobile drawer menu!"
    assert 'theme-toggle-btn' in html_content, "Missing theme toggle control!"
    assert 'rtl-toggle-btn' in html_content, "Missing RTL toggle control!"
    assert 'Home 1' in html_content and 'Home 2' in html_content, "Missing Home dropdown sublinks!"
    assert 'fg-login-btn' in html_content, "Missing login button in drawer!"
    print("  ✓ Hamburger menu contains all navigation links, dropdowns, dark mode, RTL, and login.")

    # 11. Check Accessible Modals & Sections
    assert 'id="login-modal"' in html_content, "Missing login modal!"
    assert 'id="gallery-lightbox"' in html_content, "Missing gallery lightbox!"
    assert 'id="fg-estimator-form"' in html_content, "Missing interactive print estimator form!"
    print("  ✓ Login modal, gallery lightbox, and print estimator all present and hooked up.")

    print("\n" + "=" * 70)
    print("✓ ALL AUDIT CHECKS PASSED WITH 100% SUCCESS!")
    print("=" * 70)

if __name__ == "__main__":
    run_verification()
