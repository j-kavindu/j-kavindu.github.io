/* Progressive enhancements: content and links remain available without JavaScript. */
(() => {
  'use strict';
  const root = document.documentElement;
  const themeButton = document.querySelector('.theme-toggle');
  let storedTheme;
  try { storedTheme = localStorage.getItem('kj-portfolio-theme'); } catch { /* Storage is optional. */ }
  if (storedTheme === 'light' || storedTheme === 'dark') root.dataset.theme = storedTheme;
  const updateThemeButton = () => {
    if (!themeButton) return;
    const light = root.dataset.theme === 'light';
    themeButton.textContent = light ? 'Dark mode' : 'Light mode';
    themeButton.setAttribute('aria-label', `Switch to ${light ? 'dark' : 'light'} theme`);
    themeButton.setAttribute('aria-pressed', String(light));
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = light ? '#f7f8fc' : '#0b1325';
  };
  if (themeButton) {
    themeButton.hidden = false;
    updateThemeButton();
    themeButton.addEventListener('click', () => {
      root.dataset.theme = root.dataset.theme === 'light' ? 'dark' : 'light';
      try { localStorage.setItem('kj-portfolio-theme', root.dataset.theme); } catch { /* Keep current session usable. */ }
      updateThemeButton();
    });
  }
  const menu = document.querySelector('.menu-toggle');
  const nav = document.getElementById('primary-nav');
  if (menu && nav) {
    const mobile = window.matchMedia('(max-width: 760px)');
    const setMenu = expanded => {
      menu.setAttribute('aria-expanded', String(expanded));
      nav.dataset.mobile = mobile.matches && !expanded ? 'collapsed' : 'expanded';
    };
    const resize = () => { menu.hidden = !mobile.matches; setMenu(false); };
    resize();
    if (mobile.addEventListener) mobile.addEventListener('change', resize);
    menu.addEventListener('click', () => setMenu(menu.getAttribute('aria-expanded') !== 'true'));
    nav.addEventListener('click', e => { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && mobile.matches && menu.getAttribute('aria-expanded') === 'true') { setMenu(false); menu.focus(); }
    });
    document.addEventListener('click', e => { if (mobile.matches && !e.target.closest('.site-header')) setMenu(false); });
  }
  const filters = document.querySelector('.filters');
  const projects = [...document.querySelectorAll('[data-project]')];
  const status = document.getElementById('filter-status');
  if (filters && projects.length) {
    filters.hidden = false;
    filters.addEventListener('click', e => {
      const button = e.target.closest('button[data-filter]');
      if (!button) return;
      const category = button.dataset.filter;
      let visible = 0;
      for (const project of projects) {
        project.hidden = category !== 'all' && !project.dataset.category.split(' ').includes(category);
        if (!project.hidden) visible++;
      }
      for (const control of filters.querySelectorAll('button')) control.setAttribute('aria-pressed', String(control === button));
      if (status) status.textContent = `${visible} ${visible === 1 ? 'project' : 'projects'}${category === 'all' ? '' : ` · ${button.textContent}`}`;
    });
  }
})();
