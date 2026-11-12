// Patička drží aktuální rok. Bez JavaScriptu zůstane rok z HTML.
document.querySelectorAll("[data-year]").forEach(function (el) {
  el.textContent = String(new Date().getFullYear());
});
