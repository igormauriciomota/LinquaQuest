(() => {
  const dataNode = document.getElementById('matchArenaData');
  if (!dataNode) return;
  const categories = JSON.parse(dataNode.textContent);
  const csrf = document.querySelector('meta[name="csrf-token"]').content;
  const picker = document.getElementById('categoryPicker');
  const game = document.getElementById('matchGame');
  const result = document.getElementById('arenaResult');
  const englishList = document.getElementById('englishWords');
  const portugueseList = document.getElementById('portugueseWords');
  const live = document.getElementById('matchLive');
  const progress = document.getElementById('matchProgress');
  const track = document.querySelector('.match-progress-track');
  let current = null;
  let selectedEnglish = null;
  let matches = 0;
  let mistakes = 0;
  let score = 0;

  const shuffle = values => [...values].sort(() => Math.random() - 0.5);

  function announce(message) {
    live.textContent = '';
    window.setTimeout(() => { live.textContent = message; }, 30);
  }

  function updateProgress() {
    const percent = Math.round(matches / current.pairs.length * 100);
    progress.style.width = `${percent}%`;
    track.setAttribute('aria-valuenow', String(percent));
    document.getElementById('matchScore').textContent = score;
  }

  function wordButton(text, language, originalIndex) {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'arena-word';
    button.dataset.index = String(originalIndex);
    button.dataset.language = language;
    button.innerHTML = `<span>${text}</span>${language === 'en' ? '<i class="bi bi-volume-up" aria-hidden="true"></i>' : '<i class="bi bi-circle" aria-hidden="true"></i>'}`;
    button.setAttribute('aria-label', `${text}, ${language === 'en' ? 'em inglês' : 'em português'}`);
    button.addEventListener('click', () => language === 'en' ? chooseEnglish(button, text) : choosePortuguese(button, text));
    return button;
  }

  function chooseEnglish(button, text) {
    if (button.classList.contains('matched')) return;
    englishList.querySelectorAll('.arena-word').forEach(item => item.classList.remove('selected'));
    button.classList.add('selected');
    selectedEnglish = button;
    window.LinguaQuest.speak(text, 0.78);
    announce(`${text} selecionado. Agora escolha a tradução em português.`);
  }

  function choosePortuguese(button, text) {
    if (button.classList.contains('matched')) return;
    if (!selectedEnglish) {
      button.classList.add('needs-source');
      announce('Escolha primeiro uma palavra na coluna English.');
      window.setTimeout(() => button.classList.remove('needs-source'), 500);
      return;
    }
    const correct = selectedEnglish.dataset.index === button.dataset.index;
    if (correct) {
      const englishText = selectedEnglish.querySelector('span').textContent;
      selectedEnglish.classList.remove('selected');
      selectedEnglish.classList.add('matched');
      button.classList.add('matched');
      selectedEnglish.setAttribute('aria-label', `${englishText}, combinado corretamente com ${text}`);
      button.setAttribute('aria-label', `${text}, combinado corretamente com ${englishText}`);
      selectedEnglish.querySelector('i').className = 'bi bi-check-circle-fill';
      button.querySelector('i').className = 'bi bi-check-circle-fill';
      matches += 1;
      score += Math.max(5, 10 - mistakes);
      mistakes = 0;
      announce(`Correto! ${englishText} significa ${text}. ${matches} de ${current.pairs.length} pares encontrados.`);
      selectedEnglish = null;
      updateProgress();
      const next = englishList.querySelector('.arena-word:not(.matched)');
      if (matches === current.pairs.length) window.setTimeout(finish, 650);
      else next?.focus();
    } else {
      mistakes += 1;
      selectedEnglish.classList.add('wrong');
      button.classList.add('wrong');
      announce(`Ainda não. ${text} não corresponde à palavra selecionada. Tente novamente.`);
      window.setTimeout(() => {
        selectedEnglish?.classList.remove('wrong');
        button.classList.remove('wrong');
      }, 600);
    }
  }

  function renderRound(slug) {
    current = categories[slug];
    selectedEnglish = null; matches = 0; mistakes = 0; score = 0;
    document.getElementById('matchGameTitle').textContent = current.title;
    document.getElementById('matchGameSubtitle').textContent = current.title_pt;
    document.getElementById('matchCategoryLevel').textContent = `NÍVEL ${current.level} · ${current.pairs.length} PARES`;
    englishList.innerHTML = ''; portugueseList.innerHTML = '';
    const indexed = current.pairs.map((pair, index) => ({pair, index}));
    shuffle(indexed).forEach(item => englishList.appendChild(wordButton(item.pair[0], 'en', item.index)));
    shuffle(indexed).forEach(item => portugueseList.appendChild(wordButton(item.pair[1], 'pt', item.index)));
    picker.hidden = true; result.hidden = true; game.hidden = false;
    updateProgress();
    game.scrollIntoView({behavior: document.documentElement.classList.contains('reduce-motion') ? 'auto' : 'smooth', block: 'start'});
    window.setTimeout(() => englishList.querySelector('button')?.focus(), 150);
  }

  async function finish() {
    let payload = {completed: true, score: 100, xp_awarded: 0};
    try {
      const response = await fetch('/aprender/arena-pares/concluir', {
        method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRF-Token': csrf},
        body: JSON.stringify({category: current.slug, correct: matches})
      });
      if (!response.ok) throw new Error('Não foi possível salvar o progresso.');
      payload = await response.json();
    } catch (error) {
      announce(error.message);
    }
    game.hidden = true; result.hidden = false;
    document.getElementById('arenaAccuracy').textContent = `${payload.score}%`;
    document.getElementById('arenaXp').textContent = `+${payload.xp_awarded}`;
    document.getElementById('arenaResultMessage').textContent = `${current.title}: você encontrou todos os ${matches} pares. ${payload.xp_awarded ? 'Novo vocabulário dominado!' : 'Sua memória ficou mais forte.'}`;
    result.scrollIntoView({behavior: 'smooth', block: 'center'});
    document.getElementById('playAgain').focus();
  }

  function showPicker() {
    game.hidden = true; result.hidden = true; picker.hidden = false;
    picker.scrollIntoView({behavior: 'smooth', block: 'start'});
    picker.querySelector('[data-category]')?.focus();
  }

  document.querySelectorAll('[data-category]').forEach(button => button.addEventListener('click', () => renderRound(button.dataset.category)));
  document.getElementById('backToCategories').addEventListener('click', showPicker);
  document.getElementById('chooseAnother').addEventListener('click', showPicker);
  document.getElementById('playAgain').addEventListener('click', () => renderRound(current.slug));
})();
