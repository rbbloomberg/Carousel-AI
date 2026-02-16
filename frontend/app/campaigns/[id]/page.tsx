"use client";

import { useQuery } from "@tanstack/react-query";
import { useParams } from "next/navigation";
import { getCampaign, approveCampaign } from "@/lib/api";
import { formatCurrency, formatNumber, statusColor } from "@/lib/utils";
import { StatsCard } from "@/components/dashboard/stats-card";
import { PipelineTracker } from "@/components/dashboard/pipeline-tracker";
import { StrategyOutput } from "@/components/dashboard/strategy-output";
import { CreativeOutput } from "@/components/dashboard/creative-output";
import {
  Eye,
  MousePointerClick,
  ShoppingCart,
  TrendingUp,
} from "lucide-react";
import { useState } from "react";

export default function CampaignDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [approving, setApproving] = useState(false);
  const [activeTab, setActiveTab] = useState<"strategy" | "creative" | "platform">("strategy");

  const {
    data: campaign,
    isLoading,
    refetch,
  } = useQuery({
    queryKey: ["campaign", id],
    queryFn: () => getCampaign(id),
    refetchInterval: (query) => {
      // Poll every 3s while pipeline is running
      const status = query.state.data?.status;
      return status === "strategy" || status === "creative" ? 3000 : false;
    },
  });

  async function handleApprove() {
    setApproving(true);
    try {
      await approveCampaign(id);
      refetch();
    } finally {
      setApproving(false);
    }
  }

  if (isLoading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-brand-600 border-t-transparent" />
      </div>
    );
  }

  if (!campaign) {
    return (
      <div className="p-12 text-center text-gray-500">Campaign not found</div>
    );
  }

  const strategy = campaign.strategy_output || {};
  const creative = campaign.creative_output || {};

  // Determine pipeline state for tracker
  const completedStages: string[] = [];
  if (strategy.market_research) completedStages.push("market_research");
  if (strategy.brand_strategy) completedStages.push("brand_strategy");
  if (creative.ad_copy) completedStages.push("copywriting");
  if (creative.visual_creative) completedStages.push("visual_creative");

  let currentStage = "";
  if (campaign.status === "strategy") currentStage = completedStages.length === 0 ? "market_research" : "brand_strategy";
  if (campaign.status === "creative") currentStage = "copywriting";

  const tabs = [
    { key: "strategy" as const, label: "Strategy & Insights", count: Object.keys(strategy).length },
    { key: "creative" as const, label: "Creative Output", count: Object.keys(creative).length },
    { key: "platform" as const, label: "Platform Data", count: Object.keys(campaign.platform_data || {}).length },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{campaign.name}</h1>
          <div className="mt-2 flex items-center gap-3">
            <span
              className={`rounded-full px-3 py-1 text-xs font-medium ${statusColor(campaign.status)}`}
            >
              {campaign.status}
            </span>
            <span className="text-sm text-gray-500">
              Created {new Date(campaign.created_at).toLocaleDateString()}
            </span>
            {campaign.launched_at && (
              <span className="text-sm text-gray-500">
                Launched{" "}
                {new Date(campaign.launched_at).toLocaleDateString()}
              </span>
            )}
          </div>
        </div>

        {campaign.status === "approval" && (
          <button
            onClick={handleApprove}
            disabled={approving}
            className="rounded-lg bg-green-600 px-6 py-2.5 text-sm font-medium text-white hover:bg-green-700 disabled:opacity-50"
          >
            {approving ? "Approving..." : "Approve & Launch on Meta"}
          </button>
        )}
      </div>

      {/* Metrics + Pipeline tracker */}
      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <StatsCard
              title="Impressions"
              value={formatNumber(campaign.impressions)}
              icon={Eye}
            />
            <StatsCard
              title="Clicks"
              value={formatNumber(campaign.clicks)}
              icon={MousePointerClick}
            />
            <StatsCard
              title="Conversions"
              value={formatNumber(campaign.conversions)}
              icon={ShoppingCart}
            />
            <StatsCard
              title="ROAS"
              value={campaign.roas.toFixed(2) + "x"}
              icon={TrendingUp}
            />
          </div>
        </div>
        <PipelineTracker
          currentStage={currentStage}
          completedStages={completedStages}
          status={campaign.status}
        />
      </div>

      {/* Tabs */}
      <div className="border-b">
        <div className="flex gap-6">
          {tabs.map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`border-b-2 pb-3 text-sm font-medium transition-colors ${
                activeTab === tab.key
                  ? "border-brand-600 text-brand-600"
                  : "border-transparent text-gray-500 hover:text-gray-700"
              }`}
            >
              {tab.label}
              {tab.count > 0 && (
                <span className="ml-2 rounded-full bg-gray-100 px-2 py-0.5 text-xs">
                  {tab.count}
                </span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Tab content */}
      {activeTab === "strategy" && Object.keys(strategy).length > 0 && (
        <StrategyOutput
          marketResearch={strategy.market_research || {}}
          brandStrategy={strategy.brand_strategy || {}}
        />
      )}

      {activeTab === "creative" && Object.keys(creative).length > 0 && (
        <CreativeOutput
          adCopy={creative.ad_copy || {}}
          visualCreative={creative.visual_creative || {}}
        />
      )}

      {activeTab === "platform" && (
        <div className="rounded-xl border bg-white p-6">
          <h3 className="mb-4 font-semibold text-gray-900">Platform Data</h3>
          {Object.keys(campaign.platform_data || {}).length > 0 ? (
            <pre className="max-h-96 overflow-auto rounded-lg bg-gray-50 p-4 text-xs text-gray-700">
              {JSON.stringify(campaign.platform_data, null, 2)}
            </pre>
          ) : (
            <p className="text-sm text-gray-500">
              No platform data yet. Approve the campaign to launch on Meta Ads.
            </p>
          )}
        </div>
      )}

      {/* Empty state for in-progress campaigns */}
      {(campaign.status === "strategy" || campaign.status === "creative") && (
        <div className="rounded-xl border border-brand-200 bg-brand-50 p-6 text-center">
          <div className="mx-auto h-8 w-8 animate-spin rounded-full border-4 border-brand-600 border-t-transparent" />
          <p className="mt-3 font-medium text-brand-900">
            AI agents are working on your campaign...
          </p>
          <p className="mt-1 text-sm text-brand-600">
            This page will auto-refresh as agents complete their tasks.
          </p>
        </div>
      )}
    </div>
  );
}
