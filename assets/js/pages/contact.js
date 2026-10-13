/**
 * PRINTWORKS PRINT & COPY — CONTACT PAGE JAVASCRIPT
 * Handles category preselection, accessible form validation,
 * demo submission state, and directory rail smooth scrolling.
 */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', () => {
    // ------------------------------------------------------------------------
    // 1. DIRECTORY RAIL & INTRO ANCHOR SMOOTH SCROLLING
    // ------------------------------------------------------------------------
    const internalLinks = document.querySelectorAll('a[href^="#"]');
    const navbarHeight = 85;

    internalLinks.forEach((link) => {
      link.addEventListener('click', (e) => {
        const targetId = link.getAttribute('href');
        if (targetId && targetId !== '#') {
          const targetElem = document.querySelector(targetId);
          if (targetElem) {
            e.preventDefault();
            const targetPos = targetElem.getBoundingClientRect().top + window.scrollY - navbarHeight;
            window.scrollTo({
              top: targetPos,
              behavior: 'smooth'
            });
            targetElem.setAttribute('tabindex', '-1');
            targetElem.focus({ preventScroll: true });
          }
        }
      });
    });

    // ------------------------------------------------------------------------
    // 2. ENQUIRY CATEGORY SELECTOR (SECTION 2 -> FORM INTERACTION)
    // ------------------------------------------------------------------------
    const categoryCards = document.querySelectorAll('.help-category-card');
    const enquiryTypeSelect = document.getElementById('enquiry-type');
    const enquiryForm = document.getElementById('contact-enquiry-form');

    categoryCards.forEach((card) => {
      card.addEventListener('click', () => {
        const catValue = card.getAttribute('data-category');

        // Update active card styling
        categoryCards.forEach((c) => c.classList.remove('is-active'));
        card.classList.add('is-active');

        // Update select value in form
        if (enquiryTypeSelect && catValue) {
          enquiryTypeSelect.value = catValue;
          enquiryTypeSelect.dispatchEvent(new Event('change'));
        }

        // Smooth scroll to form
        const formSection = document.getElementById('order-enquiry');
        if (formSection) {
          const targetPos = formSection.getBoundingClientRect().top + window.scrollY - navbarHeight;
          window.scrollTo({
            top: targetPos,
            behavior: 'smooth'
          });
          const firstField = document.getElementById('contact-name');
          if (firstField) {
            setTimeout(() => firstField.focus(), 400);
          }
        }
      });
    });

    // ------------------------------------------------------------------------
    // 3. ACCESSIBLE FORM VALIDATION & DEMO SUBMISSION HANDLER
    // ------------------------------------------------------------------------
    if (enquiryForm) {
      const nameInput = document.getElementById('contact-name');
      const emailInput = document.getElementById('contact-email');
      const subjectInput = document.getElementById('contact-subject');
      const messageInput = document.getElementById('contact-message');
      const demoAlert = document.getElementById('contact-demo-alert');
      const errorAlert = document.getElementById('contact-error-alert');

      function validateEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
      }

      function setFieldError(input, errorElementId, message) {
        const errEl = document.getElementById(errorElementId);
        if (errEl) {
          errEl.textContent = message;
          errEl.classList.add('is-visible');
        }
        if (input) {
          input.classList.add('is-invalid');
          input.setAttribute('aria-invalid', 'true');
        }
      }

      function clearFieldError(input, errorElementId) {
        const errEl = document.getElementById(errorElementId);
        if (errEl) {
          errEl.textContent = '';
          errEl.classList.remove('is-visible');
        }
        if (input) {
          input.classList.remove('is-invalid');
          input.removeAttribute('aria-invalid');
        }
      }

      // Live clear on input
      [
        { input: nameInput, errId: 'error-contact-name' },
        { input: emailInput, errId: 'error-contact-email' },
        { input: enquiryTypeSelect, errId: 'error-enquiry-type' },
        { input: subjectInput, errId: 'error-contact-subject' },
        { input: messageInput, errId: 'error-contact-message' }
      ].forEach((field) => {
        if (field.input) {
          field.input.addEventListener('input', () => {
            clearFieldError(field.input, field.errId);
            if (errorAlert) errorAlert.classList.remove('is-visible');
          });
          field.input.addEventListener('change', () => {
            clearFieldError(field.input, field.errId);
            if (errorAlert) errorAlert.classList.remove('is-visible');
          });
        }
      });

      enquiryForm.addEventListener('submit', (e) => {
        e.preventDefault();

        let isValid = true;
        let firstInvalidField = null;

        // Reset status alerts
        if (demoAlert) demoAlert.classList.remove('is-visible');
        if (errorAlert) errorAlert.classList.remove('is-visible');

        // 1. Name validation
        if (!nameInput || !nameInput.value.trim()) {
          setFieldError(nameInput, 'error-contact-name', 'Please enter your full name.');
          isValid = false;
          if (!firstInvalidField) firstInvalidField = nameInput;
        } else {
          clearFieldError(nameInput, 'error-contact-name');
        }

        // 2. Email validation
        if (!emailInput || !emailInput.value.trim()) {
          setFieldError(emailInput, 'error-contact-email', 'Please enter your email address.');
          isValid = false;
          if (!firstInvalidField) firstInvalidField = emailInput;
        } else if (!validateEmail(emailInput.value.trim())) {
          setFieldError(emailInput, 'error-contact-email', 'Please enter a valid email address (e.g. name@domain.com).');
          isValid = false;
          if (!firstInvalidField) firstInvalidField = emailInput;
        } else {
          clearFieldError(emailInput, 'error-contact-email');
        }

        // 3. Enquiry type validation
        if (!enquiryTypeSelect || !enquiryTypeSelect.value) {
          setFieldError(enquiryTypeSelect, 'error-enquiry-type', 'Please select an enquiry category.');
          isValid = false;
          if (!firstInvalidField) firstInvalidField = enquiryTypeSelect;
        } else {
          clearFieldError(enquiryTypeSelect, 'error-enquiry-type');
        }

        // 4. Subject validation
        if (!subjectInput || !subjectInput.value.trim()) {
          setFieldError(subjectInput, 'error-contact-subject', 'Please provide a subject for your enquiry.');
          isValid = false;
          if (!firstInvalidField) firstInvalidField = subjectInput;
        } else {
          clearFieldError(subjectInput, 'error-contact-subject');
        }

        // 5. Message validation
        if (!messageInput || !messageInput.value.trim()) {
          setFieldError(messageInput, 'error-contact-message', 'Please describe your printing requirements or question.');
          isValid = false;
          if (!firstInvalidField) firstInvalidField = messageInput;
        } else {
          clearFieldError(messageInput, 'error-contact-message');
        }

        if (!isValid) {
          if (errorAlert) {
            errorAlert.classList.add('is-visible');
          }
          if (firstInvalidField) {
            firstInvalidField.focus();
          }
          return;
        }

        // Valid Submission - Display Honest Demo State Banner
        // Explains client-side validation succeeded and backend integration requirements
        if (demoAlert) {
          const summarySpan = document.getElementById('demo-summary-name');
          if (summarySpan && nameInput) {
            summarySpan.textContent = nameInput.value.trim();
          }
          demoAlert.classList.add('is-visible');
          demoAlert.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
      });
    }
  });
})();
