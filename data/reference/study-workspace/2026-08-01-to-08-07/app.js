const progressKey = 'goha-study-week-2026-08-07';
const checks = [...document.querySelectorAll('[data-progress]')];
const saved = JSON.parse(localStorage.getItem(progressKey) || '{}');

function updateProgress() {
  const done = checks.filter((item) => item.checked).length;
  const percent = Math.round((done / checks.length) * 100);
  document.querySelector('#progressValue').textContent = `${percent}%`;
  localStorage.setItem(progressKey, JSON.stringify(Object.fromEntries(checks.map((item) => [item.dataset.progress, item.checked]))));
}

checks.forEach((item) => {
  item.checked = Boolean(saved[item.dataset.progress]);
  item.addEventListener('change', updateProgress);
});
updateProgress();

const filters = [...document.querySelectorAll('[data-filter]')];
const modules = [...document.querySelectorAll('[data-category]')];
filters.forEach((button) => button.addEventListener('click', () => {
  filters.forEach((item) => item.classList.toggle('active', item === button));
  const filter = button.dataset.filter;
  modules.forEach((card) => card.classList.toggle('hidden', filter !== 'all' && !card.dataset.category.split(' ').includes(filter)));
}));
