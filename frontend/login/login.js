// Theme controls and persistent preference
const themeToggle = document.querySelector(".theme-toggle");

function updateThemeButton(theme) {
  const nextTheme = theme === "dark" ? "light" : "dark";
  themeToggle.setAttribute("aria-label", `Switch to ${nextTheme} mode`);
  themeToggle.setAttribute("title", `Switch to ${nextTheme} mode`);
}

updateThemeButton(document.documentElement.dataset.theme || "light");

themeToggle.addEventListener("click", () => {
  const currentTheme = document.documentElement.dataset.theme;
  const nextTheme = currentTheme === "dark" ? "light" : "dark";
  document.documentElement.dataset.theme = nextTheme;
  updateThemeButton(nextTheme);

  try {
    localStorage.setItem("compound-lab-theme", nextTheme);
  } catch {
    // Theme switching still works if browser storage is unavailable.
  }
});

