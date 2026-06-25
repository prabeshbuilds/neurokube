export interface HealthResponse {
  status: string;
  service: string;
}

export interface Diagnosis {
  root_cause?: string;
  suggested_fix?: string;
}
