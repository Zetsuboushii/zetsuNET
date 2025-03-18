document.addEventListener("DOMContentLoaded", function () {
    const tabs = document.querySelectorAll("menu[role='tablist'] button");
    const tabPanels = document.querySelectorAll("article[role='tabpanel']");

    tabs.forEach(tab => {
        tab.addEventListener("click", function () {
            tabs.forEach(t => t.setAttribute("aria-selected", "false"));
            tabPanels.forEach(panel => panel.hidden = true);

            this.setAttribute("aria-selected", "true");
            const tabId = this.getAttribute("aria-controls");
            document.getElementById(tabId).hidden = false;
        });
    });
});