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
            case "cherry":
                themePath = "/static/css/cherry.css";
                break;
            case "cherryb":
                themePath = "/static/css/cherryb.css";
                break;
            case "black":
            default:
                themePath = "/static/css/black.css";
        }

        themeStylesheet.setAttribute("href", themePath);
    }
});
