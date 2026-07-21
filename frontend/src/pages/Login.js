import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
export default function Login() {
    const { user, login } = useAuth();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(null);
    const [submitting, setSubmitting] = useState(false);
    if (user)
        return _jsx(Navigate, { to: "/dashboard", replace: true });
    async function handleSubmit(e) {
        e.preventDefault();
        setError(null);
        setSubmitting(true);
        try {
            await login(email, password);
        }
        catch {
            setError("Invalid email or password.");
        }
        finally {
            setSubmitting(false);
        }
    }
    return (_jsx("main", { className: "form-shell", children: _jsxs("section", { className: "auth-card", children: [_jsxs("div", { className: "auth-brand", children: [_jsx("span", { className: "brand-mark", children: "E" }), _jsxs("div", { children: [_jsx("strong", { className: "auth-brand-title", children: "Elecbits" }), _jsx("span", { className: "auth-brand-subtitle", children: "ATS RES-Hive" })] })] }), _jsx("h1", { className: "auth-title", children: "Sign in" }), _jsx("p", { className: "auth-text", children: "Sign in to manage candidates, job roles, and hiring activity." }), _jsxs("form", { onSubmit: handleSubmit, className: "login-form", children: [error && _jsx("div", { className: "form-errors", children: error }), _jsxs("div", { className: "form-group", children: [_jsx("label", { htmlFor: "email", children: "Email" }), _jsx("input", { id: "email", type: "email", className: "form-control", value: email, onChange: (e) => setEmail(e.target.value), required: true })] }), _jsxs("div", { className: "form-group", children: [_jsx("label", { htmlFor: "password", children: "Password" }), _jsx("input", { id: "password", type: "password", className: "form-control", value: password, onChange: (e) => setPassword(e.target.value), required: true })] }), _jsx("button", { type: "submit", className: "btn btn-primary login-submit", disabled: submitting, children: submitting ? "Signing in..." : "Sign In" })] })] }) }));
}
