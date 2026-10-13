/**
 * PRINTWORKS PRINT & COPY — PRICING PAGE JAVASCRIPT
 * Handles pricing desk quick-index scrolling, active section observer,
 * and accessible worksheet interaction.
 */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', () => {
    // ------------------------------------------------------------------------
    // 1. PRICING DESK VERTICAL INDEX OBSERVER & SMOOTH SCROLL
    // ------------------------------------------------------------------------
    const indexLinks = document.querySelectorAll('.pricing-index-item');
    const sectionsToObserve = [
      document.getElementById('printing-prices'),
      document.getElementById('copying-prices'),
      document.getElementById('finishing-prices')
    ].filter(Boolean);

    if (sectionsToObserve.length > 0 && 'IntersectionObserver' in window) {
      const observerOptions = {
        root: null,
        rootMargin: '-20% 0px -60% 0px',
        threshold: 0
      };

      const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const id = entry.target.getAttribute('id');
            indexLinks.forEach((link) => {
              const href = link.getAttribute('href');
              if (href === `#${id}`) {
                link.classList.add('is-active');
              } else if (href && href.startsWith('#')) {
                link.classList.remove('is-active');
              }
            });
          }
        });
      }, observerOptions);

      sectionsToObserve.forEach((sec) => sectionObserver.observe(sec));
    }

    // Smooth scroll with navbar offset compensation
    indexLinks.forEach((link) => {
      const targetId = link.getAttribute('href');
      if (targetId && targetId.startsWith('#')) {
        link.addEventListener('click', (e) => {
          const targetElem = document.querySelector(targetId);
          if (targetElem) {
            e.preventDefault();
            const navbarHeight = 85;
            const targetPos = targetElem.getBoundingClientRect().top + window.scrollY - navbarHeight;
            window.scrollTo({
              top: targetPos,
              behavior: 'smooth'
            });
            // Update focus for keyboard accessibility
            targetElem.setAttribute('tabindex', '-1');
            targetElem.focus({ preventScroll: true });
          }
        });
      }
    });

    // ------------------------------------------------------------------------
    // 2. WORKSHEET PREPARATION ANCHOR PASS-THROUGH
    // ------------------------------------------------------------------------
    const worksheetActionBtn = document.querySelector('.worksheet-action-btn');
    if (worksheetActionBtn) {
      worksheetActionBtn.addEventListener('click', () => {
        // Smoothly guides customer to contact order enquiry form
      });
    }
  });
})();
