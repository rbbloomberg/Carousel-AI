"use client";

import { CheckCircle2, Circle, Loader2 } from "lucide-react";

interface Stage {
  key: string;
  label: string;
  pod: string;
}

const STAGES: Stage[] = [
  { key: "market_research", label: "Market Research", pod: "Strategy" },
  { key: "brand_strategy", label: "Brand Strategy", pod: "Strategy" },
  { key: "copywriting", label: "Ad Copywriting", pod: "Creative" },
  { key: "visual_creative", label: "Visual Creative", pod: "Creative" },
];

interface PipelineTrackerProps {
  currentStage: string;
  completedStages: string[];
  status: string;
}

export function PipelineTracker({
  currentStage,
  completedStages,
  status,
}: PipelineTrackerProps) {
  function getStageState(key: string) {
    if (completedStages.includes(key)) return "completed";
    if (currentStage === key) return "active";
    return "pending";
  }

  const isFinished = status === "approval" || status === "live" || status === "completed";

  return (
    <div className="rounded-xl border bg-white p-6">
      <h2 className="mb-4 text-lg font-semibold text-gray-900">
        Pipeline Progress
      </h2>
      <div className="space-y-3">
        {STAGES.map((stage, i) => {
          const state = isFinished ? "completed" : getStageState(stage.key);
          return (
            <div key={stage.key} className="flex items-center gap-3">
              {/* Icon */}
              {state === "completed" ? (
                <CheckCircle2 className="h-5 w-5 text-green-500" />
              ) : state === "active" ? (
                <Loader2 className="h-5 w-5 animate-spin text-brand-600" />
              ) : (
                <Circle className="h-5 w-5 text-gray-300" />
              )}

              {/* Label */}
              <div className="flex-1">
                <p
                  className={`text-sm font-medium ${
                    state === "completed"
                      ? "text-green-700"
                      : state === "active"
                        ? "text-brand-700"
                        : "text-gray-400"
                  }`}
                >
                  {stage.label}
                </p>
                <p className="text-xs text-gray-400">{stage.pod} Pod</p>
              </div>

              {/* Status badge */}
              {state === "completed" && (
                <span className="rounded-full bg-green-50 px-2 py-0.5 text-xs text-green-600">
                  Done
                </span>
              )}
              {state === "active" && (
                <span className="rounded-full bg-brand-50 px-2 py-0.5 text-xs text-brand-600">
                  Running
                </span>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
