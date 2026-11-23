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

// Password visibility control
const passwordInput = document.querySelector("#password");
const passwordToggle = document.querySelector(".password-toggle");

passwordToggle.addEventListener("click", () => {
  const isVisible = passwordInput.type === "text";
  passwordInput.type = isVisible ? "password" : "text";
  passwordToggle.classList.toggle("is-visible", !isVisible);
  passwordToggle.setAttribute("aria-label", isVisible ? "Show password" : "Hide password");
});

// Frontend validation and status messaging
const form = document.querySelector(".login-form");
const emailInput = document.querySelector("#email");
const statusMessage = document.querySelector(".form-status");

function setFieldError(input, message) {
  const shell = input.closest(".input-shell");
  const error = document.querySelector(`#${input.getAttribute("aria-describedby")}`);
  shell.classList.toggle("is-invalid", Boolean(message));
  input.setAttribute("aria-invalid", String(Boolean(message)));
  error.textContent = message;
}

function validateForm() {
  const emailValue = emailInput.value.trim();
  const passwordValue = passwordInput.value;
  const emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailValue);

  setFieldError(
    emailInput,
    !emailValue ? "Enter your email address." : emailValid ? "" : "Enter a valid email address.",
  );
  setFieldError(
    passwordInput,
    !passwordValue
      ? "Enter your password."
      : passwordValue.length < 8
        ? "Password must contain at least 8 characters."
        : "",
  );

  return emailValid && passwordValue.length >= 8;
}

[emailInput, passwordInput].forEach((input) => {
  input.addEventListener("input", () => {
    if (input.getAttribute("aria-invalid") === "true") validateForm();
    statusMessage.classList.remove("is-visible");
    statusMessage.textContent = "";
  });
});

form.addEventListener("submit", (event) => {
  event.preventDefault();
  if (!validateForm()) return;

  statusMessage.textContent =
    "Login interface validated successfully. Connect an authentication service to sign in.";
  statusMessage.classList.add("is-visible");
});

// Non-authentication actions explain their current frontend-only state
document.querySelector(".forgot-link").addEventListener("click", () => {
  statusMessage.textContent =
    "Password recovery will become available when authentication is connected.";
  statusMessage.classList.add("is-visible");
});

document.querySelector(".signup-link").addEventListener("click", () => {
  statusMessage.textContent =
    "Account creation will become available when authentication is connected.";
  statusMessage.classList.add("is-visible");
});
