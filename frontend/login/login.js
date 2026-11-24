import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = "https://ulnzqrwzomzzopvocvzj.supabase.co";
const SUPABASE_ANON_KEY = "<your-full-publishable-key>";
const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

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

// Form validation and status messaging
const form = document.querySelector(".login-form");
const emailInput = document.querySelector("#email");
const rememberInput = document.querySelector('input[name="remember"]');
const statusMessage = document.querySelector(".form-status");
const submitButton = form.querySelector(".submit-button");

function showStatus(message) {
  statusMessage.textContent = message;
  statusMessage.classList.add("is-visible");
}

function getRedirectTarget() {
  const params = new URLSearchParams(window.location.search);
  const next = params.get("next");
  if (next && next.startsWith("/") && !next.startsWith("//")) {
    return next;
  }
  return "../index.html";
}

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

// If already signed in, return to the lab
const { data: initialSession } = await supabase.auth.getSession();
if (initialSession?.session) {
  window.location.replace(getRedirectTarget());
}

[emailInput, passwordInput].forEach((input) => {
  input.addEventListener("input", () => {
    if (input.getAttribute("aria-invalid") === "true") validateForm();
    statusMessage.classList.remove("is-visible");
    statusMessage.textContent = "";
  });
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!validateForm()) return;

  submitButton.disabled = true;
  showStatus("Signing in to Compound Lab...");

  const { error } = await supabase.auth.signInWithPassword({
    email: emailInput.value.trim(),
    password: passwordInput.value,
  });

  if (error) {
    submitButton.disabled = false;
    showStatus(error.message || "Could not sign in. Check your credentials.");
    return;
  }

  try {
    localStorage.setItem("compound-lab-remember", String(Boolean(rememberInput?.checked)));
  } catch {
    // Ignore storage errors in restricted browsing modes.
  }

  showStatus("Signed in! Redirecting to the lab...");
  window.location.assign(getRedirectTarget());
});

// Password recovery
document.querySelector(".forgot-link").addEventListener("click", async () => {
  const emailValue = emailInput.value.trim();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailValue)) {
    setFieldError(emailInput, "Enter your email address first to reset your password.");
    emailInput.focus();
    return;
  }

  const { error } = await supabase.auth.resetPasswordForEmail(emailValue, {
    redirectTo: window.location.origin + window.location.pathname,
  });

  if (error) {
    showStatus(error.message || "Unable to send reset email.");
    return;
  }

  showStatus("Password reset instructions sent if an account exists for that email.");
});

// Account creation
document.querySelector(".signup-link").addEventListener("click", async () => {
  if (!validateForm()) return;

  submitButton.disabled = true;
  showStatus("Creating your Compound Lab account...");

  const { data, error } = await supabase.auth.signUp({
    email: emailInput.value.trim(),
    password: passwordInput.value,
  });

  submitButton.disabled = false;

  if (error) {
    showStatus(error.message || "Could not create account.");
    return;
  }

  if (data?.session) {
    showStatus("Account created! Redirecting to the lab...");
    window.location.assign(getRedirectTarget());
  } else {
    showStatus("Account created! Check your email to confirm your address before signing in.");
  }
});