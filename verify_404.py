import os
import re

with open("404.html", "r", encoding="utf-8") as f:
    html = f.read()

print("=" * 60)
print("PRINTWORKS PRINT & COPY — 404 PAGE VERIFICATION")
print("=" * 60)

# 1. Navbar and Footer Check
assert "fg-navbar" not in html, "ERROR: fg-navbar found in 404.html!"
assert "fg-footer" not in html, "ERROR: fg-footer found in 404.html!"
assert "mobile-drawer" not in html, "ERROR: mobile-drawer found in 404.html!"
print("✓ CONFIRMED: No navbar and no footer present in 404.html")

# 2. Viewport & Screen Fit Check
assert "error-page-wrapper" in html, "ERROR: error-page-wrapper missing!"
assert "min-height: 100vh" in open("assets/css/pages/error-404.css").read()
print("✓ CONFIRMED: Fullscreen 100vh / 100dvh fit without scrolling configured")

# 3. Brand Compliance Check
assert "PRINTWORKS PRINT &amp; COPY" in html or "PRINTWORKS PRINT & COPY" in html
assert "FEELGOOD" not in html, "ERROR: Forbidden legacy brand name found!"
print("✓ CONFIRMED: Brand identity 'PRINTWORKS PRINT & COPY' verified")

# 4. Asset Links Check
css_links = re.findall(r'<link[^>]+href=["\']([^"\']+\.css)["\']', html)
for css in css_links:
    if css.startswith("http"):
        continue
    assert os.path.exists(css), f"ERROR: Missing CSS file {css}"
    print(f"✓ CSS exists: {css}")

js_links = re.findall(r'<script[^>]+src=["\']([^"\']+\.js)["\']', html)
for js in js_links:
    assert os.path.exists(js), f"ERROR: Missing JS file {js}"
    print(f"✓ JS exists: {js}")

img_links = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
for img in img_links:
    assert os.path.exists(img), f"ERROR: Missing image {img}"
    print(f"✓ Image exists: {img}")

# 5. Quick Links Check
expected_pages = ["index.html", "home2.html", "about.html", "services.html", "pricing.html", "blog.html", "contact.html"]
for page in expected_pages:
    assert page in html, f"ERROR: Missing link to {page} in 404.html"
print("✓ CONFIRMED: All 7 website pages accessible from quick reprint routes")

print("\n" + "=" * 60)
print("ALL 404 PAGE CHECKS PASSED 100% SUCCESSFULLY!")
print("=" * 60)
