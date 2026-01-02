const container = document.getElementById("container");
const registerBtn = document.getElementById("register");
const loginBtn = document.getElementById("login");
  const mobileToggle = document.getElementById('mobileToggle');

registerBtn.addEventListener("click", () => {
  container.classList.add("active");
});

loginBtn.addEventListener("click", () => {
  container.classList.remove("active");
});

  if (mobileToggle) {
    mobileToggle.addEventListener('click', () => {
      container.classList.add("active");
    });
  }


setTimeout(() => {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(a => a.style.display = 'none');
}, 2000);

