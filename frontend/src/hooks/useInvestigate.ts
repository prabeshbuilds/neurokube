"use client";

import { useState } from "react";

export function useInvestigate() {
  const [isInvestigating, setIsInvestigating] = useState(false);

  const investigate = () => {
    setIsInvestigating(true);
    // Placeholder for future cluster investigation flow.
    setTimeout(() => setIsInvestigating(false), 500);
  };

  return { investigate, isInvestigating };
}
