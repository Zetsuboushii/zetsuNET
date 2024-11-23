document.addEventListener("DOMContentLoaded", () => {
    const tabs = document.querySelectorAll('[role="tab"]');
    const panels = document.querySelectorAll('.tabpanel');

    tabs.forEach((tab) => {
        tab.addEventListener("click", () => {
            tabs.forEach((t) => t.setAttribute("aria-selected", "false"));
            panels.forEach((p) => p.setAttribute("aria-hidden", "true"));

            tab.setAttribute("aria-selected", "true");
            const tabId = tab.getAttribute("data-tab");
            document.getElementById(tabId).setAttribute("aria-hidden", "false");
        });
    });
});