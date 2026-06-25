"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import { insforge } from "@/lib/insforge";

type AuthUser = {
  id: string;
  email: string;
  emailVerified?: boolean;
};

type AuthContextValue = {
  user: AuthUser | null;
  accessToken: string | null;
  isLoading: boolean;
  signIn: (email: string, password: string) => Promise<string | null>;
  signUp: (email: string, password: string, name: string) => Promise<boolean>;
  verifyEmail: (email: string, otp: string) => Promise<string | null>;
  signOut: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | null>(null);

const TOKEN_KEY = "insforge_access_token";

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const persistSession = useCallback((token: string | null, nextUser: AuthUser | null) => {
    setAccessToken(token);
    setUser(nextUser);
    if (token) {
      sessionStorage.setItem(TOKEN_KEY, token);
    } else {
      sessionStorage.removeItem(TOKEN_KEY);
    }
  }, []);

  useEffect(() => {
    const bootstrap = async () => {
      const storedToken = sessionStorage.getItem(TOKEN_KEY);
      if (storedToken) {
        setAccessToken(storedToken);
      }

      const { data, error } = await insforge.auth.getCurrentUser();
      if (data?.user) {
        setUser({
          id: data.user.id,
          email: data.user.email,
          emailVerified: data.user.emailVerified,
        });
      } else if (error && storedToken) {
        persistSession(null, null);
      }

      setIsLoading(false);
    };

    bootstrap();
  }, [persistSession]);

  const signIn = useCallback(
    async (email: string, password: string) => {
      const { data, error } = await insforge.auth.signInWithPassword({
        email,
        password,
      });

      if (error || !data?.accessToken) {
        return error?.message ?? "Sign in failed";
      }

      persistSession(data.accessToken, {
        id: data.user.id,
        email: data.user.email,
        emailVerified: data.user.emailVerified,
      });
      return null;
    },
    [persistSession],
  );

  const signUp = useCallback(async (email: string, password: string, name: string) => {
    const { data, error } = await insforge.auth.signUp({
      email,
      password,
      name,
    });

    if (error) {
      throw new Error(error.message ?? "Sign up failed");
    }

    return Boolean(data?.requireEmailVerification);
  }, []);

  const verifyEmail = useCallback(
    async (email: string, otp: string) => {
      const { data, error } = await insforge.auth.verifyEmail({ email, otp });

      if (error || !data?.accessToken) {
        return error?.message ?? "Verification failed";
      }

      persistSession(data.accessToken, {
        id: data.user.id,
        email: data.user.email,
        emailVerified: data.user.emailVerified,
      });
      return null;
    },
    [persistSession],
  );

  const signOut = useCallback(async () => {
    await insforge.auth.signOut();
    persistSession(null, null);
  }, [persistSession]);

  const value = useMemo(
    () => ({
      user,
      accessToken,
      isLoading,
      signIn,
      signUp,
      verifyEmail,
      signOut,
    }),
    [user, accessToken, isLoading, signIn, signUp, verifyEmail, signOut],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
