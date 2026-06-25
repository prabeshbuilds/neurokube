import { insforge } from "@/lib/insforge";
import type { InvestigationRecord } from "@/types";

export async function createInvestigation(userId: string): Promise<InvestigationRecord> {
  const { data, error } = await insforge.database
    .from("investigations")
    .insert([
      {
        user_id: userId,
        status: "pending",
        progress_step: "starting",
        progress_label: "Starting investigation",
      },
    ])
    .select();

  if (error || !data?.[0]) {
    throw new Error(error?.message ?? "Failed to create investigation record");
  }

  return data[0] as InvestigationRecord;
}

export async function fetchInvestigationHistory(
  userId: string,
): Promise<InvestigationRecord[]> {
  const { data, error } = await insforge.database
    .from("investigations")
    .select("id,user_id,status,root_cause,namespace,confidence,cluster_context,created_at")
    .eq("user_id", userId)
    .eq("status", "completed")
    .order("created_at", { ascending: false })
    .limit(10);

  if (error) {
    throw new Error(error.message ?? "Failed to load history");
  }

  return (data ?? []) as InvestigationRecord[];
}
