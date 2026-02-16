"use client";

import { useQuery } from "@tanstack/react-query";
import { useParams } from "next/navigation";
import { getCampaign, approveCampaign } from "@/lib/api";
import { formatCurrency, formatNumber, statusColor } from "@/lib/utils";
import { StatsCard } from "@/components/dashboard/stats-card";
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

  const {
    data: campaign,
    isLoading,
    refetch,
  } = useQuery({
    queryKey: ["campaign", id],
    queryFn: () => getCampaign(id),
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
    return <div className="p-12 text-center text-gray-400">Loading...</div>;
  }

  if (!campaign) {
    return <div className="p-12 text-center text-gray-500">Campaign not found</div>;
  }

  return (
    <div className="space-y-8">
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
          </div>
        </div>

        {campaign.status === "approval" && (
          <button
            onClick={handleApprove}
            disabled={approving}
            className="rounded-lg bg-green-600 px-6 py-2 text-sm font-medium text-white hover:bg-green-700 disabled:opacity-50"
          >
            {approving ? "Approving..." : "Approve & Launch"}
          </button>
        )}
      </div>

      {/* Metrics */}
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

      {/* Agent outputs */}
      {campaign.strategy_output &&
        Object.keys(campaign.strategy_output).length > 0 && (
          <div className="rounded-xl border bg-white p-6">
            <h2 className="mb-4 text-lg font-semibold text-gray-900">
              Strategy & Insights
            </h2>
            <pre className="max-h-96 overflow-auto rounded-lg bg-gray-50 p-4 text-xs text-gray-700">
              {JSON.stringify(campaign.strategy_output, null, 2)}
            </pre>
          </div>
        )}

      {campaign.creative_output &&
        Object.keys(campaign.creative_output).length > 0 && (
          <div className="rounded-xl border bg-white p-6">
            <h2 className="mb-4 text-lg font-semibold text-gray-900">
              Creative Output
            </h2>
            <pre className="max-h-96 overflow-auto rounded-lg bg-gray-50 p-4 text-xs text-gray-700">
              {JSON.stringify(campaign.creative_output, null, 2)}
            </pre>
          </div>
        )}

      {/* Platform data */}
      {campaign.platform_data &&
        Object.keys(campaign.platform_data).length > 0 && (
          <div className="rounded-xl border bg-white p-6">
            <h2 className="mb-4 text-lg font-semibold text-gray-900">
              Platform Data
            </h2>
            <pre className="max-h-96 overflow-auto rounded-lg bg-gray-50 p-4 text-xs text-gray-700">
              {JSON.stringify(campaign.platform_data, null, 2)}
            </pre>
          </div>
        )}
    </div>
  );
}
