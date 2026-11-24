import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

// ===========================================================
// SUPABASE CLIENT & AUTH NAVIGATION SYNC
// ===========================================================

// Base Supabase project URL (no /rest/v1 suffix) and public browser publishable key
const SUPABASE_URL = "https://ulnzqrwzomzzopvocvzj.supabase.co";
const SUPABASE_ANON_KEY = "<your-full-publishable-key>";
const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Top-bar link that switches between "Sign in" and the signed-in user's email
const authNavLink = document.querySelector("#auth-nav-link");
const logoutButton = document.querySelector("#logout-button");

// Reads the current session and updates the auth link text, href, and state
async function syncAuthNav() {
  if (!authNavLink) return;
  const { data } = await supabase.auth.getSession();
  const user = data?.session?.user;

  if (user) {
    authNavLink.textContent = user.email;
    authNavLink.title = `Signed in as ${user.email}`;
    authNavLink.href = "#";
    authNavLink.dataset.signedIn = "true";
    if (logoutButton) logoutButton.hidden = false;
  } else {
    authNavLink.textContent = "Sign in";
    authNavLink.title = "Sign in to Compound Lab";
    authNavLink.href = "./login/login.html";
    authNavLink.dataset.signedIn = "false";
    if (logoutButton) logoutButton.hidden = true;
  }
}

logoutButton?.addEventListener("click", async () => {
  logoutButton.disabled = true;
  try {
    await supabase.auth.signOut();
    await syncAuthNav();
  } finally {
    logoutButton.disabled = false;
  }
});

// Sign the user out when clicking the link while already signed in
authNavLink?.addEventListener("click", async (event) => {
  if (authNavLink.dataset.signedIn === "true") {
    event.preventDefault();
    await supabase.auth.signOut();
    await syncAuthNav();
  }
});

// Keep the header in sync whenever sign-in or sign-out happens
supabase.auth.onAuthStateChange(() => {
  syncAuthNav();
});

// Run initial auth check on page load
syncAuthNav();

// ===========================================================
// UI CONTROLS (THEME, MOBILE MENU & TOASTS)
// ===========================================================

const menuButton = document.querySelector(".menu-button");
const navigation = document.querySelector(".main-nav");
const toast = document.querySelector(".toast");
const toastMessage = document.querySelector(".toast-message");
const themeToggle = document.querySelector(".theme-toggle");
let toastTimer;

// Update the theme toggle button's accessible label and tooltip for the next mode
function updateThemeButton(theme) {
  const nextTheme = theme === "dark" ? "light" : "dark";
  themeToggle.setAttribute("aria-label", `Switch to ${nextTheme} mode`);
  themeToggle.setAttribute("title", `Switch to ${nextTheme} mode`);
}

updateThemeButton(document.documentElement.dataset.theme || "light");

// Toggle light/dark theme and persist preference in localStorage
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

// Close the mobile navigation drawer and reset aria-expanded
function closeMenu() {
  navigation.classList.remove("is-open");
  menuButton.setAttribute("aria-expanded", "false");
}

// Toggle mobile navigation menu open/closed
menuButton.addEventListener("click", () => {
  const isOpen = navigation.classList.toggle("is-open");
  menuButton.setAttribute("aria-expanded", String(isOpen));
});

// Automatically close the mobile menu after selecting a nav link
navigation.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", closeMenu);
});

// Display a temporary toast notification for elements marked with [data-launch]
document.querySelectorAll("[data-launch]").forEach((button) => {
  button.addEventListener("click", () => {
    clearTimeout(toastTimer);
    toastMessage.textContent = `${button.dataset.launch} is coming soon!`;
    toast.classList.add("is-visible");
    closeMenu();

    toastTimer = window.setTimeout(() => {
      toast.classList.remove("is-visible");
    }, 2800);
  });
});