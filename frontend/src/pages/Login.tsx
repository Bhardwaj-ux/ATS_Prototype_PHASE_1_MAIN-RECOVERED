import { FormEvent, useState } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
    const { user, login } = useAuth();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState<string | null>(null);
    const [submitting, setSubmitting] = useState(false);

    if (user) return <Navigate to="/dashboard" replace />;

    async function handleSubmit(e: FormEvent) {
        e.preventDefault();
        setError(null);
        setSubmitting(true);
        try {
            await login(email, password);
        } catch {
            setError("Invalid email or password.");
        } finally {
            setSubmitting(false);
        }
    }

    return (
        <main className="form-shell">
            <section className="auth-card">
                <div className="auth-brand">
                    <span className="brand-mark">E</span>
                    <div>
                        <strong className="auth-brand-title">Elecbits</strong>
                        <span className="auth-brand-subtitle">ATS RES-Hive</span>
                    </div>
                </div>

                <h1 className="auth-title">Sign in</h1>
                <p className="auth-text">
                    Sign in to manage candidates, job roles, and hiring activity.
                </p>

                <form onSubmit={handleSubmit} className="login-form">
                    {error && <div className="form-errors">{error}</div>}
                    <div className="form-group">
                        <label htmlFor="email">Email</label>
                        <input
                            id="email"
                            type="email"
                            className="form-control"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <input
                            id="password"
                            type="password"
                            className="form-control"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <button
                        type="submit"
                        className="btn btn-primary login-submit"
                        disabled={submitting}
                    >
                        {submitting ? "Signing in..." : "Sign In"}
                    </button>
                </form>
            </section>
        </main>
    );
}
