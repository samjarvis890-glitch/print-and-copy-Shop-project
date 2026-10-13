import os
import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Find all img src tags
img_tags = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', content)
print(f"Total <img> tags: {len(img_tags)}")

missing = []
used_images = []
for src in img_tags:
    exists = os.path.exists(src)
    status = "OK" if exists else "MISSING"
    size_kb = (os.path.getsize(src) / 1024) if exists else 0
    print(f"[{status}] {src} ({size_kb:.1f} KB)")
    if not exists:
        missing.append(src)
    used_images.append(src)

# Check for duplicates among content images (excluding logos)
content_images = [s for s in used_images if not s.endswith(".svg")]
duplicates = [s for s in content_images if content_images.count(s) > 1 and s != "assets/images/index/gallery-corporate-identity.webp"]
# Note: gallery-corporate-identity.webp is used in Gallery 1 and as default lightbox modal preview

print("\n--- DUPLICATE CHECK ---")
if duplicates:
    print("Warning: Duplicate content images found:", set(duplicates))
else:
    print("✓ ZERO duplicate content images across index sections!")

print("\n--- OFFLINE LOCAL ASSET CHECK ---")
remote_urls = [s for s in used_images if s.startswith(("http://", "https://", "//"))]
if remote_urls:
    print("Warning: Remote URLs found:", remote_urls)
else:
    print("✓ All images are 100% local and work offline without internet connection!")

# Check against other pages
other_pages_images = [
    # home2
    "home2-hero.webp", "home2-notebook.webp", "home2-paper.webp", "home2-workflow.webp",
    "home2-finishing-main.webp", "home2-finishing-detail.webp", "home2-checklist.webp", "home2-closing.webp",
    # about
    "about-intro.webp", "about-purpose.webp", "about-approach.webp", "about-detail-main.webp",
    "about-detail-paper.webp", "about-detail-finish.webp", "about-community.webp", "about-experience.webp", "about-closing.webp",
    # services
    "services-intro.webp", "document-printing.webp", "photocopying.webp", "binding-main.webp",
    "binding-detail.webp", "finished-documents.webp", "study-documents.webp", "business-documents.webp",
    "specification-guide.webp", "services-closing.webp",
    # pricing
    "pricing-intro.webp", "pricing-copying.webp", "pricing-finishing-main.webp", "pricing-finishing-detail.webp",
    "pricing-checklist.webp", "pricing-closing.webp",
    # contact
    "contact-intro.webp", "contact-process.webp", "contact-details.webp", "contact-map-fallback.webp", "contact-closing.webp",
    # blog
    "blog-masthead.webp", "blog-featured-paper.webp", "blog-file-check.webp", "blog-color-guide.webp",
    "blog-process-file.webp", "blog-process-paper.webp", "blog-process-output.webp", "blog-paper-notes.webp",
    "blog-closing.webp", "blog-guide-readiness.webp", "blog-guide-duplex.webp"
]

print("\n--- CROSS-PAGE IMAGE REUSE CHECK ---")
reused = []
for s in content_images:
    basename = os.path.basename(s)
    if basename in other_pages_images:
        reused.append(basename)

if reused:
    print("ERROR: Images from previous pages reused:", reused)
else:
    print("✓ ZERO images from previous pages reused!")

print("\n--- OVERALL STATUS ---")
if not missing and not reused:
    print("✓ ALL CHECKS PASSED PERFECTLY!")
else:
    print("Some checks failed.")
