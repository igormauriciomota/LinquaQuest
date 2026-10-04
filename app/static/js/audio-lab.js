(() => {
  const player = document.getElementById('audioPlayer');
  if (!player) return;
  const csrf = document.querySelector('meta[name="csrf-token"]').content;
  const dock = document.getElementById('audioDock');
  const dockLabel = document.getElementById('audioDockLabel');
  const dockPlay = document.getElementById('audioDockPlay');
  const heardCount = document.getElementById('heardCount');
  const ring = document.querySelector('.audio-ring');
  const cards = [...document.querySelectorAll('.audio-phrase-card')];
  const storageKey = 'lq-family-audio-heard';
  const serverSaved = JSON.parse(document.getElementById('audioLessonData').textContent).saved || 0;
  let heard = new Set(JSON.parse(localStorage.getItem(storageKey) || '[]').map(Number));
  let saveTimer = null;

  function currentCount() { return Math.max(serverSaved, heard.size); }

  function updateProgress() {
    const count = currentCount();
    heardCount.textContent = count;
    ring.style.setProperty('--progress', `${Math.round(count / 64 * 100)}%`);
    cards.forEach(card => card.classList.toggle('heard', heard.has(Number(card.dataset.id))));
    localStorage.setItem(storageKey, JSON.stringify([...heard]));
    clearTimeout(saveTimer);
    saveTimer = window.setTimeout(async () => {
      try {
        const response = await fetch('/aprender/laboratorio-audio/familia-cidade/progresso', {
          method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRF-Token': csrf},
          body: JSON.stringify({heard_items: count})
        });
        const result = await response.json();
        if (result.xp_awarded) announce(`Laboratório concluído. Você ganhou ${result.xp_awarded} XP.`);
      } catch (_) { /* o progresso local continua disponível */ }
    }, 700);
  }

  function announce(message) {
    let live = document.getElementById('audioLabLive');
    if (!live) { live = document.createElement('div'); live.id = 'audioLabLive'; live.className = 'visually-hidden'; live.setAttribute('aria-live', 'polite'); document.body.appendChild(live); }
    live.textContent = ''; window.setTimeout(() => { live.textContent = message; }, 30);
  }

  function play(button) {
    const card = button.closest('.audio-phrase-card');
    cards.forEach(item => item.classList.remove('playing'));
    card.classList.add('playing');
    heard.add(Number(card.dataset.id)); updateProgress();
    player.src = button.dataset.audio; dockLabel.textContent = button.dataset.label;
    dock.hidden = false; player.play().then(() => {
      dockPlay.innerHTML = '<i class="bi bi-pause-fill"></i>'; dock.classList.add('is-playing');
      announce(`Reproduzindo ${button.dataset.label}`);
    }).catch(() => announce('Use o botão reproduzir para iniciar o áudio.'));
  }

  document.querySelectorAll('[data-audio]').forEach(button => button.addEventListener('click', () => play(button)));
  dockPlay.addEventListener('click', () => {
    if (player.paused) player.play(); else player.pause();
  });
  player.addEventListener('play', () => { dockPlay.innerHTML = '<i class="bi bi-pause-fill"></i>'; dock.classList.add('is-playing'); });
  player.addEventListener('pause', () => { dockPlay.innerHTML = '<i class="bi bi-play-fill"></i>'; dock.classList.remove('is-playing'); });
  document.getElementById('audioDockClose').addEventListener('click', () => { player.pause(); dock.hidden = true; cards.forEach(card => card.classList.remove('playing')); });

  function filterCards() {
    const query = document.getElementById('audioSearch').value.trim().toLocaleLowerCase('pt-BR');
    const activeGroup = document.querySelector('.audio-group-tabs button.active').dataset.group;
    let visible = 0;
    cards.forEach(card => {
      const show = (!query || card.dataset.search.includes(query)) && (activeGroup === 'all' || card.dataset.group === activeGroup);
      card.hidden = !show; if (show) visible += 1;
    });
    document.getElementById('audioNoResults').hidden = visible !== 0;
  }
  document.getElementById('audioSearch').addEventListener('input', filterCards);
  document.querySelectorAll('.audio-group-tabs button').forEach(button => button.addEventListener('click', () => {
    document.querySelectorAll('.audio-group-tabs button').forEach(item => { item.classList.remove('active'); item.setAttribute('aria-selected', 'false'); });
    button.classList.add('active'); button.setAttribute('aria-selected', 'true'); filterCards();
  }));
  updateProgress();
})();
