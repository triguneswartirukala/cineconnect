document.addEventListener("DOMContentLoaded", () => {
    const intro = document.getElementById("intro");

    // If intro already shown in this session
    if (sessionStorage.getItem("introShown")) {
        intro.remove();
        return;
    }

    // Mark intro as shown
    sessionStorage.setItem("introShown", "true");

    // Fade out intro
    setTimeout(() => {
        intro.style.opacity = "0";
    }, 900);

    setTimeout(() => {
        intro.remove();
    }, 1500);
});
