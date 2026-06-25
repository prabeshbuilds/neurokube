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
      className="btn-primary inline-flex items-center gap-2 px-6 py-3 disabled:transform-none"
    >
      <svg
        viewBox="0 0 24 24"
        fill="none"
        className="h-4 w-4"
        stroke="currentColor"
        strokeWidth="2.5"
        aria-hidden
      >
        <circle cx="11" cy="11" r="7" />
        <path d="M20 20l-3-3" strokeLinecap="round" />
      </svg>
      Investigate Cluster
    </button>
  );
}
