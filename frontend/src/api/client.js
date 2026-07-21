import axios from "axios";
function getCookie(name) {
    const match = document.cookie.match(new RegExp(`(^| )${name}=([^;]+)`));
    return match ? decodeURIComponent(match[2]) : null;
}
export const api = axios.create({
    baseURL: "/api",
    withCredentials: true,
});
api.interceptors.request.use((config) => {
    const csrfToken = getCookie("csrftoken");
    if (csrfToken && config.method !== "get") {
        config.headers = config.headers ?? {};
        config.headers["X-CSRFToken"] = csrfToken;
    }
    return config;
});
