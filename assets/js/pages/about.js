/**
 * PRINTWORKS PRINT & COPY — ABOUT PAGE JAVASCRIPT
 * Accessible Anchor Handling, Sequence Card Focus, and Interactive Polish
 */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', () => {
    // ------------------------------------------------------------------------
    // 1. SMOOTH SCROLLING FOR INTERNAL ANCHORS
    // ------------------------------------------------------------------------
    const internalAnchors = document.querySelectorAll('a[href^="#"]:not([href="#"])');
    internalAnchors.forEach((anchor) => {
      anchor.addEventListener('click', (e) => {
        const targetId = anchor.getAttribute('href');
        if (!targetId || targetId === '#') return;
        const targetEl = document.querySelector(targetId);
        if (targetEl) {
          e.preventDefault();
          targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
          targetEl.focus({ preventScroll: true });
        }
      });
    });

    // ------------------------------------------------------------------------
    // 2. ACCESSIBLE SEQUENCE CARDS INTERACTION (SECTION 3)
    // ------------------------------------------------------------------------
    const sequenceCards = document.querySelectorAll('.ab-sequence-card');
    sequenceCards.forEach((card) => {
      card.setAttribute('tabindex', '0');
      card.addEventListener('focus', () => {
        card.style.borderColor = 'var(--fg-blue)';
      });
      card.addEventListener('blur', () => {
        card.style.borderColor = '';
      });
    });
  });
})();
