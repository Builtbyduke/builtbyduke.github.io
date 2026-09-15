(() => {
  const navToggle = document.querySelector(".nav-toggle");
  const siteNav = document.querySelector(".site-nav");

  if (navToggle && siteNav) {
    navToggle.addEventListener("click", () => {
      const expanded = navToggle.getAttribute("aria-expanded") === "true";
      navToggle.setAttribute("aria-expanded", String(!expanded));
      siteNav.classList.toggle("is-open");
    });
  }

  const year = document.getElementById("year");
  if (year) {
    year.textContent = String(new Date().getFullYear());
  }

  const revealNodes = document.querySelectorAll(".reveal");
  if (revealNodes.length > 0 && "IntersectionObserver" in window) {
    const revealObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 }
    );

    revealNodes.forEach((node) => revealObserver.observe(node));
  } else {
    revealNodes.forEach((node) => node.classList.add("is-visible"));
  }

  const copyButtons = document.querySelectorAll("[data-copy]");
  copyButtons.forEach((button) => {
    button.addEventListener("click", async () => {
      const value = button.getAttribute("data-copy") || "";
      try {
        await navigator.clipboard.writeText(value);
        const original = button.textContent;
        button.textContent = "Copied";
        setTimeout(() => {
          button.textContent = original;
        }, 1200);
      } catch {
        alert("Copy failed. Please copy manually: " + value);
      }
    });
  });

  const aiLockButton = document.getElementById("aiLockButton");
  const aiLockStatus = document.getElementById("aiLockStatus");

  if (aiLockButton && aiLockStatus) {
    aiLockButton.addEventListener("click", () => {
      const input = prompt("Enter passphrase");
      if (input === null) return;

      if (input.trim() === "FISHERTHECAT") {
        aiLockStatus.textContent = "Access granted: local AI panel placeholder unlocked.";
      } else {
        aiLockStatus.textContent = "Access denied: invalid passphrase.";
      }
    });
  }
})();
