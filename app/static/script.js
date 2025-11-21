// Smooth fade-in animation on page load
document.addEventListener("DOMContentLoaded", () => {
    document.body.style.opacity = "1";
});

// Add small click animation for buttons
document.querySelectorAll(".btn").forEach(btn => {
    btn.addEventListener("mousedown", () => {
        btn.style.transform = "scale(0.96)";
    });
    btn.addEventListener("mouseup", () => {
        btn.style.transform = "scale(1)";
    });
});
