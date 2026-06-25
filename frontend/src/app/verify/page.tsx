"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { FormEvent, Suspense, useState } from "react";
import { BrandLogo } from "@/components/BrandLogo";
import { useAuth } from "@/lib/auth-context";

function VerifyForm() {
  const searchParams = useSearchParams();
  const email = searchParams.get("email") ?? "";
  const { verifyEmail } = useAuth();
  const router = useRouter();
  const [otp, setOtp] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setSubmitting(true);
    setError(null);

    const message = await verifyEmail(email, otp);
    if (message) {
      setError(message);
      setSubmitting(false);
      return;
    }

    router.push("/dashboard");
  };

  return (
    <div className="auth-shell">
      <main className="auth-card">
        <div className="mb-6 flex justify-center">
          <BrandLogo compact />
        </div>
        <h1 className="text-center text-xl font-semibold text-white">Verify Email</h1>
        <p className="mt-2 text-center text-sm text-slate-400">
          Enter the 6-digit code sent to{" "}
          <span className="text-cyan-300">{email || "your email"}</span>.
        </p>

        <form onSubmit={handleSubmit} className="mt-8 space-y-4">
          <input
            type="text"
            placeholder="123456"
            required
            pattern="[0-9]{6}"
            value={otp}
            onChange={(event) => setOtp(event.target.value)}
            className="input-field text-center text-lg tracking-[0.4em]"
          />
          {error ? (
            <p className="rounded-lg border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm text-red-300">
              {error}
            </p>
          ) : null}
          <button
            type="submit"
            disabled={submitting || !email}
            className="btn-primary w-full py-3"
          >
            {submitting ? "Verifying..." : "Verify & Continue"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-slate-500">
          <Link href="/login" className="text-cyan-400/80 hover:text-cyan-300">
            Back to sign in
          </Link>
        </p>
      </main>
    </div>
  );
}

export default function VerifyPage() {
  return (
    <Suspense
      fallback={
        <div className="auth-shell text-slate-400">
          <div className="h-8 w-8 animate-spin rounded-full border-2 border-cyan-500/30 border-t-cyan-400" />
        </div>
      }
    >
      <VerifyForm />
    </Suspense>
  );
}
