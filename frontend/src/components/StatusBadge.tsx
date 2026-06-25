"use client";

interface StatusBadgeProps {
  label: string;
  isLoading?: boolean;
}

export function StatusBadge({ label, isLoading }: StatusBadgeProps) {
  return (
    <div className="flex items-center gap-2 text-sm text-slate-600">
      <span
        className={`inline-block h-2 w-2 rounded-full ${
          isLoading ? "animate-pulse bg-amber-400" : "bg-emerald-500"
        }`}
      />
      <span>System Status: {label}</span>
    </div>
  );
}
