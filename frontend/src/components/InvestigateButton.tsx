"use client";

interface InvestigateButtonProps {
  onClick: () => void;
  disabled?: boolean;
}

export function InvestigateButton({ onClick, disabled }: InvestigateButtonProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className="rounded-lg bg-blue-600 px-6 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
    >
      Investigate Cluster
    </button>
  );
}
