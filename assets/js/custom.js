// Close the top-left persona dropdown when clicking outside or pressing Escape.
const wordmarkMenu = document.querySelector("details.wordmark-menu");
if (wordmarkMenu) {
  document.addEventListener("click", (event) => {
    if (wordmarkMenu.open && !wordmarkMenu.contains(event.target)) {
      wordmarkMenu.open = false;
    }
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") wordmarkMenu.open = false;
  });
}
