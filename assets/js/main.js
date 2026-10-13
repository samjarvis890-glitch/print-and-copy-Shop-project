/**
 * PRINTWORKS PRINT & COPY — MAIN JAVASCRIPT
 * Handles Theme Toggling (Dark/Light), RTL/LTR Switching, Interactive Print Estimator,
 * FAQ Accordion, and Global Utilities
 */

(function () {
  'use strict';

  // --------------------------------------------------------------------------
  // 1. THEME MANAGEMENT (Dark / Light Mode)
  // --------------------------------------------------------------------------
  const THEME_KEY = 'printworks_theme';

  function getPreferredTheme() {
    const savedTheme = localStorage.getItem(THEME_KEY);
    if (savedTheme) {
      return savedTheme;
    }
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light';
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(THEME_KEY, theme);

    // Update all theme toggle buttons
    const themeButtons = document.querySelectorAll('.theme-toggle-btn');
    themeButtons.forEach((btn) => {
      const icon = btn.querySelector('i');
      if (icon) {
        if (theme === 'dark') {
          icon.className = 'bi bi-sun-fill';
          btn.setAttribute('aria-label', 'Switch to light mode');
          btn.setAttribute('title', 'Switch to light mode');
        } else {
          icon.className = 'bi bi-moon-stars-fill';
          btn.setAttribute('aria-label', 'Switch to dark mode');
          btn.setAttribute('title', 'Switch to dark mode');
        }
      }
    });
  }

  function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme);
  }

  // --------------------------------------------------------------------------
  // 2. DIRECTION MANAGEMENT (RTL / LTR)
  // --------------------------------------------------------------------------
  const DIR_KEY = 'printworks_dir';

  function getPreferredDir() {
    return localStorage.getItem(DIR_KEY) || 'ltr';
  }

  function applyDir(dir) {
    document.documentElement.setAttribute('dir', dir);
    document.documentElement.setAttribute('lang', dir === 'rtl' ? 'ar' : 'en');
    localStorage.setItem(DIR_KEY, dir);

    const rtlButtons = document.querySelectorAll('.rtl-toggle-btn');
    rtlButtons.forEach((btn) => {
      btn.setAttribute('aria-label', dir === 'rtl' ? 'Switch to Left to Right' : 'Switch to Right to Left');
      btn.setAttribute('title', dir === 'rtl' ? 'LTR View' : 'RTL View');
    });
  }

  function toggleDir() {
    const currentDir = document.documentElement.getAttribute('dir') || 'ltr';
    const newDir = currentDir === 'rtl' ? 'ltr' : 'rtl';
    applyDir(newDir);
  }

  // --------------------------------------------------------------------------
  // 3. INTERACTIVE PRINT ESTIMATOR CALCULATOR
  // --------------------------------------------------------------------------
  function initPrintEstimator() {
    const form = document.getElementById('fg-estimator-form');
    const priceDisplay = document.getElementById('calc-price-display');
    const turnaroundBadge = document.getElementById('calc-turnaround-badge');
    if (!form || !priceDisplay) return;

    function calculateEstimate() {
      const serviceType = document.getElementById('calc-service')?.value || 'document';
      const paperStock = document.getElementById('calc-stock')?.value || 'silk';
      const quantity = parseInt(document.getElementById('calc-quantity')?.value, 10) || 50;
      const binding = document.getElementById('calc-binding')?.value || 'none';
      const speed = document.getElementById('calc-speed')?.value || 'standard';

      // Base Rates
      let baseRatePerUnit = 0.15;
      let setupFee = 5.0;

      switch (serviceType) {
        case 'document':
          baseRatePerUnit = 0.12;
          setupFee = 2.0;
          break;
        case 'booklet':
          baseRatePerUnit = 3.80;
          setupFee = 15.0;
          break;
        case 'blueprint':
          baseRatePerUnit = 5.50;
          setupFee = 6.0;
          break;
        case 'business_cards':
          baseRatePerUnit = 0.28;
          setupFee = 10.0;
          break;
        case 'posters':
          baseRatePerUnit = 14.00;
          setupFee = 8.0;
          break;
        case 'stickers':
          baseRatePerUnit = 0.45;
          setupFee = 12.0;
          break;
      }

      // Paper Stock Multiplier
      let stockMultiplier = 1.0;
      switch (paperStock) {
        case 'silk':
          stockMultiplier = 1.2;
          break;
        case 'kraft':
          stockMultiplier = 1.35;
          break;
        case 'gloss':
          stockMultiplier = 1.25;
          break;
        case 'uncoated':
          stockMultiplier = 1.0;
          break;
      }

      // Binding Fee Per Unit
      let bindingFee = 0;
      switch (binding) {
        case 'wire':
          bindingFee = 3.20;
          break;
        case 'spiral':
          bindingFee = 2.40;
          break;
        case 'perfect':
          bindingFee = 4.80;
          break;
        case 'laminate':
          bindingFee = 1.75;
          break;
      }

      // Volume Discount
      let volumeDiscount = 1.0;
      if (quantity >= 500) volumeDiscount = 0.75;
      else if (quantity >= 200) volumeDiscount = 0.85;
      else if (quantity >= 100) volumeDiscount = 0.92;

      // Speed Multiplier
      let speedMultiplier = 1.0;
      let turnaroundText = 'Standard Pickup (24-48 Hours)';
      if (speed === 'rush_2hr') {
        speedMultiplier = 1.45;
        turnaroundText = '⚡ 2-Hour Express Rush';
      } else if (speed === 'same_day') {
        speedMultiplier = 1.25;
        turnaroundText = '🚀 Ready Today (Same-Day)';
      }

      // Calculation
      const unitTotal = (baseRatePerUnit * stockMultiplier + bindingFee) * quantity * volumeDiscount;
      const subtotal = (unitTotal + setupFee) * speedMultiplier;
      const finalPrice = Math.max(subtotal, 12.00); // Minimum order

      priceDisplay.textContent = `$${finalPrice.toFixed(2)}`;
      if (turnaroundBadge) {
        turnaroundBadge.innerHTML = `<i class="bi bi-clock-history"></i><span>${turnaroundText}</span>`;
      }
    }

    form.addEventListener('input', calculateEstimate);
    form.addEventListener('change', calculateEstimate);
    calculateEstimate(); // Initial run
  }

  // --------------------------------------------------------------------------
  // 4. FAQ ACCORDION
  // --------------------------------------------------------------------------
  function initFaqAccordion() {
    const faqItems = document.querySelectorAll('.fg-faq-item');
    faqItems.forEach((item) => {
      const btn = item.querySelector('.fg-faq-question');
      if (!btn) return;

      btn.addEventListener('click', () => {
        const isOpen = item.classList.contains('is-open');
        // Close siblings
        faqItems.forEach((sibling) => {
          sibling.classList.remove('is-open');
          sibling.querySelector('.fg-faq-question')?.setAttribute('aria-expanded', 'false');
        });

        if (!isOpen) {
          item.classList.add('is-open');
          btn.setAttribute('aria-expanded', 'true');
        }
      });
    });
  }

  // --------------------------------------------------------------------------
  // 5. BACK TO TOP BUTTON
  // --------------------------------------------------------------------------
  function initBackToTop() {
    const btn = document.querySelector('.fg-back-to-top');
    if (!btn) return;
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // --------------------------------------------------------------------------
  // 6. INITIALIZATION ON DOM READY
  // --------------------------------------------------------------------------
  document.addEventListener('DOMContentLoaded', () => {
    applyTheme(getPreferredTheme());
    applyDir(getPreferredDir());

    document.querySelectorAll('.theme-toggle-btn').forEach((btn) => {
      btn.addEventListener('click', toggleTheme);
    });

    document.querySelectorAll('.rtl-toggle-btn').forEach((btn) => {
      btn.addEventListener('click', toggleDir);
    });

    initPrintEstimator();
    initFaqAccordion();
    initBackToTop();

    // Highlight active nav links
    const currentPath = window.location.pathname.split('/').pop() || 'index.html';
    const cleanPath = (currentPath === '' || currentPath === '/') ? 'index.html' : currentPath;

    document.querySelectorAll('.fg-nav-link, .fg-drawer-link, .fg-dropdown-link, .fg-drawer-sublink').forEach((link) => {
      const href = link.getAttribute('href');
      if (!href) return;
      const baseHref = href.split('#')[0];
      const hasHash = href.includes('#');

      if (href === cleanPath || (!hasHash && baseHref === cleanPath)) {
        link.classList.add('active');
        link.setAttribute('aria-current', 'page');
      }
    });
  });
})();
