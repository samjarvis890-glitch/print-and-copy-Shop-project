"""
PRINTWORKS PRINT & COPY — About Page Quality & Asset Audit Script
Validates about.html integrity, brand consistency, exact 7 sections, local assets, CSS, JS, navigation, and responsiveness.
"""

import os
import re
from html.parser import HTMLParser

class AboutAuditor(HTMLParser):
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
    print("PRINTWORKS PRINT & COPY — COMPLETE ABOUT PAGE AUDIT")
    print("=" * 70)

    # 1. Existence of about.html
    assert os.path.exists("about.html"), "about.html does not exist!"
    print("  ✓ about.html exists.")

    with open("about.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    auditor = AboutAuditor()
    auditor.feed(html_content)

    # 2. Duplicate IDs check
    if auditor.duplicate_ids:
        print(f"  [ERROR] Duplicate IDs found: {auditor.duplicate_ids}")
        assert False, f"Duplicate IDs: {auditor.duplicate_ids}"
    else:
        print(f"  ✓ No duplicate IDs found (total IDs: {len(auditor.ids)})")

    # 3. Main Sections Check: Exactly 7 content sections
    print(f"[*] Main Content Sections detected: {len(auditor.sections)}")
    for i, sec in enumerate(auditor.sections, 1):
        print(f"    Section {i}: id='{sec.get('id', '')}', class='{sec.get('class', '')}'")
    assert len(auditor.sections) == 7, f"Expected exactly 7 content sections, found {len(auditor.sections)}"
    print("  ✓ Exactly 7 unique main content sections verified.")

    # 4. Images Check
    print(f"[*] Verifying Images referenced in about.html ({len(auditor.images)} total)...")
    forbidden_images = [
        "home-hero.webp", "home-services.webp", "home-process.webp", "home-print-types.webp",
        "home-options.webp", "home-get-started.webp", "home-closing.webp",
        "gallery-1.webp", "gallery-2.webp", "gallery-3.webp", "gallery-4.webp",
        "gallery-5.webp", "gallery-6.webp",
        "home2-hero.webp", "home2-notebook.webp", "home2-paper.webp", "home2-workflow.webp",
        "home2-finishing-main.webp", "home2-finishing-detail.webp", "home2-checklist.webp",
        "home2-closing.webp"
    ]

    for img in auditor.images:
        src = img.get("src")
        assert src, f"Image missing src: {img}"
        
        # Check local existence
        clean_src = src.split("?")[0].replace("/", os.sep)
        assert os.path.exists(clean_src), f"Image does not exist locally: {src}"
        
        # Check that none of the previous images are reused in about content
        base_name = os.path.basename(clean_src)
        if base_name in forbidden_images:
            assert False, f"Previous page image was reused in About page! Reused: {base_name}"
            
        print(f"    ✓ Image OK: {src} (alt='{img.get('alt', '')[:30]}...')")

    # Verify the 9 required About page images exist in assets/images/about/
    required_about_images = [
        "about-intro.webp",
        "about-purpose.webp",
        "about-approach.webp",
        "about-detail-main.webp",
        "about-detail-paper.webp",
        "about-detail-finish.webp",
        "about-community.webp",
        "about-experience.webp",
        "about-closing.webp"
    ]
    for r_img in required_about_images:
        p = os.path.join("assets", "images", "about", r_img)
        assert os.path.exists(p), f"Required About page image missing: {p}"
        print(f"    ✓ Required image present: {p} ({os.path.getsize(p) // 1024} KB)")

    # 5. Check CSS & JS imports
    print("[*] Checking stylesheets and scripts...")
    required_css = ["assets/css/style.css", "assets/css/pages/about.css", "assets/css/responsive.css"]
    for css in required_css:
        assert os.path.exists(css.replace("/", os.sep)), f"CSS file missing: {css}"
        assert css in html_content, f"CSS link missing in about.html: {css}"
        print(f"    ✓ Stylesheet referenced: {css}")

    required_js = ["assets/js/main.js", "assets/js/navigation.js", "assets/js/pages/about.js"]
    for js in required_js:
        assert os.path.exists(js.replace("/", os.sep)), f"JS file missing: {js}"
        assert js in html_content, f"JS script missing in about.html: {js}"
        print(f"    ✓ Script referenced: {js}")

    # 6. Brand Name & Tagline check
    assert "PRINTWORKS PRINT &amp; COPY" in html_content or "PRINTWORKS PRINT & COPY" in html_content
    assert "PRECISION PRINTS. PROUD RESULTS." in html_content
    print("  ✓ Brand name 'PRINTWORKS PRINT & COPY' and tagline 'PRECISION PRINTS. PROUD RESULTS.' confirmed.")

    # 7. Check for forbidden previous brand name
    assert "FEELGOOD" not in html_content.upper(), "Forbidden brand name 'FEELGOOD' found in about.html!"
    print("  ✓ No forbidden legacy brand name found.")

    # 8. Shared Navbar & Footer check
    assert '<header class="fg-navbar"' in html_content, "Shared navbar header tag missing!"
    assert '<footer class="fg-footer"' in html_content, "Shared footer tag missing!"
    assert 'id="mobile-drawer"' in html_content, "Mobile drawer missing!"
    assert 'fg-hamburger-btn' in html_content, "Hamburger button missing!"
    assert 'theme-toggle-btn' in html_content, "Theme toggle button missing!"
    assert 'rtl-toggle-btn' in html_content, "RTL toggle button missing!"
    assert 'id="login-modal"' in html_content, "Login modal missing!"
    print("  ✓ Shared navbar, drawer, theme/RTL toggles, and footer components verified.")

    print("\n" + "=" * 70)
    print("ALL ABOUT PAGE QUALITY & INTEGRITY CHECKS PASSED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    run_verification()
