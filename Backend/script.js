const reveals = document.querySelectorAll(".reveal");
const menuToggle = document.getElementById("menuToggle");
const mobileMenu = document.getElementById("mobileMenu");
const mobileLinks = mobileMenu ? mobileMenu.querySelectorAll("a") : [];
const contactForm = document.getElementById("contactForm");
const formStatus = document.getElementById("formStatus");
const toast = document.getElementById("toast");

/* REVEAL ANIMATION */
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("active");
      }
    });
  },
  {
    threshold: 0.15,
  }
);

reveals.forEach((item) => observer.observe(item));

/* MOBILE MENU */
if (menuToggle && mobileMenu) {
  menuToggle.addEventListener("click", () => {
    menuToggle.classList.toggle("active");
    mobileMenu.classList.toggle("show");
  });

  mobileLinks.forEach((link) => {
    link.addEventListener("click", () => {
      menuToggle.classList.remove("active");
      mobileMenu.classList.remove("show");
    });
  });
}

/* TOAST FUNCTION */
function showToast(message, type = "success") {
  if (!toast) return;

  toast.textContent = message;
  toast.classList.add("show");

  // Stay visible longer (5 seconds)
  setTimeout(() => {
    toast.classList.remove("show");
  }, 5000);
}

/* CONTACT FORM */
if (contactForm) {
  contactForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = {
      name: document.getElementById("name").value.trim(),
      email: document.getElementById("email").value.trim(),
      message: document.getElementById("message").value.trim(),
    };

    try {
     const response = await fetch("/contact", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (response.ok) {
        showToast(data.message || "Message sent successfully 🚀");
        formStatus.textContent = "";
        contactForm.reset();
      } else {
        formStatus.textContent = data.error || "Something went wrong.";
        showToast(data.error || "Something went wrong.");
      }
    } catch (error) {
      formStatus.textContent = "Server error. Please try again later.";
      showToast("Server error. Please try again later.");
    }
  });
}