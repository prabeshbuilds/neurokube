import type { HealthResponse } from "@/types";
import { apiClient } from "./api";

export async function fetchHealth(): Promise<HealthResponse> {
  const response = await apiClient.get<HealthResponse>("/health");
  return response.data;
}
