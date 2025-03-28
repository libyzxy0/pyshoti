const menuButton = document.getElementById("menu-btn");
const navbar = document.getElementById("navbar");
const navItems = document.getElementById("nav-items");

let isMenuOpen = false;

menuButton.addEventListener("click", () => {
  isMenuOpen = !isMenuOpen;

  if (isMenuOpen) {
    menuButton.innerHTML = `<ion-icon name="close-outline"></ion-icon>`;
    navbar.style.backgroundColor = "#00060c";
    navItems.style.top = "3.5rem";

    navbar.style.borderBottom = "1.3px solid #111111";
  } else {
    menuButton.innerHTML = `<ion-icon name="menu-outline"></ion-icon>`;
    navbar.style.backgroundColor = "transparent";
    navItems.style.top = "-15rem";

    navbar.style.borderBottom = "none";
  }
});
