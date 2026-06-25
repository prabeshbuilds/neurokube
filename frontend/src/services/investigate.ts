import { apiClient } from "./api";
import type { InvestigateResponse } from "@/types";

export async function runInvestigation(
  investigationId: string,
  clusterContext: string,
  accessToken: string,
): Promise<InvestigateResponse> {
  const response = await apiClient.post<InvestigateResponse>(
    "/investigate",
    {
      investigation_id: investigationId,
      cluster_context: clusterContext,
    },
    {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
      timeout: 180_000,
    },
  );
  return response.data;
}
