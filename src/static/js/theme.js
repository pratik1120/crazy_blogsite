document.addEventListener("DOMContentLoaded", function () {
    const themeSelect = document.getElementById("theme-select");
    const savedTheme = localStorage.getItem("selectedTheme");
    if (savedTheme) {
        applyTheme(savedTheme);
        themeSelect.value = savedTheme;
    }
    themeSelect.addEventListener("change", function () {
        const selectedTheme = themeSelect.value;
        applyTheme(selectedTheme);
        localStorage.setItem("selectedTheme", selectedTheme);
    });

    function applyTheme(theme) {
        const themeStylesheet = document.getElementById("theme-stylesheet");
        let themePath;
        switch (theme) {
            case "theme2":
                themePath = "/static/css/theme2.css";
                break;
            case "theme1":
            default:
                themePath = "/static/css/theme1";
        }

        themeStylesheet.setAttribute("href", themePath);
    }
});
