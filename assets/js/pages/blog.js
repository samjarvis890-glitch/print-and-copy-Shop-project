/**
 * PRINTWORKS PRINT & COPY — BLOG JAVASCRIPT
 * Handles Category Filtering, Accessible Editorial Article Reader Modal,
 * Deep-linking via URL hash, Keyboard Navigation, and Reading Progress
 */

(function () {
  'use strict';

  // --------------------------------------------------------------------------
  // ARTICLE REPOSITORY (ORIGINAL EDITORIAL PRINTING GUIDES)
  // --------------------------------------------------------------------------
  const ARTICLES_DATA = {
    'article-paper-selection': {
      category: 'Paper & Materials',
      badgeClass: 'cat-paper',
      title: 'Choosing Paper That Suits Your Print Project',
      readTime: '5 min read',
      lead: 'Paper is never just a passive substrate. Weight, surface texture, bulk, and opacity actively shape how text reads, how colors settle, and how durable the finished piece feels in hand.',
      content: `
        <h3>1. Decoding Paper Weight (GSM)</h3>
        <p>Paper weight is measured in grams per square meter (GSM). For standard everyday correspondence and draft photocopying, 80gsm uncoated bond is standard. However, client-facing reports benefit significantly from 100gsm or 120gsm smooth white stock, which eliminates show-through when printed on both sides.</p>
        <p>For covers, marketing booklets, and presentation leave-behinds, step up to 250gsm–350gsm cardstock. A heavier cover protects inner sheets and provides immediate tactile authority before a single word is read.</p>

        <h3>2. Surface Finishes: Matte, Gloss, and Uncoated</h3>
        <p>The finish dictates how light reflects off ink:</p>
        <ul>
          <li><strong>Silk / Matte:</strong> Offers rich, saturated color reproduction without distracting surface glare. Ideal for catalogs, lookbooks, and high-readability reports.</li>
          <li><strong>Gloss:</strong> Coated to produce high reflective sheen. Colors appear punchy and contrast-heavy, making it suitable for photo-heavy flyers and promotional leaflets.</li>
          <li><strong>Uncoated Bond:</strong> Features natural tooth and organic absorbency. This is the only suitable choice for documents intended to be written on with pen or pencil (such as workbooks, forms, and letterheads).</li>
        </ul>

        <h3>3. Opacity and Bulk</h3>
        <p>Bulk refers to the thickness of a sheet relative to its weight. Highly calendered glossy papers can be surprisingly thin at 130gsm, whereas a high-bulk uncoated 100gsm sheet can feel substantial and prevent back-side toner show-through in duplex printing.</p>

        <div class="fg-article-key-takeaway">
          <h4>Editorial Takeaway</h4>
          <p>Always align your paper selection with user handling: use uncoated 100gsm+ for documents meant to be noted upon, and pair 150gsm silk interior pages with a 300gsm laminated cover for prestige proposals.</p>
        </div>
      `
    },

    'article-file-check': {
      category: 'Document Preparation',
      badgeClass: 'cat-file',
      title: 'The Final File Check Before Printing',
      readTime: '4 min read',
      lead: 'A systematic 5-minute pre-flight check saves hours of reprint delay. Here are the crucial document verification steps every print-ready file requires.',
      content: `
        <h3>1. Check Page Dimensions and Orientation</h3>
        <p>Confirm your document canvas matches standard production sheet sizes (A4: 210 × 297mm, A3: 297 × 420mm) or intended trim size. Submitting a US Letter (8.5 × 11 in) file to an A4 workflow can lead to proportional scaling, resulting in unintended margin compression or tiny text clipping.</p>

        <h3>2. Bleed and Safe Margins</h3>
        <p>If your graphics or background colors run to the page edge, ensure your file includes at least 3mm of bleed beyond the trim line. Keep essential text, pagination numbers, and logos at least 5mm to 8mm inside the trim line (the safe zone) to protect against mechanical trimming tolerances.</p>

        <h3>3. Font Embedding and Vector Outlines</h3>
        <p>When exporting PDFs, always select <em>PDF/X-1a</em> or <em>High Quality Print</em> with font embedding activated. Non-embedded fonts risk defaulting to system fallback typography on print press RIP stations.</p>

        <div class="fg-article-key-takeaway">
          <h4>Editorial Takeaway</h4>
          <p>Always review your exported PDF at 100% zoom with overprint preview turned on. What you see at actual size is the most reliable predictor of final press output.</p>
        </div>
      `
    },

    'article-color-guide': {
      category: 'Printing Basics',
      badgeClass: 'cat-color',
      title: 'Color or Monochrome? Making the Right Choice',
      readTime: '3 min read',
      lead: 'Balancing visual clarity, document purpose, and production costs: when black-and-white excels and when full CMYK is indispensable.',
      content: `
        <h3>1. When Monochrome Delivers Superior Clarity</h3>
        <p>For text-dense agreements, legal filings, lecture packets, and technical manuals, sharp black toner on high-brightness white paper offers the highest contrast and quickest cognitive reading speed. Monochrome production is also markedly more economical for multi-page documents.</p>

        <h3>2. When Full Color is Non-Negotiable</h3>
        <p>Infographics, financial heatmaps, architectural elevations, and branded identity materials rely on color to communicate hierarchy and data relationships. In presentations and sales collateral, full CMYK color creates emotional engagement and conveys professionalism.</p>

        <h3>3. Spot Color and Accent Pages</h3>
        <p>Consider mixed-mode printing: keeping body text in rich crisp black while utilizing vibrant color only on section divider pages and covers. This delivers maximum visual impact while keeping overall page rates balanced.</p>

        <div class="fg-article-key-takeaway">
          <h4>Editorial Takeaway</h4>
          <p>Never rely solely on color to convey critical information; ensure charts and headings have sufficient tonal contrast so they remain legible if photocopied in grayscale.</p>
        </div>
      `
    },

    'article-readiness-guide': {
      category: 'Document Preparation',
      badgeClass: 'cat-file',
      title: 'Before You Print: A Document Readiness Guide',
      readTime: '4 min read',
      lead: 'Essential checklist before exporting your final PDF: resolution thresholds, flattening transparency, color spaces, and page ordering.',
      content: `
        <h3>1. Image Resolution (DPI vs PPI)</h3>
        <p>Web graphics at 72dpi will appear pixelated and fuzzy when transferred to commercial paper. Ensure all embedded raster images are at least 300dpi at their final printed dimensions.</p>

        <h3>2. RGB to CMYK Color Conversion</h3>
        <p>Monitors emit light in RGB, whereas printing presses deposit cyan, magenta, yellow, and black pigments. Converting your artwork to CMYK before hand-off allows you to preview and adjust gamut shifts (such as ultra-bright neon blues and greens) on calibrated screens.</p>

        <h3>3. Flattening and Transparency Layers</h3>
        <p>Complex drop shadows, transparency effects, and layered vector masks should be flattened or exported using modern PDF standards to prevent rasterization stitching lines on laser press rip engines.</p>

        <div class="fg-article-key-takeaway">
          <h4>Editorial Takeaway</h4>
          <p>Supply continuous multi-page documents as a single paginated PDF rather than individual loose pages to preserve intended page sequencing and duplex backing.</p>
        </div>
      `
    },

    'article-duplex-printing': {
      category: 'Printing Basics',
      badgeClass: 'cat-color',
      title: 'Understanding Single-Sided and Double-Sided Printing',
      readTime: '3 min read',
      lead: 'How duplex printing reduces paper bulk, the difference between long-edge and short-edge tumbling, and when single-sided is required.',
      content: `
        <h3>1. Flip on Long Edge vs Flip on Short Edge</h3>
        <p>Duplex printing relies on accurate tumbling alignment:</p>
        <ul>
          <li><strong>Flip on Long Edge:</strong> The standard for portrait documents (books, manuals, reports). Flipping the page horizontally keeps both sides right-side up.</li>
          <li><strong>Flip on Short Edge (Calendar / Notepad style):</strong> Used for landscape booklets, tent cards, or top-bound clipboards.</li>
        </ul>

        <h3>2. Paper Opacity for Double-Sided Jobs</h3>
        <p>Standard 80gsm paper may exhibit faint text ghosting on reverse pages when printing dense imagery. For professional double-sided manuals, 100gsm or 120gsm stock ensures complete opacity and clean contrast.</p>

        <div class="fg-article-key-takeaway">
          <h4>Editorial Takeaway</h4>
          <p>Always specify your binding edge before setting duplex tumbling so that page headers and margins align harmoniously when turned.</p>
        </div>
      `
    },

    'article-study-notes': {
      category: 'Study & Office Guides',
      badgeClass: 'cat-paper',
      title: 'Preparing Study Notes and Office Documents',
      readTime: '4 min read',
      lead: 'Optimal layout techniques for high-retention study materials, meeting handouts, slide decks, and spiral-bound project binders.',
      content: `
        <h3>1. Layouts Designed for Annotation</h3>
        <p>Leave a generous 20mm–25mm outer margin for handwritten margin notes, highlight tabs, or hole punching. Compact 2-up or 4-up slide printouts should feature clean lined memo boxes alongside slides for lecture notes.</p>

        <h3>2. Durable Protective Covers</h3>
        <p>Documents that experience daily backpack or desk handling benefit from a clear frosted acetate front cover and a heavyweight black or navy embossed leatherette backboard with twin-loop wire binding.</p>

        <div class="fg-article-key-takeaway">
          <h4>Editorial Takeaway</h4>
          <p>Opt for durable coil or wire binding for revision notes—it lays flat at 360 degrees, allowing seamless writing on both sides of every page.</p>
        </div>
      `
    },

    'article-binding-finishing': {
      category: 'Finishing & Binding',
      badgeClass: 'cat-binding',
      title: 'Questions to Ask About Binding and Finishing',
      readTime: '5 min read',
      lead: 'From saddle-stitched booklets to twin-loop wire and thermal tape: choosing the right binding method for your page count and longevity.',
      content: `
        <h3>1. Page Count Considerations</h3>
        <p>Binding methods have distinct page capacity constraints:</p>
        <ul>
          <li><strong>Saddle Stitch (Fold & Staple):</strong> Ideal for 8 to 48 pages (must be multiples of 4). Clean, lightweight, and cost-effective.</li>
          <li><strong>Twin-Loop Wire:</strong> Handles 15 to 250 sheets. Provides a crisp corporate look and folds back 360 degrees.</li>
          <li><strong>Plastic Spiral Coil:</strong> Flexible, virtually indestructible, and crush-proof for field manuals and study guides.</li>
          <li><strong>Thermal Spine Tape:</strong> Sleek flat spine suited for legal briefs and executive proposals up to 150 sheets.</li>
        </ul>

        <h3>2. Lamination and Corner Detailing</h3>
        <p>Adding soft-touch matte lamination shields covers against fingerprints and moisture, while rounded corners prevent dog-eared edges on pocket reference cards.</p>

        <div class="fg-article-key-takeaway">
          <h4>Editorial Takeaway</h4>
          <p>Plan page count early: saddle-stitched documents require total page counts divisible by 4, whereas mechanical wire-bound documents accept any even or odd single sheets.</p>
        </div>
      `
    }
  };

  // --------------------------------------------------------------------------
  // INITIALIZATION
  // --------------------------------------------------------------------------
  document.addEventListener('DOMContentLoaded', () => {
    initCategoryFiltering();
    initArticleModal();
    initSmoothScrollLinks();
  });

  // --------------------------------------------------------------------------
  // 1. CATEGORY FILTERING
  // --------------------------------------------------------------------------
  function initCategoryFiltering() {
    const filterBtns = document.querySelectorAll('.fg-topic-filter-btn');
    const topicRows = document.querySelectorAll('.fg-topic-row');
    const articleCards = document.querySelectorAll('[data-category]');
    const emptyNotice = document.getElementById('fg-empty-filter-notice');

    if (!filterBtns.length) return;

    filterBtns.forEach((btn) => {
      btn.addEventListener('click', () => {
        const selectedCat = btn.getAttribute('data-filter') || 'all';

        // Update active button state
        filterBtns.forEach((b) => {
          b.classList.remove('is-active');
          b.setAttribute('aria-pressed', 'false');
        });
        btn.classList.add('is-active');
        btn.setAttribute('aria-pressed', 'true');

        // Filter cards in Section 3 and Section 6
        let visibleCount = 0;
        articleCards.forEach((card) => {
          const cardCat = card.getAttribute('data-category');
          if (selectedCat === 'all' || cardCat === selectedCat) {
            card.style.display = '';
            visibleCount++;
          } else {
            card.style.display = 'none';
          }
        });

        // Highlight matching topic in Section 2
        topicRows.forEach((row) => {
          const rowCat = row.getAttribute('data-category');
          if (selectedCat !== 'all' && rowCat === selectedCat) {
            row.classList.add('is-filtered-match');
          } else {
            row.classList.remove('is-filtered-match');
          }
        });

        // Show/hide empty state message
        if (emptyNotice) {
          emptyNotice.style.display = visibleCount === 0 ? 'block' : 'none';
        }
      });
    });

    // Handle clicks directly on Topic rows in Section 2
    topicRows.forEach((row) => {
      row.addEventListener('click', (e) => {
        e.preventDefault();
        const targetCat = row.getAttribute('data-category');
        if (!targetCat) return;

        // Find matching filter button
        const matchingBtn = document.querySelector(`.fg-topic-filter-btn[data-filter="${targetCat}"]`);
        if (matchingBtn) {
          matchingBtn.click();
        }

        // Smooth scroll to latest articles section
        const targetSection = document.getElementById('latest-articles');
        if (targetSection) {
          targetSection.scrollIntoView({ behavior: 'smooth' });
        }
      });
    });
  }

  // --------------------------------------------------------------------------
  // 2. ARTICLE READER MODAL (ACCESSIBLE IN-PAGE JOURNAL READER)
  // --------------------------------------------------------------------------
  function initArticleModal() {
    const modal = document.getElementById('article-reader-modal');
    if (!modal) return;

    const closeBtn = modal.querySelector('.fg-article-modal-close');
    const badgeEl = modal.querySelector('#reader-badge');
    const timeEl = modal.querySelector('#reader-time');
    const titleEl = modal.querySelector('#reader-title');
    const leadEl = modal.querySelector('#reader-lead');
    const contentEl = modal.querySelector('#reader-content');

    let previousFocusElement = null;

    function openArticle(articleId) {
      const data = ARTICLES_DATA[articleId];
      if (!data) return;

      previousFocusElement = document.activeElement;

      // Populate content
      if (badgeEl) {
        badgeEl.textContent = data.category;
        badgeEl.className = `fg-cat-badge ${data.badgeClass || ''}`;
      }
      if (timeEl) timeEl.textContent = data.readTime;
      if (titleEl) titleEl.textContent = data.title;
      if (leadEl) leadEl.textContent = data.lead;
      if (contentEl) contentEl.innerHTML = data.content;

      // Show modal
      modal.classList.add('is-open');
      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';

      // Update URL hash for addressability
      if (history.pushState) {
        history.pushState(null, null, `#${articleId}`);
      } else {
        location.hash = articleId;
      }

      if (closeBtn) {
        setTimeout(() => closeBtn.focus(), 60);
      }
    }

    function closeArticle() {
      if (!modal.classList.contains('is-open')) return;

      modal.classList.remove('is-open');
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';

      // Clean hash from URL without reloading
      if (history.pushState) {
        history.pushState(null, null, window.location.pathname + window.location.search);
      }

      if (previousFocusElement && typeof previousFocusElement.focus === 'function') {
        previousFocusElement.focus();
      }
    }

    // Bind triggers
    document.querySelectorAll('[data-article-id]').forEach((trigger) => {
      trigger.addEventListener('click', (e) => {
        e.preventDefault();
        const articleId = trigger.getAttribute('data-article-id');
        openArticle(articleId);
      });
    });

    if (closeBtn) {
      closeBtn.addEventListener('click', closeArticle);
    }

    // Close on backdrop click
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeArticle();
      }
    });

    // Close on Escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.classList.contains('is-open')) {
        closeArticle();
      }
    });

    // Check URL hash on page load for deep-linking
    const initialHash = window.location.hash.replace('#', '');
    if (initialHash && ARTICLES_DATA[initialHash]) {
      setTimeout(() => openArticle(initialHash), 100);
    }

    // Handle browser back/forward history
    window.addEventListener('hashchange', () => {
      const hash = window.location.hash.replace('#', '');
      if (hash && ARTICLES_DATA[hash]) {
        openArticle(hash);
      } else {
        closeArticle();
      }
    });
  }

  // --------------------------------------------------------------------------
  // 3. SMOOTH SCROLL LINKS
  // --------------------------------------------------------------------------
  function initSmoothScrollLinks() {
    document.querySelectorAll('a[href^="#"]:not([href="#"])').forEach((anchor) => {
      anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href.startsWith('#article-')) return; // handled by article modal

        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }

})();
