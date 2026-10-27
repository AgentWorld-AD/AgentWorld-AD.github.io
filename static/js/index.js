'use strict';
// Fill the final public URLs here when the paper and repository are released.
const RESOURCES = { paper: '', code: '' };
for (const [name, url] of Object.entries(RESOURCES)) {
  if (!url) continue;
  const link = document.querySelector(`[data-resource="${name}"]`);
  link.href = url;
  link.classList.remove('disabled');
  link.removeAttribute('aria-disabled');
  link.removeAttribute('tabindex');
  link.querySelector('span')?.remove();
}

const tabs = [...document.querySelectorAll('[role="tab"]')];
function selectTab(selected, focus = false) {
  for (const tab of tabs) {
    const active = tab === selected;
    tab.setAttribute('aria-selected', String(active));
    tab.tabIndex = active ? 0 : -1;
    document.getElementById(tab.getAttribute('aria-controls')).hidden = !active;
  }
  if (focus) selected.focus();
}
for (const [index, tab] of tabs.entries()) {
  tab.addEventListener('click', () => selectTab(tab));
  tab.addEventListener('keydown', event => {
    let next;
    if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
    if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
    if (event.key === 'Home') next = 0;
    if (event.key === 'End') next = tabs.length - 1;
    if (next !== undefined) { event.preventDefault(); selectTab(tabs[next], true); }
  });
}

const dialog = document.querySelector('#figure-dialog');
let lastFigureButton;
for (const button of document.querySelectorAll('[data-zoom]')) {
  button.addEventListener('click', () => {
    const source = button.querySelector('img');
    const enlarged = document.querySelector('#enlarged-figure');
    enlarged.src = source.currentSrc || source.src;
    enlarged.alt = source.alt;
    document.querySelector('#enlarged-caption').textContent = button.closest('figure').querySelector('figcaption')?.textContent.replace('Click figures to enlarge ↗', '').trim() || '';
    lastFigureButton = button;
    dialog.showModal();
    document.body.classList.add('dialog-open');
  });
}
document.querySelector('#close-figure').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => { if (event.target === dialog) { const rect = dialog.getBoundingClientRect(); if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close(); } });
dialog.addEventListener('close', () => { document.body.classList.remove('dialog-open'); lastFigureButton?.focus({preventScroll:true}); });

document.querySelector('#copy-bibtex').addEventListener('click', async () => {
  const text = document.querySelector('#bibtex-code').textContent;
  const status = document.querySelector('#copy-status');
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
    } else {
      const field = document.createElement('textarea');
      field.value = text; field.style.position = 'fixed'; field.style.opacity = '0';
      document.body.append(field); field.select();
      const success = document.execCommand('copy'); field.remove();
      if (!success) throw new Error('Clipboard unavailable');
    }
    status.textContent = 'Citation copied.';
    document.querySelector('#copy-bibtex').textContent = 'Copied ✓';
    setTimeout(() => { document.querySelector('#copy-bibtex').textContent = 'Copy citation'; status.textContent = ''; }, 3000);
  } catch {
    const selection = window.getSelection();
    const range = document.createRange(); range.selectNodeContents(document.querySelector('#bibtex-code'));
    selection.removeAllRanges(); selection.addRange(range);
    status.textContent = 'Citation selected. Press Ctrl+C (or ⌘C) to copy.';
  }
});
