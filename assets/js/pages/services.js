/**
 * PRINTWORKS PRINT & COPY — SERVICES PAGE JAVASCRIPT
 * Smooth Directory Scrolling, Specification Focus, and Interactive Polish
 */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', () => {
    // ------------------------------------------------------------------------
    // 1. SMOOTH ANCHOR NAVIGATION FOR SERVICE DIRECTORY
    // ------------------------------------------------------------------------
    const directoryLinks = document.querySelectorAll('.sv-index-item, a[href^="#"]:not([href="#"])');
    directoryLinks.forEach((link) => {
      link.addEventListener('click', (e) => {
        const href = link.getAttribute('href');
        if (!href || href === '#' || !href.startsWith('#')) return;
        const targetElement = document.querySelector(href);
        if (targetElement) {
          e.preventDefault();
          targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
          targetElement.focus({ preventScroll: true });
        }
      });
    });

    // ------------------------------------------------------------------------
    // 2. ACCESSIBLE KEYBOARD FOCUS FOR SPECIFICATION MATRIX ROWS
    // ------------------------------------------------------------------------
    const matrixRows = document.querySelectorAll('.sv-matrix-row-card');
    matrixRows.forEach((row) => {
      row.setAttribute('tabindex', '0');
      row.addEventListener('focus', () => {
        row.style.borderColor = 'var(--fg-blue)';
      });
      row.addEventListener('blur', () => {
        row.style.borderColor = '';
      });
    });
  });
})();
