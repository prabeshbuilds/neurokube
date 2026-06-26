"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import { BrandLogo } from "@/components/BrandLogo";
import { useAuth } from "@/lib/auth-context";

export default function HomePage() {
  const router = useRouter();
  const { user, isLoading } = useAuth();

  useEffect(() => {
    if (isLoading) return;

    const destination = user ? "/dashboard" : "/login";
    router.replace(destination);
  }, [isLoading, user, router]);

  return (
    <main className="auth-shell flex flex-col items-center justify-center gap-4">
      <BrandLogo showTagline />

      <div
        className="h-6 w-6 animate-spin rounded-full border-2 border-cyan-500/30 border-t-cyan-400"
        aria-label="Loading"
      />

      <p className="text-sm text-slate-500">
        Redirecting...
      </p>
    </main>
  );
}