/**
 * PRINTWORKS PRINT & COPY — HOME 2 (EDITORIAL CONCEPT) JAVASCRIPT
 * Handles Interactive Planning Checklist, Progress Updates, and Editorial Interactions
 */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', () => {
    // ------------------------------------------------------------------------
    // 1. INTERACTIVE PRINT JOB PLANNING CHECKLIST (SECTION 6)
    // ------------------------------------------------------------------------
    const checklistRows = document.querySelectorAll('.h2-checklist-row');
    const progressBadge = document.querySelector('.h2-progress-badge');
    const totalItems = checklistRows.length;

    function updateChecklistProgress() {
      const completedCount = document.querySelectorAll('.h2-checklist-row.is-completed').length;
      if (progressBadge) {
        progressBadge.textContent = `${completedCount} of ${totalItems} Ready`;
      }
    }

    checklistRows.forEach((row) => {
      // Click toggle
      row.addEventListener('click', () => {
        const isCompleted = row.classList.toggle('is-completed');
        row.setAttribute('aria-checked', isCompleted ? 'true' : 'false');
        updateChecklistProgress();
      });

      // Keyboard toggle (Enter or Space)
      row.addEventListener('keydown', (e) => {
        if (e.key === ' ' || e.key === 'Enter') {
          e.preventDefault();
          const isCompleted = row.classList.toggle('is-completed');
          row.setAttribute('aria-checked', isCompleted ? 'true' : 'false');
          updateChecklistProgress();
        }
      });
    });

    // Initialize progress counter
    updateChecklistProgress();

    // ------------------------------------------------------------------------
    // 2. TIMELINE HORIZONTAL SCROLL HELPER FOR TABLETS
    // ------------------------------------------------------------------------
    const timelineWrapper = document.querySelector('.h2-workflow-timeline-wrapper');
    if (timelineWrapper) {
      let isDown = false;
      let startX;
      let scrollLeft;

      timelineWrapper.addEventListener('mousedown', (e) => {
        isDown = true;
        startX = e.pageX - timelineWrapper.offsetLeft;
        scrollLeft = timelineWrapper.scrollLeft;
      });

      timelineWrapper.addEventListener('mouseleave', () => {
        isDown = false;
      });

      timelineWrapper.addEventListener('mouseup', () => {
        isDown = false;
      });

      timelineWrapper.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - timelineWrapper.offsetLeft;
        const walk = (x - startX) * 1.5;
        timelineWrapper.scrollLeft = scrollLeft - walk;
      });
    }
  });
})();
