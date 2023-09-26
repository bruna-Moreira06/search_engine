const html = document.querySelector("html");
const button = document.getElementById("color-mode");
console.log(button);

// Initialisation du mode de couleur
const mode = localStorage.getItem("mode");
if (mode) {
  html.setAttribute("data-theme", mode);
  button.innerHTML = mode === "light" ? "🌙" : "☀️";
} else {
  localStorage.setItem("mode", "light");
  button.innerHTML = "☀️";
}

// Modification lors du click
button.addEventListener("click", () => {
  if (html.getAttribute("data-theme") === "dark") {
    html.setAttribute("data-theme", "light");
    localStorage.setItem("mode", "light");
    button.innerHTML = "🌙";
  } else {
    html.setAttribute("data-theme", "dark");
    localStorage.setItem("mode", "dark");
    button.innerHTML = "☀️";
  }
});
