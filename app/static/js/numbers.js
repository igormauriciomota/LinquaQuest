(() => {
  const words = ['oh','one','two','three','four','five','six','seven','eight','nine'];
  const digits = document.getElementById('phoneDigits');
  const spoken = document.getElementById('phoneWords');
  if (!digits || !spoken) return;
  let raw = '31967305801';
  function render() {
    digits.textContent = `(${raw.slice(0,2)}) ${raw.slice(2,7)}-${raw.slice(7)}`;
    spoken.textContent = `${[...raw.slice(0,2)].map(x=>words[x]).join(' ')} · ${[...raw.slice(2,7)].map(x=>words[x]).join(' ')} · ${[...raw.slice(7)].map(x=>words[x]).join(' ')}`;
  }
  document.getElementById('newPhone').addEventListener('click', () => { raw = Array.from({length:11},(_,i)=> i===0 ? String(1+Math.floor(Math.random()*8)) : String(Math.floor(Math.random()*10))).join(''); render(); });
  document.getElementById('hearPhone').addEventListener('click', () => window.LinguaQuest.speak([...raw].map(x=>words[x]).join(', '), .7));
  document.getElementById('toggleWords').addEventListener('click', () => spoken.classList.toggle('invisible'));
  render();
})();
