function configureAxiosCsrf() {
    if (!window.axios) {
        return;
    }

    const token = document.querySelector('meta[name="_csrf"]')?.content;
    const header = document.querySelector('meta[name="_csrf_header"]')?.content;

    if (token && header) {
        axios.defaults.headers.common[header] = token;
    }
}

configureAxiosCsrf();

<script th:src="@{/js/security.js}"></script>
