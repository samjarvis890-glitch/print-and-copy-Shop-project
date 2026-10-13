"""
PRINTWORKS PRINT & COPY — Pricing Page Quality & Asset Audit Script
Validates pricing.html integrity, brand consistency, exact 7 sections, local assets, CSS, JS, navigation, zero fake prices, and responsiveness.
"""

import os
import re
from html.parser import HTMLParser

class PricingAuditor(HTMLParser):
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
    print("PRINTWORKS PRINT & COPY — COMPLETE PRICING PAGE AUDIT")
    print("=" * 70)

    # 1. Existence of pricing.html
    assert os.path.exists("pricing.html"), "pricing.html does not exist!"
    print("  ✓ pricing.html exists.")

    with open("pricing.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    auditor = PricingAuditor()
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

    expected_section_ids = [
        "pricing-intro",
        "printing-prices",
        "copying-prices",
        "finishing-prices",
        "quote-factors",
        "quote-preparation",
        "pricing-closing"
    ]
    actual_section_ids = [sec.get('id') for sec in auditor.sections]
    assert actual_section_ids == expected_section_ids, f"Section IDs mismatch! Got: {actual_section_ids}"
    print("  ✓ All 7 expected section IDs match exactly.")

    # 4. Images Check
    print(f"[*] Verifying Images referenced in pricing.html ({len(auditor.images)} total)...")
    forbidden_images = [
        "home-hero.webp", "home-services.webp", "home-process.webp", "home-print-types.webp",
        "home-options.webp", "home-get-started.webp", "home-closing.webp",
        "gallery-1.webp", "gallery-2.webp", "gallery-3.webp", "gallery-4.webp",
        "gallery-5.webp", "gallery-6.webp",
        "home2-hero.webp", "home2-notebook.webp", "home2-paper.webp", "home2-workflow.webp",
        "home2-finishing-main.webp", "home2-finishing-detail.webp", "home2-checklist.webp",
        "home2-closing.webp",
        "about-intro.webp", "about-purpose.webp", "about-approach.webp", "about-detail-main.webp",
        "about-detail-paper.webp", "about-detail-finish.webp", "about-community.webp",
        "about-experience.webp", "about-closing.webp",
        "services-intro.webp", "document-printing.webp", "photocopying.webp", "binding-main.webp",
        "binding-detail.webp", "finished-documents.webp", "study-documents.webp",
        "business-documents.webp", "specification-guide.webp", "services-closing.webp"
    ]

    seen_content_images = set()
    for img in auditor.images:
        src = img.get("src")
        assert src, f"Image missing src: {img}"
        
        # Check local existence
        clean_src = src.split("?")[0].replace("/", os.sep)
        assert os.path.exists(clean_src), f"Image does not exist locally: {src}"
        
        # Check that none of the previous images are reused in pricing content
        base_name = os.path.basename(clean_src)
        if base_name in forbidden_images:
            assert False, f"Previous page image was reused in Pricing page! Reused: {base_name}"
        
        if "pricing" in base_name:
            assert base_name not in seen_content_images, f"Image reused within pricing page: {base_name}"
            seen_content_images.add(base_name)
            
        print(f"    ✓ Image OK: {src} (alt='{img.get('alt', '')[:30]}...')")

    # Verify all 6 required pricing images exist in assets/images/pricing/
    required_pricing_images = [
        "pricing-intro.webp",
        "pricing-copying.webp",
        "pricing-finishing-main.webp",
        "pricing-finishing-detail.webp",
        "pricing-checklist.webp",
        "pricing-closing.webp"
    ]
    for r_img in required_pricing_images:
        p = os.path.join("assets", "images", "pricing", r_img)
        assert os.path.exists(p), f"Required Pricing page image missing: {p}"
        print(f"    ✓ Required image present: {p} ({os.path.getsize(p) // 1024} KB)")

    # 5. Check CSS & JS imports
    print("[*] Checking stylesheets and scripts...")
    required_css = ["assets/css/style.css", "assets/css/pages/pricing.css", "assets/css/responsive.css"]
    for css in required_css:
        assert os.path.exists(css.replace("/", os.sep)), f"CSS file missing: {css}"
        assert css in html_content, f"CSS link missing in pricing.html: {css}"
        print(f"    ✓ Stylesheet referenced: {css}")

    required_js = ["assets/js/main.js", "assets/js/navigation.js", "assets/js/pages/pricing.js"]
    for js in required_js:
        assert os.path.exists(js.replace("/", os.sep)), f"JS file missing: {js}"
        assert js in html_content, f"JS script missing in pricing.html: {js}"
        print(f"    ✓ Script referenced: {js}")

    # 6. Brand Name & Tagline check
    assert "PRINTWORKS PRINT &amp; COPY" in html_content or "PRINTWORKS PRINT & COPY" in html_content
    assert "PRECISION PRINTS. PROUD RESULTS." in html_content
    print("  ✓ Brand name 'PRINTWORKS PRINT & COPY' and tagline 'PRECISION PRINTS. PROUD RESULTS.' confirmed.")

    # 7. Check for forbidden previous brand name
    assert "FEELGOOD" not in html_content.upper(), "Forbidden brand name 'FEELGOOD' found in pricing.html!"
    print("  ✓ No forbidden legacy brand name found.")

    # 8. Shared Navbar & Footer check
    assert '<header class="fg-navbar"' in html_content, "Shared navbar header tag missing!"
    assert '<footer class="fg-footer"' in html_content, "Shared footer tag missing!"
    assert 'id="mobile-drawer"' in html_content, "Mobile drawer missing!"
    assert 'fg-hamburger-btn' in html_content, "Hamburger button missing!"
    assert 'theme-toggle-btn' in html_content, "Theme toggle button missing!"
    assert 'rtl-toggle-btn' in html_content, "RTL toggle button missing!"
    assert 'id="login-modal"' in html_content, "Login modal missing!"
    assert 'pricing.html" class="fg-nav-link active"' in html_content, "Pricing nav link not active!"
    assert 'pricing.html" class="fg-drawer-link active"' in html_content, "Pricing drawer link not active!"
    print("  ✓ Shared navbar, drawer, theme/RTL toggles, active pricing state, and footer components verified.")

    # 9. No fake prices check
    assert "$" not in html_content, "Fake dollar prices found in pricing.html!"
    assert "£" not in html_content, "Fake pound prices found in pricing.html!"
    assert "€" not in html_content, "Fake euro prices found in pricing.html!"
    assert "Confirm current rate" in html_content
    assert "Quotation required" in html_content
    assert "Depends on specifications" in html_content
    print("  ✓ Honest non-numerical pricing badges verified without fake currency amounts.")

    print("\n" + "=" * 70)
    print("ALL PRICING PAGE QUALITY & INTEGRITY CHECKS PASSED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    run_verification()
