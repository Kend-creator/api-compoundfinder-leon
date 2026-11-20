const menuButton = document.querySelector(".menu-button");
const navigation = document.querySelector(".main-nav");
const toast = document.querySelector(".toast");
const toastMessage = document.querySelector(".toast-message");
const themeToggle = document.querySelector(".theme-toggle");
let toastTimer;

/* Update the theme toggle button based on the current theme */
function updateThemeButton(theme) {
  const nextTheme = theme === "dark" ? "light" : "dark";
  themeToggle.setAttribute("aria-label", `Switch to ${nextTheme} mode`);
  themeToggle.setAttribute("title", `Switch to ${nextTheme} mode`);
}

updateThemeButton(document.documentElement.dataset.theme || "light");

/* Toggle the theme when the theme toggle button is clicked */
themeToggle.addEventListener("click", () => {
  const currentTheme = document.documentElement.dataset.theme;
  const nextTheme = currentTheme === "dark" ? "light" : "dark";
  document.documentElement.dataset.theme = nextTheme;
  updateThemeButton(nextTheme);

  try {
    localStorage.setItem("compound-lab-theme", nextTheme);
  } catch {
    // The theme still changes when storage is unavailable.
  }
});

/* Close the mobile menu when a link is clicked */
function closeMenu() {
  navigation.classList.remove("is-open");
  menuButton.setAttribute("aria-expanded", "false");
}

menuButton.addEventListener("click", () => {
  const isOpen = navigation.classList.toggle("is-open");
  menuButton.setAttribute("aria-expanded", String(isOpen));
});

navigation.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", closeMenu);
});

/* Toast and Toast Timer */
document.querySelectorAll("[data-launch]").forEach((button) => {
  button.addEventListener("click", () => {
    clearTimeout(toastTimer);
    toastMessage.textContent = `${button.dataset.launch} is ready for your API connection.`;
    toast.classList.add("is-visible");
    closeMenu();

    toastTimer = window.setTimeout(() => {
      toast.classList.remove("is-visible");
    }, 2800);
  });
});