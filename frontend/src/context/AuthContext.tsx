import {
    createContext,
    useContext,
    useEffect,
    useState,
    ReactNode,
} from "react";
import { api } from "../api/client";

interface User {
    id: number;
    email: string;
    full_name: string;
    department: string;
    phone: string;
}

interface AuthContextValue {
    user: User | null;
    loading: boolean;
    login: (email: string, password: string) => Promise<void>;
    logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api
            .get("/auth/csrf/")
            .then(() => api.get("/auth/me/"))
            .then((res) => setUser(res.data.user))
            .catch(() => setUser(null))
            .finally(() => setLoading(false));
    }, []);

    async function login(email: string, password: string) {
        await api.get("/auth/csrf/");
        const res = await api.post("/auth/login/", { email, password });
        setUser(res.data);
    }

    async function logout() {
        await api.post("/auth/logout/");
        setUser(null);
    }

    return (
        <AuthContext.Provider value={{ user, loading, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error("useAuth must be used within AuthProvider");
    return ctx;
}
