import { APP_NAME, APP_TAGLINE } from "@/lib/brand";

interface BrandLogoProps {
  compact?: boolean;
  showTagline?: boolean;
}

export function BrandLogo({ compact = false, showTagline = false }: BrandLogoProps) {
  const iconSize = compact ? "h-9 w-9" : "h-11 w-11";
  const titleClass = compact ? "text-lg" : "text-xl";

  return (
    <div className="flex items-center gap-3">
      <div
        className={`${iconSize} flex shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-cyan-400 via-cyan-500 to-teal-600 shadow-lg shadow-cyan-500/25 ring-1 ring-cyan-400/30`}
        aria-hidden
      >
        <svg
          viewBox="0 0 24 24"
          fill="none"
          className={compact ? "h-5 w-5 text-slate-950" : "h-6 w-6 text-slate-950"}
          stroke="currentColor"
          strokeWidth="2"
        >
          <circle cx="12" cy="12" r="3" />
          <path d="M12 2v4M12 18v4M2 12h4M18 12h4" strokeLinecap="round" />
          <circle cx="12" cy="12" r="8" strokeOpacity="0.5" />
        </svg>
      </div>
      <div>
        <p className={`${titleClass} font-bold tracking-tight text-white`}>
          {APP_NAME}
        </p>
        {showTagline ? (
          <p className="text-xs font-medium text-cyan-300/80">{APP_TAGLINE}</p>
        ) : null}
      </div>
    </div>
  );
}
