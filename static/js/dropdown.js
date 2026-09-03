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

document.addEventListener("DOMContentLoaded", function () {
  /*
    |--------------------------------------------------------------------------
    | Type of Accident
    |--------------------------------------------------------------------------
    */

  const accidentButton = document.getElementById("accidentDropdownButton");

  const accidentDropdown = document.getElementById("accidentDropdown");

  const accidentText = document.getElementById("accidentDropdownText");

  const accidentIcon = document.getElementById("accidentDropdownIcon");

  /*
    |--------------------------------------------------------------------------
    | Type of Injury
    |--------------------------------------------------------------------------
    */

  const injuryButton = document.getElementById("injuryDropdownButton");

  const injuryDropdown = document.getElementById("injuryDropdown");

  const injuryText = document.getElementById("injuryDropdownText");

  const injuryIcon = document.getElementById("injuryDropdownIcon");

  /*
    |--------------------------------------------------------------------------
    | Helper - Update Accident Text
    |--------------------------------------------------------------------------
    */

  function updateAccidentText() {
    const checked = accidentDropdown.querySelectorAll(
      'input[type="checkbox"]:checked',
    );

    if (checked.length === 0) {
      accidentText.textContent = "Select accident type";
      accidentText.classList.add("text-slate-400");
      accidentText.classList.remove("text-slate-700");

      return;
    }

    const labels = [];

    checked.forEach(function (checkbox) {
      const label = checkbox.closest("label").querySelector("span");

      if (label) {
        labels.push(label.textContent.trim());
      }
    });

    if (labels.length === 1) {
      accidentText.textContent = labels[0];
    } else {
      accidentText.textContent = labels.length + " accident types selected";
    }

    accidentText.classList.remove("text-slate-400");
    accidentText.classList.add("text-slate-700");
  }

  /*
    |--------------------------------------------------------------------------
    | Helper - Update Injury Text
    |--------------------------------------------------------------------------
    */

  function updateInjuryText() {
    const checked = injuryDropdown.querySelectorAll(
      'input[type="checkbox"]:checked',
    );

    if (checked.length === 0) {
      injuryText.textContent = "Select injury type";
      injuryText.classList.add("text-slate-400");
      injuryText.classList.remove("text-slate-700");

      return;
    }

    const labels = [];

    checked.forEach(function (checkbox) {
      const label = checkbox.closest("label").querySelector("span");

      if (label) {
        labels.push(label.textContent.trim());
      }
    });

    if (labels.length === 1) {
      injuryText.textContent = labels[0];
    } else {
      injuryText.textContent = labels.length + " injury types selected";
    }

    injuryText.classList.remove("text-slate-400");
    injuryText.classList.add("text-slate-700");
  }

  /*
    |--------------------------------------------------------------------------
    | Open / Close Accident Dropdown
    |--------------------------------------------------------------------------
    */

  accidentButton.addEventListener("click", function (event) {
    event.stopPropagation();

    const isOpen = !accidentDropdown.classList.contains("hidden");

    // Close injury dropdown
    injuryDropdown.classList.add("hidden");
    injuryIcon.classList.remove("rotate-180");

    if (isOpen) {
      accidentDropdown.classList.add("hidden");
      accidentIcon.classList.remove("rotate-180");
    } else {
      accidentDropdown.classList.remove("hidden");
      accidentIcon.classList.add("rotate-180");
    }
  });

  /*
    |--------------------------------------------------------------------------
    | Open / Close Injury Dropdown
    |--------------------------------------------------------------------------
    */

  injuryButton.addEventListener("click", function (event) {
    event.stopPropagation();

    const isOpen = !injuryDropdown.classList.contains("hidden");

    // Close accident dropdown
    accidentDropdown.classList.add("hidden");
    accidentIcon.classList.remove("rotate-180");

    if (isOpen) {
      injuryDropdown.classList.add("hidden");
      injuryIcon.classList.remove("rotate-180");
    } else {
      injuryDropdown.classList.remove("hidden");
      injuryIcon.classList.add("rotate-180");
    }
  });

  /*
    |--------------------------------------------------------------------------
    | Checkbox Changes
    |--------------------------------------------------------------------------
    */

  accidentDropdown
    .querySelectorAll('input[type="checkbox"]')
    .forEach(function (checkbox) {
      checkbox.addEventListener("change", function () {
        updateAccidentText();
      });
    });

  injuryDropdown
    .querySelectorAll('input[type="checkbox"]')
    .forEach(function (checkbox) {
      checkbox.addEventListener("change", function () {
        updateInjuryText();
      });
    });

  /*
    |--------------------------------------------------------------------------
    | Close dropdown when clicking outside
    |--------------------------------------------------------------------------
    */

  document.addEventListener("click", function (event) {
    if (
      !accidentDropdown.contains(event.target) &&
      !accidentButton.contains(event.target)
    ) {
      accidentDropdown.classList.add("hidden");
      accidentIcon.classList.remove("rotate-180");
    }

    if (
      !injuryDropdown.contains(event.target) &&
      !injuryButton.contains(event.target)
    ) {
      injuryDropdown.classList.add("hidden");
      injuryIcon.classList.remove("rotate-180");
    }
  });

  /*
    |--------------------------------------------------------------------------
    | Initial state
    |--------------------------------------------------------------------------
    */

  updateAccidentText();
  updateInjuryText();
});
