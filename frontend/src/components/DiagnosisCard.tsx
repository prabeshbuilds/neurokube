import type { Diagnosis } from "@/types";

interface DiagnosisCardProps {
  diagnosis: Diagnosis;
}

export function DiagnosisCard({ diagnosis }: DiagnosisCardProps) {
  return (
    <section className="panel overflow-hidden p-0">
      <div className="border-b border-cyan-500/20 bg-gradient-to-r from-cyan-500/10 to-teal-500/5 px-6 py-4">
        <p className="panel-header">Analysis Result</p>
        <h2 className="mt-1 text-lg font-semibold text-white">Diagnosis</h2>
      </div>

      <div className="space-y-5 p-6 text-sm">
        <div className="rounded-lg border-l-2 border-cyan-400 bg-slate-900/50 pl-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-cyan-400/90">
            Root Cause
          </p>
          <p className="mt-1.5 text-base font-medium text-white">{diagnosis.root_cause}</p>
        </div>

        <div>
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
            Explanation
          </p>
          <p className="mt-1.5 leading-relaxed text-slate-300">{diagnosis.explanation}</p>
        </div>

        <div>
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
            Suggested Fix
          </p>
          <p className="mt-1.5 leading-relaxed text-slate-300">{diagnosis.fix}</p>
        </div>

        <div>
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
            Command
          </p>
          <pre className="mt-2 overflow-x-auto rounded-lg border border-slate-700/80 bg-slate-950 p-4 font-mono text-xs leading-relaxed text-cyan-100">
            {diagnosis.kubectl_command}
          </pre>
        </div>

        <div className="flex flex-col gap-4 border-t border-slate-800 pt-5 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
              Confidence
            </p>
            <p className="mt-1 bg-gradient-to-r from-cyan-400 to-teal-400 bg-clip-text text-3xl font-bold text-transparent">
              {diagnosis.confidence}%
            </p>
          </div>
          {diagnosis.confidence_reasoning ? (
            <p className="max-w-md text-xs leading-relaxed text-slate-500 sm:text-right">
              {diagnosis.confidence_reasoning}
            </p>
          ) : null}
        </div>
      </div>
    </section>
  );
}
