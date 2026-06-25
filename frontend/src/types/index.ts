export interface HealthResponse {
  status: string;
  service: string;
}

export interface ClusterInfo {
  name: string;
  cluster: string;
  server: string;
  namespace: string;
  is_current: boolean;
}

export interface ClusterListResponse {
  status: string;
  clusters: ClusterInfo[];
  error?: string | null;
}

export interface Diagnosis {
  root_cause: string;
  explanation: string;
  fix: string;
  kubectl_command: string;
  prevention_recommendation?: string;
  confidence: number;
  confidence_reasoning?: string;
}

export interface InvestigateResponse {
  status: string;
  diagnosis: Diagnosis;
  cluster_healthy: boolean;
  cluster_context: string;
}

export interface InvestigationRecord {
  id: string;
  user_id: string;
  status: string;
  progress_step?: string | null;
  progress_label?: string | null;
  root_cause?: string | null;
  namespace?: string | null;
  confidence?: number | null;
  cluster_context?: string | null;
  created_at: string;
}

export interface ProgressEvent {
  id?: string;
  status?: string;
  progress_step?: string;
  progress_label?: string;
}

export const INVESTIGATION_STEPS = [
  { step: "checking_pods", label: "Checking Pods" },
  { step: "reading_logs", label: "Reading Logs" },
  { step: "analyzing_events", label: "Analyzing Events" },
  { step: "inspecting_deployments", label: "Inspecting Deployments" },
  { step: "checking_networking", label: "Checking Networking" },
  { step: "ai_reasoning", label: "AI Reasoning" },
  { step: "root_cause_found", label: "Root Cause Found" },
] as const;
