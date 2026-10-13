"""
PRINTWORKS PRINT & COPY — Blog Page Quality & Asset Audit Script
Validates blog.html integrity, brand consistency, exact 7 sections, local assets, CSS, JS, navigation, and accessibility.
"""

import os
import re
from html.parser import HTMLParser

class BlogAuditor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.links = []
        self.scripts = []
        self.stylesheets = []
        self.buttons = []
        self.sections = []
        self.headings = []
        self.ids = set()
        self.duplicate_ids = []
        self.in_main = False

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        
        elem_id = attr_dict.get("id")
        if elem_id:
            if elem_id in self.ids:
                self.duplicate_ids.append(elem_id)
            self.ids.add(elem_id)

        if tag == "main":
            self.in_main = True

        if tag == "section" and self.in_main:
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
        elif tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            self.headings.append((tag, attr_dict))

    def handle_endtag(self, tag):
        if tag == "main":
            self.in_main = False

def run_verification():
    print("=" * 70)
    print("PRINTWORKS PRINT & COPY — COMPLETE BLOG PAGE AUDIT")
    print("=" * 70)

    # 1. Existence of blog.html
    assert os.path.exists("blog.html"), "blog.html does not exist!"
    print("  ✓ blog.html exists.")

    with open("blog.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    auditor = BlogAuditor()
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
        "blog-masthead",
        "blog-topics",
        "latest-articles",
        "print-anatomy",
        "paper-notes",
        "practical-guides",
        "blog-closing"
    ]
    actual_section_ids = [sec.get('id') for sec in auditor.sections]
    assert actual_section_ids == expected_section_ids, f"Section IDs mismatch! Got: {actual_section_ids}"
    print("  ✓ All 7 expected section IDs match exactly.")

    # 4. Images Check
    print(f"[*] Verifying Images referenced in blog.html ({len(auditor.images)} total)...")
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
        "business-documents.webp", "specification-guide.webp", "services-closing.webp",
        "pricing-intro.webp", "pricing-copying.webp", "pricing-finishing-main.webp",
        "pricing-finishing-detail.webp", "pricing-checklist.webp", "pricing-closing.webp",
        "contact-intro.webp", "contact-process.webp", "contact-details.webp",
        "contact-closing.webp", "contact-map-fallback.webp"
    ]

    seen_content_images = set()
    for img in auditor.images:
        src = img.get("src")
        assert src, f"Image missing src: {img}"
        
        # Check local existence
        clean_src = src.split("?")[0].replace("/", os.sep)
        assert os.path.exists(clean_src), f"Image does not exist locally: {src}"
        
        # Check that none of the previous images are reused in blog content
        base_name = os.path.basename(clean_src)
        if base_name in forbidden_images:
            assert False, f"Previous page image was reused in Blog page! Reused: {base_name}"
        
        if "blog" in base_name:
            assert base_name not in seen_content_images, f"Image reused within blog page: {base_name}"
            seen_content_images.add(base_name)
            
        print(f"    ✓ Image OK: {src} (alt='{img.get('alt', '')[:35]}...')")

    # Verify required blog images exist in assets/images/blog/
    required_blog_images = [
        "blog-masthead.webp",
        "blog-featured-paper.webp",
        "blog-file-check.webp",
        "blog-color-guide.webp",
        "blog-process-file.webp",
        "blog-process-paper.webp",
        "blog-process-output.webp",
        "blog-paper-notes.webp",
        "blog-guide-readiness.webp",
        "blog-guide-duplex.webp",
        "blog-guide-studynotes.webp",
        "blog-guide-binding.webp",
        "blog-closing.webp"
    ]
    for r_img in required_blog_images:
        p = os.path.join("assets", "images", "blog", r_img)
        assert os.path.exists(p), f"Required Blog page image missing: {p}"
        print(f"    ✓ Required image present: {p} ({os.path.getsize(p) // 1024} KB)")

    # 5. Check CSS & JS imports
    print("[*] Checking stylesheets and scripts...")
    required_css = ["assets/css/style.css", "assets/css/pages/blog.css", "assets/css/responsive.css"]
    actual_css = [s.get("href") for s in auditor.stylesheets]
    for css in required_css:
        assert css in actual_css, f"Missing stylesheet: {css}"
        assert os.path.exists(css.replace("/", os.sep)), f"Local stylesheet does not exist: {css}"
        print(f"    ✓ CSS import verified: {css}")

    required_js = ["assets/js/main.js", "assets/js/navigation.js", "assets/js/pages/blog.js"]
    actual_js = [s.get("src") for s in auditor.scripts]
    for js in required_js:
        assert js in actual_js, f"Missing script: {js}"
        assert os.path.exists(js.replace("/", os.sep)), f"Local script does not exist: {js}"
        print(f"    ✓ Script verified: {js}")

    # 6. Navbar & Active Link Check
    print("[*] Checking Navigation elements...")
    assert 'class="fg-nav-link active"' in html_content or 'class="fg-nav-link active" aria-current="page"' in html_content, "Blog nav link not marked active!"
    assert 'class="fg-drawer-link active"' in html_content or 'class="fg-drawer-link active" aria-current="page"' in html_content, "Blog mobile drawer link not marked active!"
    assert 'href="index.html"' in html_content, "Missing link to index.html"
    assert 'href="home2.html"' in html_content, "Missing link to home2.html"
    assert 'href="about.html"' in html_content, "Missing link to about.html"
    assert 'href="services.html"' in html_content, "Missing link to services.html"
    assert 'href="pricing.html"' in html_content, "Missing link to pricing.html"
    assert 'href="contact.html"' in html_content, "Missing link to contact.html"
    print("  ✓ All navigation links and active states verified.")

    # 7. Brand Check
    print("[*] Checking Brand Consistency...")
    assert "PRINTWORKS PRINT &amp; COPY" in html_content or "PRINTWORKS PRINT & COPY" in html_content, "Brand name mismatch!"
    assert "PRECISION PRINTS. PROUD RESULTS." in html_content, "Tagline missing in footer!"
    print("  ✓ Brand identity and tagline verified.")

    # 8. Single H1 Check
    h1s = [h for h in auditor.headings if h[0] == "h1"]
    assert len(h1s) == 1, f"Expected exactly 1 H1 heading, found {len(h1s)}"
    print(f"  ✓ Exactly 1 H1 heading verified.")

    # 9. Six Categories in Section 2 Check
    import html
    decoded_html = html.unescape(html_content)
    for cat in ["Printing Basics", "Paper & Materials", "Document Preparation", "Finishing & Binding", "Business Printing", "Study & Office Guides"]:
        assert cat in decoded_html, f"Missing category: {cat}"
    print("  ✓ All 6 required categories present.")

    # 10. Article Content & Reader Modal
    assert 'id="article-reader-modal"' in html_content, "Article reader modal missing!"
    for art_id in [
        "article-paper-selection",
        "article-file-check",
        "article-color-guide",
        "article-readiness-guide",
        "article-duplex-printing",
        "article-study-notes",
        "article-binding-finishing"
    ]:
        assert art_id in html_content, f"Missing article anchor/trigger: {art_id}"
    print("  ✓ Article reader modal and all 7 article triggers verified.")

    print("=" * 70)
    print("AUDIT SUCCESSFUL: 100% COMPLIANT WITH ALL REQUIREMENTS!")
    print("=" * 70)

if __name__ == "__main__":
    run_verification()
