document.addEventListener("DOMContentLoaded", () => {
    loadThemePreference();
    document.getElementById("toggleThemeBtn").addEventListener("click", toggleTheme);
    document.getElementById("renderBtn").addEventListener("click", renderTemplate);
});

const elements = {
    template: document.getElementById("template"),
    variables: document.getElementById("variables"),
    outputDiv: document.getElementById("output"),
    outputContainer: document.getElementById("output-container"),
    loading: document.getElementById("loading"),
    errorAlert: document.getElementById("errorAlert")
};

function toggleTheme() {
    const html = document.documentElement;
    const theme = html.getAttribute("data-bs-theme") === "dark" ? "light" : "dark";
    html.setAttribute("data-bs-theme", theme);
    document.getElementById("themeIcon").textContent = theme === "dark" ? "☀️" : "🌙";
    localStorage.setItem("theme", theme);
}

function loadThemePreference() {
    const theme = localStorage.getItem("theme") || "dark";
    document.documentElement.setAttribute("data-bs-theme", theme);
    document.getElementById("themeIcon").textContent = theme === "dark" ? "☀️" : "🌙";
}

async function renderTemplate() {
    const template = elements.template.value.trim();
    const variables = elements.variables.value.trim();

    // Validate input
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
}

function showError(message) {
    elements.errorAlert.textContent = message;
    toggleVisibility(elements.errorAlert, true);
}

function toggleVisibility(element, show) {
    element.classList.toggle("d-none", !show);
}

