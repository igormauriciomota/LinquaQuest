(() => {
  const root = document.documentElement;
  const themeButton = document.getElementById('themeToggle');
  const accessibilityButton = document.getElementById('accessibilityToggle');
  const accessibilityPanel = document.getElementById('accessibilityPanel');

  function syncControls() {
    const light = root.dataset.theme === 'light';
    themeButton?.setAttribute('aria-pressed', String(light));
    themeButton?.setAttribute('aria-label', light ? 'Ativar tema escuro' : 'Ativar tema claro');
    const contrast = root.classList.contains('high-contrast');
    const reduced = root.classList.contains('reduce-motion');
    const contrastButton = document.getElementById('contrastToggle');
    const motionButton = document.getElementById('motionToggle');
    [
      [contrastButton, contrast], [motionButton, reduced]
    ].forEach(([button, active]) => {
      if (!button) return;
      button.setAttribute('aria-pressed', String(active));
      const icon = button.querySelector('.switch-icon');
      if (icon) icon.className = `bi ${active ? 'bi-toggle-on' : 'bi-toggle-off'} switch-icon`;
    });
  }

  themeButton?.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('lq-theme', root.dataset.theme);
    syncControls();
  });

  function setPanel(open) {
    if (!accessibilityPanel || !accessibilityButton) return;
    accessibilityPanel.hidden = !open;
    accessibilityButton.setAttribute('aria-expanded', String(open));
    if (open) accessibilityPanel.querySelector('button')?.focus();
  }
  accessibilityButton?.addEventListener('click', () => setPanel(accessibilityPanel?.hidden));
  document.getElementById('closeAccessibility')?.addEventListener('click', () => {
    setPanel(false); accessibilityButton?.focus();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && accessibilityPanel && !accessibilityPanel.hidden) {
      setPanel(false); accessibilityButton?.focus();
    }
  });

  document.querySelectorAll('[data-font-action]').forEach(button => button.addEventListener('click', () => {
    const current = Number(root.dataset.fontScale || 100);
    const step = button.dataset.fontAction === 'increase' ? 10 : -10;
    const next = Math.min(130, Math.max(90, current + step));
    root.dataset.fontScale = String(next);
    localStorage.setItem('lq-font-scale', String(next));
  }));
  document.getElementById('contrastToggle')?.addEventListener('click', () => {
    root.classList.toggle('high-contrast');
    localStorage.setItem('lq-contrast', String(root.classList.contains('high-contrast')));
    syncControls();
  });
  document.getElementById('motionToggle')?.addEventListener('click', () => {
    root.classList.toggle('reduce-motion');
    localStorage.setItem('lq-motion', root.classList.contains('reduce-motion') ? 'reduced' : 'full');
    syncControls();
  });
  document.getElementById('accessibilityReset')?.addEventListener('click', () => {
    root.dataset.fontScale = '100';
    root.classList.remove('high-contrast', 'reduce-motion');
    ['lq-font-scale', 'lq-contrast', 'lq-motion'].forEach(key => localStorage.removeItem(key));
    syncControls();
  });

  const speak = (text, rate = 0.85) => {
    if (!('speechSynthesis' in window)) {
      alert('Seu navegador não oferece síntese de voz. Tente Chrome, Edge ou Safari.');
      return;
    }
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    utterance.rate = rate;
    const voices = window.speechSynthesis.getVoices();
    utterance.voice = voices.find(v => v.lang === 'en-US') || voices.find(v => v.lang.startsWith('en')) || null;
    window.speechSynthesis.speak(utterance);
  };
  window.LinguaQuest = { speak };
  document.addEventListener('click', event => {
    const button = event.target.closest('[data-speak]');
    if (button) speak(button.dataset.speak);
    const card = event.target.closest('[data-card-href]');
    if (card && !event.target.closest('a, button, input, select, textarea')) {
      window.location.assign(card.dataset.cardHref);
    }
  });
  syncControls();
})();
