// authcontext.tsx
import React, { createContext, useContext, useEffect, useState } from "react";
import { loginRequest, clearTokens, fetchCurrentUser } from "@/lib/authClient";

// Define a type for the user data you expect from the API
type User = {
  id: number;
  username: string;
  email: string;
  role?: string | null;
  bio?: string | null;
  mobile_number?: string | null;
  profile_image?: string | null;
  institution_name?: string | null;
};


type AuthContextType = {
  user: User | null; // Store the user object instead of a boolean
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
   setUser: React.Dispatch<React.SetStateAction<User | null>>;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function bootstrap() {
      console.log("[Auth] Bootstrapping...");
      try {
        const userData = await fetchCurrentUser();
        console.log("[Auth] Bootstrap fetch user:", userData);
        if (userData) {
          setUser(userData);
        }
      } catch (e) {
        console.error("[Auth] Bootstrap failed:", e);
      } finally {
        setLoading(false);
      }
    }
    bootstrap();
  }, []);

  const login = async (username: string, password: string) => {
    setLoading(true);
    try {
      const userData = await loginRequest(username, password);
      console.log("[Auth] Login successful, setting user:", userData);
      setUser(userData);
    } catch (error) {
      console.error("[Auth] Login failed:", error);
      setUser(null); // Ensure user is null on failure
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    console.log("[Auth] Logging out.");
    await clearTokens();
    setUser(null);
  };

  return (
    <AuthContext.Provider
      // Value is now based on the presence of the user object
      value={{ user, loading, login, logout,setUser }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return ctx;
}
