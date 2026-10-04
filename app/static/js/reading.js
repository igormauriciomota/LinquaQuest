(() => {
  const node = document.getElementById('readingData');
  if (!node) return;
  const data = JSON.parse(node.textContent);
  const csrf = document.querySelector('meta[name="csrf-token"]').content;
  let listenCount = 0, bestSpeakingScore = 0, target = '';
  const sentences = data.body_en.replace(/\n+/g, ' ').match(/[^.!?]+[.!?]+/g) || [data.body_en];
  const list = document.getElementById('shadowingList');
  const startSpeech = document.getElementById('startSpeech');

  const speakText = (rate) => { listenCount += 1; window.LinguaQuest.speak(data.body_en, rate); };
  document.getElementById('listenNormal').addEventListener('click', () => speakText(.86));
  document.getElementById('listenSlow').addEventListener('click', () => speakText(.64));
  document.getElementById('stopAudio').addEventListener('click', () => window.speechSynthesis?.cancel());
  document.getElementById('toggleTranslation').addEventListener('click', event => {
    const box = document.getElementById('translationBox'); box.classList.toggle('d-none');
    event.currentTarget.innerHTML = box.classList.contains('d-none') ? '<i class="bi bi-translate"></i> Mostrar tradução' : '<i class="bi bi-eye-slash"></i> Ocultar tradução';
  });

  sentences.forEach((sentence, index) => {
    const row = document.createElement('button'); row.type = 'button'; row.className = 'shadow-sentence';
    row.innerHTML = `<span>${index + 1}</span><p>${sentence.trim()}</p><i class="bi bi-volume-up-fill"></i>`;
    row.addEventListener('click', () => {
      list.querySelectorAll('button').forEach(x => x.classList.remove('active')); row.classList.add('active');
      target = sentence.trim(); document.getElementById('targetSentence').textContent = target; startSpeech.disabled = false;
      listenCount += 1; window.LinguaQuest.speak(target, .72);
    }); list.appendChild(row);
  });

  const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!Recognition) {
    startSpeech.disabled = true; startSpeech.innerHTML = '<i class="bi bi-mic-mute"></i> Reconhecimento indisponível';
  } else {
    startSpeech.addEventListener('click', () => {
      if (!target) return;
      const recognition = new Recognition(); recognition.lang = 'en-US'; recognition.interimResults = false; recognition.maxAlternatives = 1;
      startSpeech.disabled = true; startSpeech.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Ouvindo...';
      recognition.onresult = event => {
        const transcript = event.results[0][0].transcript;
        const normalize = value => value.toLowerCase().replace(/[^a-z0-9\s]/g,'').split(/\s+/).filter(Boolean);
        const expected = normalize(target), heard = new Set(normalize(transcript));
        const score = Math.round(expected.filter(word => heard.has(word)).length / expected.length * 100);
        bestSpeakingScore = Math.max(bestSpeakingScore, score);
        document.getElementById('speechResult').classList.remove('d-none'); document.getElementById('speechTranscript').textContent = transcript;
        document.getElementById('speechScoreBar').style.width = `${score}%`; document.getElementById('speechScoreText').textContent = `${score}% de palavras reconhecidas`;
      };
      recognition.onerror = () => { document.getElementById('speechResult').classList.remove('d-none'); document.getElementById('speechTranscript').textContent = 'Não foi possível reconhecer. Verifique a permissão do microfone e tente novamente.'; };
      recognition.onend = () => { startSpeech.disabled = false; startSpeech.innerHTML = '<i class="bi bi-mic-fill"></i> Falar e comparar'; };
      recognition.start();
    });
  }

  const quiz = document.getElementById('readingQuiz');
  data.questions.forEach((question, qIndex) => {
    const block = document.createElement('article'); block.className = 'quiz-question';
    block.innerHTML = `<span>QUESTION ${qIndex + 1}</span><h3>${question.question_en}</h3><p>${question.question_pt}</p><div></div>`;
    const options = block.querySelector('div');
    [...question.options].sort(() => Math.random() - .5).forEach(option => {
      const button = document.createElement('button'); button.type = 'button'; button.textContent = option;
      button.addEventListener('click', () => { options.querySelectorAll('button').forEach(x => { x.disabled = true; if (x.textContent === question.answer) x.classList.add('correct'); }); if (option !== question.answer) button.classList.add('incorrect'); });
      options.appendChild(button);
    }); quiz.appendChild(block);
  });

  document.getElementById('completeReading').addEventListener('click', async event => {
    const button = event.currentTarget; button.disabled = true;
    const response = await fetch(`/aprender/leitura/${data.slug}/concluir`, {method:'POST', headers:{'Content-Type':'application/json','X-CSRF-Token':csrf}, body:JSON.stringify({listen_count:listenCount,speaking_score:bestSpeakingScore})});
    const result = await response.json(); const message = document.getElementById('completionMessage'); message.classList.remove('d-none');
    message.textContent = result.xp_awarded ? `Prática concluída! +${result.xp_awarded} XP.` : 'Prática atualizada. Este texto já havia concedido XP.';
    button.innerHTML = '<i class="bi bi-check-circle-fill"></i> Prática concluída';
  });
})();
