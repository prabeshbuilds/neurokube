interface ErrorAlertProps {
  message: string;
}

export function ErrorAlert({ message }: ErrorAlertProps) {
  return (
    <div className="rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-3">
      <p className="text-sm font-semibold text-red-300">Something went wrong</p>
      <pre className="mt-2 whitespace-pre-wrap text-sm leading-relaxed text-red-200/90">
        {message}
      </pre>
    </div>
  );
}
