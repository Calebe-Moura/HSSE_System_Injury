document.addEventListener("DOMContentLoaded", () => {
  const button = document.getElementById("user-menu-button");
  const dropdown = document.getElementById("user-menu-dropdown");
  const arrow = document.getElementById("user-menu-arrow");
  const menu = document.getElementById("user-menu");

  if (!button || !dropdown || !menu) {
    return;
  }

  button.addEventListener("click", (event) => {
    event.stopPropagation();

    const isOpen = !dropdown.classList.contains("hidden");

    if (isOpen) {
      dropdown.classList.add("hidden");
      button.setAttribute("aria-expanded", "false");

      if (arrow) {
        arrow.classList.remove("rotate-180");
      }
    } else {
      dropdown.classList.remove("hidden");
      button.setAttribute("aria-expanded", "true");

      if (arrow) {
        arrow.classList.add("rotate-180");
      }
    }
  });

  document.addEventListener("click", (event) => {
    if (!menu.contains(event.target)) {
      dropdown.classList.add("hidden");
      button.setAttribute("aria-expanded", "false");

      if (arrow) {
        arrow.classList.remove("rotate-180");
      }
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      dropdown.classList.add("hidden");
      button.setAttribute("aria-expanded", "false");

      if (arrow) {
        arrow.classList.remove("rotate-180");
      }
    }
  });
});
