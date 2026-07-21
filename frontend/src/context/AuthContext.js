import { jsx as _jsx } from "react/jsx-runtime";
import { createContext, useContext, useEffect, useState, } from "react";
import { api } from "../api/client";
const AuthContext = createContext(undefined);
export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        api
            .get("/auth/csrf/")
            .then(() => api.get("/auth/me/"))
            .then((res) => setUser(res.data.user))
            .catch(() => setUser(null))
            .finally(() => setLoading(false));
    }, []);
    async function login(email, password) {
        await api.get("/auth/csrf/");
        const res = await api.post("/auth/login/", { email, password });
        setUser(res.data);
    }
    async function logout() {
        await api.post("/auth/logout/");
        setUser(null);
    }
    return (_jsx(AuthContext.Provider, { value: { user, loading, login, logout }, children: children }));
}
export function useAuth() {
    const ctx = useContext(AuthContext);
    if (!ctx)
        throw new Error("useAuth must be used within AuthProvider");
    return ctx;
}
