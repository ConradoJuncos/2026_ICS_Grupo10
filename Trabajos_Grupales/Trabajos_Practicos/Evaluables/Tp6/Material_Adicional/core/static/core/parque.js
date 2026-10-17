/* La consulta funciona con HTML; este código facilita la selección y el foco. */
(() => {
  const select = document.querySelector('#id_actividad');
  const age = document.querySelector('#id_edad');
  document.querySelectorAll('[data-activity]').forEach((link) => {
    link.addEventListener('click', () => {
      select.value = link.dataset.activity;
      age.focus({ preventScroll: true });
    });
  });
  const feedback = document.querySelector('.field-error, .result');
  if (feedback) {
    const target = document.querySelector('[aria-invalid="true"]') || feedback;
    target.focus({ preventScroll: true });
  }
})();
