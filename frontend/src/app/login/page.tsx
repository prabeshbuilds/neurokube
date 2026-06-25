"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { BrandLogo } from "@/components/BrandLogo";
import { useAuth } from "@/lib/auth-context";
import { APP_TAGLINE } from "@/lib/brand";

export default function LoginPage() {
  const { signIn, signUp, user, isLoading } = useAuth();
  const router = useRouter();
  const [mode, setMode] = useState<"signin" | "signup">("signin");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  if (!isLoading && user) {
    router.replace("/dashboard");
  }

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setSubmitting(true);
    setError(null);

    try {
      if (mode === "signin") {
        const message = await signIn(email, password);
        if (message) {
          setError(message);
        } else {
          router.push("/dashboard");
        }
      } else {
        const needsVerification = await signUp(email, password, name || email);
        if (needsVerification) {
          router.push(`/verify?email=${encodeURIComponent(email)}`);
        } else {
          const message = await signIn(email, password);
          if (message) {
            setError(message);
          } else {
            router.push("/dashboard");
          }
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Authentication failed");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="auth-shell">
      <main className="auth-card">
        <div className="mb-8 flex justify-center">
          <BrandLogo showTagline />
        </div>
        <p className="text-center text-sm text-slate-400">{APP_TAGLINE}</p>

        <div className="mt-8 flex gap-2 rounded-xl bg-slate-900/80 p-1 ring-1 ring-slate-700/50">
          <button
            type="button"
            onClick={() => setMode("signin")}
            className={`flex-1 rounded-lg px-3 py-2.5 text-sm font-medium transition ${
              mode === "signin"
                ? "bg-cyan-500/20 text-cyan-300 ring-1 ring-cyan-500/30"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Sign In
          </button>
          <button
            type="button"
            onClick={() => setMode("signup")}
            className={`flex-1 rounded-lg px-3 py-2.5 text-sm font-medium transition ${
              mode === "signup"
                ? "bg-cyan-500/20 text-cyan-300 ring-1 ring-cyan-500/30"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Sign Up
          </button>
        </div>

        <form onSubmit={handleSubmit} className="mt-6 space-y-4">
          {mode === "signup" ? (
            <input
              type="text"
              placeholder="Name"
              value={name}
              onChange={(event) => setName(event.target.value)}
              className="input-field"
            />
          ) : null}
          <input
            type="email"
            placeholder="Email"
            required
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            className="input-field"
          />
          <input
            type="password"
            placeholder="Password"
            required
            minLength={6}
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            className="input-field"
          />

          {error ? (
            <p className="rounded-lg border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm text-red-300">
              {error}
            </p>
          ) : null}

          <button type="submit" disabled={submitting} className="btn-primary w-full py-3">
            {submitting ? "Please wait..." : mode === "signin" ? "Sign In" : "Create Account"}
          </button>
        </form>

        <p className="mt-6 text-center text-xs text-slate-500">
          Protected by{" "}
          <Link href="https://insforge.dev" className="text-cyan-400/80 hover:text-cyan-300">
            InsForge
          </Link>
        </p>
      </main>
    </div>
  );
}
