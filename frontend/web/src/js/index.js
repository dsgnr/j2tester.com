window.onload = () => {
    loadThemePreference();
    document.getElementById("toggleThemeBtn").addEventListener("click", toggleTheme);
    document.getElementById("renderBtn").addEventListener("click", renderTemplate);
};

const elements = {
    template: document.getElementById("template"),
    variables: document.getElementById("variables"),
    outputDiv: document.getElementById("output"),
    outputContainer: document.getElementById("output-container"),
    loading: document.getElementById("loading"),
    errorAlert: document.getElementById("errorAlert"),
    themeIcon: document.getElementById("themeIcon"),
    html: document.documentElement
};

const toggleVisibility = (element, show) => element.classList.toggle("d-none", !show);

const toggleTheme = () => {
    const isDark = elements.html.dataset.bsTheme === "dark";
    elements.html.dataset.bsTheme = isDark ? "light" : "dark";
    elements.themeIcon.textContent = isDark ? "🌙" : "☀️";
    localStorage.setItem("theme", isDark ? "light" : "dark");
};

const loadThemePreference = () => {
    const theme = localStorage.getItem("theme") || "dark";
    elements.html.dataset.bsTheme = theme;
    elements.themeIcon.textContent = theme === "dark" ? "☀️" : "🌙";
};

const showError = (message) => {
    elements.errorAlert.textContent = message;
    toggleVisibility(elements.errorAlert, true);
};

const renderTemplate = async () => {
    const template = elements.template.value.trim();
    const variables = elements.variables.value.trim();

    if (!template) return showError("Template input cannot be empty.");

    toggleVisibility(elements.errorAlert, false);
    toggleVisibility(elements.outputContainer, false);
    toggleVisibility(elements.loading, true);

    try {
        const response = await fetch("/api/render", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ template, variables })
        });

        const result = await response.json();
        toggleVisibility(elements.loading, false);

        if (result.rendered) {
            elements.outputDiv.textContent = result.rendered;
            hljs.highlightElement(elements.outputDiv);
            toggleVisibility(elements.outputContainer, true);
        } else {
            showError(result.error || "Unknown error occurred.");
        }
    } catch {
        toggleVisibility(elements.loading, false);
        showError("Failed to connect to API.");
    }
};
