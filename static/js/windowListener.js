document.addEventListener("DOMContentLoaded", () => {
    const closeButtons = document.querySelectorAll('.title-bar-controls button[aria-label="Close"]');

    closeButtons.forEach((button) => {
        button.addEventListener("click", (event) => {
            const windowElement = button.closest('.window');
            if (windowElement) {
                windowElement.style.visibility = 'hidden';
            }
        });
    });
});