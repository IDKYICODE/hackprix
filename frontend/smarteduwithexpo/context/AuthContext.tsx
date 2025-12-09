// context/AuthContext.tsx
import React, {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";
import { Alert } from "react-native";
import {
  loginRequest,
  fetchCurrentUser,
  clearTokens,
} from "../lib/authClient";

export interface User {
  id: number;
  username: string;
  email?: string;
  role?: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider: React.FC<React.PropsWithChildren> = ({
  children,
}) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // try to restore session on app start
  useEffect(() => {
    (async () => {
      const me = await fetchCurrentUser();
      if (me) setUser(me);
      setLoading(false);
    })();
  }, []);

  const login = async (username: string, password: string) => {
    try {
      const me = await loginRequest(username, password);
      setUser(me);
      return true;
    } catch (err) {
      console.log("Login error", err);
      Alert.alert("Login failed", "Invalid username or password.");
      return false;
    }
  };

  const logout = async () => {
    await clearTokens();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return ctx;
}
