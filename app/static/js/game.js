(() => {
  const dataNode = document.getElementById('exerciseData');
  if (!dataNode) return;
  const exercises = JSON.parse(dataNode.textContent);
  const csrf = document.querySelector('meta[name="csrf-token"]').content;
  const answerUrlTemplate = document.querySelector('.lesson-shell').dataset.answerUrl;
  const els = {
    intro: document.getElementById('lessonIntro'), stage: document.getElementById('exerciseStage'),
    start: document.getElementById('startLesson'), progress: document.getElementById('lessonProgress'),
    counter: document.getElementById('exerciseCounter'), instruction: document.getElementById('exerciseInstruction'),
    prompt: document.getElementById('exercisePrompt'), area: document.getElementById('exerciseArea'),
    audio: document.getElementById('audioButton'), check: document.getElementById('checkAnswer'),
    next: document.getElementById('nextExercise'), feedback: document.getElementById('answerFeedback'),
    xp: document.getElementById('earnedXp'), result: document.getElementById('resultCard')
  };
  let index = 0, selected = null, earnedXp = 0, matched = {}, activeLeft = null;

  const shuffle = array => [...array].sort(() => Math.random() - 0.5);
  const escapeHtml = value => String(value).replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));

  function optionButton(value) {
    const button = document.createElement('button');
    button.type = 'button'; button.className = 'answer-option'; button.textContent = value;
    button.addEventListener('click', () => {
      els.area.querySelectorAll('.answer-option').forEach(x => x.classList.remove('selected'));
      button.classList.add('selected'); selected = value; els.check.disabled = false;
    });
    return button;
  }

  function renderMatch(pairs) {
    const left = shuffle(pairs.map(p => p.left)); const right = shuffle(pairs.map(p => p.right));
    const wrapper = document.createElement('div'); wrapper.className = 'match-grid';
    const leftCol = document.createElement('div'); const rightCol = document.createElement('div');
    leftCol.setAttribute('aria-label', 'Palavras em inglês'); rightCol.setAttribute('aria-label', 'Traduções em português');
    const leftTitle = document.createElement('h3'); leftTitle.className = 'match-column-title'; leftTitle.innerHTML = '<span>EN</span> English <small>Inglês</small>';
    const rightTitle = document.createElement('h3'); rightTitle.className = 'match-column-title'; rightTitle.innerHTML = '<span>PT</span> Português <small>Tradução</small>';
    leftCol.appendChild(leftTitle); rightCol.appendChild(rightTitle);
    const makeMatchButton = (value, language) => {
      const button = document.createElement('button');
      button.type = 'button'; button.className = 'match-option'; button.dataset.value = value;
      button.textContent = value; button.setAttribute('aria-pressed', 'false');
      button.setAttribute('aria-label', `${value}, ${language}`);
      return button;
    };
    left.forEach(value => {
      const b = makeMatchButton(value, 'em inglês');
      b.addEventListener('click', () => {
        leftCol.querySelectorAll('.match-option').forEach(x => x.classList.remove('active'));
        leftCol.querySelectorAll('.match-option').forEach(x => x.setAttribute('aria-pressed', 'false'));
        b.classList.add('active'); b.setAttribute('aria-pressed', 'true'); activeLeft = value;
        if (window.LinguaQuest) window.LinguaQuest.speak(value, .78);
      }); leftCol.appendChild(b);
    });
    right.forEach(value => {
      const b = makeMatchButton(value, 'em português');
      b.addEventListener('click', () => {
        if (!activeLeft) return;
        const oldRight = matched[activeLeft];
        if (oldRight) {
          const oldButton = [...rightCol.querySelectorAll('.match-option')].find(x => x.dataset.value === oldRight);
          if (oldButton) { oldButton.classList.remove('used'); oldButton.disabled = false; }
        }
        matched[activeLeft] = value;
        const leftButton = [...leftCol.querySelectorAll('.match-option')].find(x => x.dataset.value === activeLeft);
        leftButton.classList.remove('active'); leftButton.classList.add('paired');
        leftButton.setAttribute('aria-pressed', 'false');
        leftButton.innerHTML = `${escapeHtml(activeLeft)} <small>→ ${escapeHtml(value)}</small>`;
        activeLeft = null; b.classList.add('used'); b.disabled = true;
        els.check.disabled = Object.keys(matched).length !== pairs.length;
      }); rightCol.appendChild(b);
    });
    wrapper.append(leftCol, rightCol); els.area.appendChild(wrapper);
  }

  function render() {
    selected = null; matched = {}; activeLeft = null;
    const exercise = exercises[index];
    els.progress.style.width = `${index / exercises.length * 100}%`;
    els.counter.textContent = `DESAFIO ${index + 1} DE ${exercises.length}`;
    els.instruction.textContent = exercise.instruction; els.prompt.textContent = exercise.prompt;
    els.area.innerHTML = ''; els.feedback.className = 'answer-feedback d-none';
    els.check.classList.remove('d-none'); els.next.classList.add('d-none'); els.check.disabled = true;
    const speakText = exercise.payload.speak;
    els.audio.classList.toggle('d-none', !speakText);
    els.audio.onclick = () => window.LinguaQuest.speak(speakText, 0.78);
    if (exercise.kind === 'choice' || exercise.kind === 'listen') {
      const grid = document.createElement('div'); grid.className = 'answer-grid';
      shuffle(exercise.payload.options).forEach(value => grid.appendChild(optionButton(value)));
      els.area.appendChild(grid);
    } else if (exercise.kind === 'match') {
      renderMatch(exercise.payload.pairs);
    } else if (exercise.kind === 'write') {
      const input = document.createElement('input'); input.className = 'write-answer';
      input.placeholder = exercise.payload.placeholder || 'Digite sua resposta'; input.autocomplete = 'off';
      input.addEventListener('input', () => { selected = input.value; els.check.disabled = !input.value.trim(); });
      input.addEventListener('keydown', e => { if (e.key === 'Enter' && !els.check.disabled) submit(); });
      els.area.appendChild(input); setTimeout(() => input.focus(), 50);
    }
  }

  async function submit() {
    els.check.disabled = true;
    const exercise = exercises[index]; const answer = exercise.kind === 'match' ? matched : selected;
    try {
      const response = await fetch(answerUrlTemplate.replace(/0$/, String(exercise.id)), {
        method: 'POST', headers: {'Content-Type':'application/json','X-CSRF-Token':csrf}, body: JSON.stringify({answer})
      });
      const result = await response.json(); if (!response.ok) throw new Error(result.error || 'Não foi possível enviar.');
      earnedXp += result.xp_awarded; els.xp.textContent = earnedXp;
      els.feedback.className = `answer-feedback ${result.correct ? 'correct' : 'incorrect'}`;
      els.feedback.querySelector('.feedback-icon').innerHTML = `<i class="bi ${result.correct ? 'bi-check-lg' : 'bi-x-lg'}"></i>`;
      els.feedback.querySelector('strong').textContent = result.correct ? 'Muito bem!' : 'Quase lá!';
      els.feedback.querySelector('p').textContent = result.explanation;
      els.check.classList.add('d-none'); els.next.classList.remove('d-none');
      document.querySelectorAll('#exerciseArea button, #exerciseArea input').forEach(x => x.disabled = true);
    } catch (error) { alert(error.message); els.check.disabled = false; }
  }

  async function finish() {
    const response = await fetch('/aprender/finalizar', {method:'POST', headers:{'X-CSRF-Token':csrf}});
    const result = await response.json();
    els.stage.classList.add('d-none'); els.result.classList.remove('d-none'); els.progress.style.width = '100%';
    document.getElementById('resultScore').textContent = `${result.score}%`;
    document.getElementById('resultCorrect').textContent = `${result.correct}/${result.total}`;
    document.getElementById('resultXp').textContent = `+${result.xp}`;
    document.getElementById('resultTitle').textContent = result.completed ? 'Muito bem!' : 'Continue praticando!';
    window.LinguaQuest.speak(result.completed ? 'Excellent work!' : 'Keep practicing!', 0.9);
  }

  els.start.addEventListener('click', () => { els.intro.classList.add('d-none'); els.stage.classList.remove('d-none'); render(); });
  els.check.addEventListener('click', submit);
  els.next.addEventListener('click', () => { index += 1; index < exercises.length ? render() : finish(); });
})();
