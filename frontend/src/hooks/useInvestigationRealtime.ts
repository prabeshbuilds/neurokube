"use client";

import { useEffect, useState } from "react";
import { insforge } from "@/lib/insforge";
import { INVESTIGATION_STEPS, type ProgressEvent } from "@/types";

export function useInvestigationRealtime(investigationId: string | null, active: boolean) {
  const [completedSteps, setCompletedSteps] = useState<string[]>([]);
  const [currentLabel, setCurrentLabel] = useState<string | null>(null);

  useEffect(() => {
    if (!investigationId || !active) {
      return;
    }

    let cancelled = false;

    const handleProgress = (payload: ProgressEvent) => {
      if (cancelled || !payload.progress_step) {
        return;
      }

      setCurrentLabel(payload.progress_label ?? payload.progress_step);
      setCompletedSteps((prev) => {
        const stepIndex = INVESTIGATION_STEPS.findIndex(
          (item) => item.step === payload.progress_step,
        );
        if (stepIndex === -1) {
          return prev.includes(payload.progress_step!)
            ? prev
            : [...prev, payload.progress_step!];
        }

        const through = INVESTIGATION_STEPS.slice(0, stepIndex + 1).map(
          (item) => item.step,
        );
        return Array.from(new Set([...prev, ...through]));
      });
    };

    const subscribe = async () => {
      try {
        await insforge.realtime.connect();
        insforge.realtime.on("progress", handleProgress);
        const channel = `investigation:${investigationId}`;
        const response = await insforge.realtime.subscribe(channel);
        if (!response.ok && !cancelled) {
          console.error("Realtime subscribe failed:", response.error);
        }
      } catch (error) {
        console.error("Realtime connection failed:", error);
      }
    };

    subscribe();

    return () => {
      cancelled = true;
      insforge.realtime.off("progress", handleProgress);
      if (investigationId) {
        insforge.realtime.unsubscribe(`investigation:${investigationId}`);
      }
    };
  }, [investigationId, active]);

  const reset = () => {
    setCompletedSteps([]);
    setCurrentLabel(null);
  };

  return { completedSteps, currentLabel, reset };
}
