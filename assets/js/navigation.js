/**
 * PRINTWORKS PRINT & COPY — NAVIGATION & INTERACTION JAVASCRIPT
 * Accessible Drawer Menu (Mobile & Tablet), Submenu Dropdown, Login Modal, and Gallery Lightbox
 */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', () => {
    // ------------------------------------------------------------------------
    // 1. MOBILE & TABLET DRAWER NAVIGATION
    // ------------------------------------------------------------------------
    const hamburgerBtn = document.querySelector('.fg-hamburger-btn');
    const drawer = document.querySelector('.fg-drawer');
    const backdrop = document.querySelector('.fg-drawer-backdrop');
    const closeBtn = document.querySelector('.fg-drawer-close');
    const drawerNavLinks = document.querySelectorAll('.fg-drawer-link:not(.fg-drawer-dropdown-btn), .fg-drawer-sublink, .fg-drawer-footer .fg-btn');
    const drawerDropdownBtns = document.querySelectorAll('.fg-drawer-dropdown-btn');

    let previousFocusElement = null;

    function openDrawer() {
      if (!drawer || !backdrop) return;
      previousFocusElement = document.activeElement;
      drawer.classList.add('is-open');
      backdrop.classList.add('is-open');
      if (hamburgerBtn) {
        hamburgerBtn.classList.add('is-active');
        hamburgerBtn.setAttribute('aria-expanded', 'true');
      }
      document.body.style.overflow = 'hidden';

      if (closeBtn) {
        setTimeout(() => closeBtn.focus(), 50);
      }
    }

    function closeDrawer() {
      if (!drawer || !backdrop) return;
      drawer.classList.remove('is-open');
      backdrop.classList.remove('is-open');
      if (hamburgerBtn) {
        hamburgerBtn.classList.remove('is-active');
        hamburgerBtn.setAttribute('aria-expanded', 'false');
      }
      document.body.style.overflow = '';

      if (previousFocusElement && typeof previousFocusElement.focus === 'function') {
        previousFocusElement.focus();
      }
    }

    if (hamburgerBtn) {
      hamburgerBtn.addEventListener('click', () => {
        const isOpen = drawer && drawer.classList.contains('is-open');
        if (isOpen) {
          closeDrawer();
        } else {
          openDrawer();
        }
      });
    }

    if (closeBtn) {
      closeBtn.addEventListener('click', closeDrawer);
    }

    if (backdrop) {
      backdrop.addEventListener('click', closeDrawer);
    }

    // Drawer Submenus Toggle (Home ▼)
    drawerDropdownBtns.forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const parent = btn.closest('.fg-drawer-dropdown');
        if (parent) {
          const isExpanded = parent.classList.toggle('is-expanded');
          btn.setAttribute('aria-expanded', isExpanded ? 'true' : 'false');
        }
      });
    });

    // Close drawer when regular link is clicked
    drawerNavLinks.forEach((link) => {
      link.addEventListener('click', () => {
        closeDrawer();
      });
    });

    // Close drawer on Escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        if (drawer && drawer.classList.contains('is-open')) {
          closeDrawer();
        }
      }
    });

    // Trap focus inside drawer
    if (drawer) {
      drawer.addEventListener('keydown', (e) => {
        if (e.key !== 'Tab') return;
        const focusables = drawer.querySelectorAll(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        if (focusables.length === 0) return;

        const first = focusables[0];
        const last = focusables[focusables.length - 1];

        if (e.shiftKey && document.activeElement === first) {
          last.focus();
          e.preventDefault();
        } else if (!e.shiftKey && document.activeElement === last) {
          first.focus();
          e.preventDefault();
        }
      });
    }

    // ------------------------------------------------------------------------
    // 2. LOGIN MODAL CONTROLLER
    // ------------------------------------------------------------------------
    const loginModal = document.getElementById('login-modal');
    const loginBtns = document.querySelectorAll('.fg-login-btn, [data-modal="login"]');
    const loginCloseBtn = loginModal ? loginModal.querySelector('.fg-modal-close') : null;
    let preModalFocus = null;

    function openLoginModal() {
      if (!loginModal) return;
      preModalFocus = document.activeElement;
      if (drawer && drawer.classList.contains('is-open')) {
        closeDrawer();
      }
      loginModal.classList.add('is-open');
      loginModal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';

      const emailInput = loginModal.querySelector('input[type="email"]');
      setTimeout(() => {
        if (emailInput) emailInput.focus();
        else if (loginCloseBtn) loginCloseBtn.focus();
      }, 50);
    }

    function closeLoginModal() {
      if (!loginModal) return;
      loginModal.classList.remove('is-open');
      loginModal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';

      if (preModalFocus && typeof preModalFocus.focus === 'function') {
        preModalFocus.focus();
      }
    }

    loginBtns.forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        openLoginModal();
      });
    });

    if (loginCloseBtn) {
      loginCloseBtn.addEventListener('click', closeLoginModal);
    }

    if (loginModal) {
      loginModal.addEventListener('click', (e) => {
        if (e.target === loginModal) {
          closeLoginModal();
        }
      });
    }

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && loginModal && loginModal.classList.contains('is-open')) {
        closeLoginModal();
      }
    });

    // ------------------------------------------------------------------------
    // 3. GALLERY LIGHTBOX CONTROLLER
    // ------------------------------------------------------------------------
    const lightbox = document.getElementById('gallery-lightbox');
    const lightboxImg = lightbox ? lightbox.querySelector('.fg-lightbox-img') : null;
    const lightboxTitle = lightbox ? lightbox.querySelector('.fg-lightbox-title') : null;
    const lightboxSub = lightbox ? lightbox.querySelector('.fg-lightbox-sub') : null;
    const lightboxClose = lightbox ? lightbox.querySelector('.fg-lightbox-close') : null;
    const galleryItems = document.querySelectorAll('.fg-gallery-item');
    let preLightboxFocus = null;

    function openLightbox(item) {
      if (!lightbox || !lightboxImg) return;
      preLightboxFocus = document.activeElement;

      const img = item.querySelector('.fg-gallery-img');
      const titleEl = item.querySelector('.fg-gallery-title');
      const categoryEl = item.querySelector('.fg-gallery-category');

      if (img) {
        lightboxImg.src = img.src;
        lightboxImg.alt = img.alt || 'Print sample';
      }
      if (lightboxTitle && titleEl) {
        lightboxTitle.textContent = titleEl.textContent;
      }
      if (lightboxSub && categoryEl) {
        lightboxSub.textContent = categoryEl.textContent;
      }

      lightbox.classList.add('is-open');
      lightbox.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';

      if (lightboxClose) {
        setTimeout(() => lightboxClose.focus(), 50);
      }
    }

    function closeLightbox() {
      if (!lightbox) return;
      lightbox.classList.remove('is-open');
      lightbox.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';

      if (preLightboxFocus && typeof preLightboxFocus.focus === 'function') {
        preLightboxFocus.focus();
      }
    }

    galleryItems.forEach((item) => {
      item.addEventListener('click', () => openLightbox(item));
      item.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          openLightbox(item);
        }
      });
    });

    if (lightboxClose) {
      lightboxClose.addEventListener('click', closeLightbox);
    }

    if (lightbox) {
      lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) {
          closeLightbox();
        }
      });
    }

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && lightbox && lightbox.classList.contains('is-open')) {
        closeLightbox();
      }
    });
  });
})();
