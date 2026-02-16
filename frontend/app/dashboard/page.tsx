"use client";

import { useQuery } from "@tanstack/react-query";
import { listCampaigns, type Campaign } from "@/lib/api";
import { formatCurrency, formatNumber, statusColor } from "@/lib/utils";
import { StatsCard } from "@/components/dashboard/stats-card";
import { Megaphone, DollarSign, MousePointerClick, TrendingUp } from "lucide-react";
import Link from "next/link";

export default function DashboardPage() {
  const { data: campaigns = [], isLoading } = useQuery({
    queryKey: ["campaigns"],
    queryFn: listCampaigns,
  });

  const totalSpend = campaigns.reduce((s, c) => s + c.spend, 0);
  const totalImpressions = campaigns.reduce((s, c) => s + c.impressions, 0);
  const totalClicks = campaigns.reduce((s, c) => s + c.clicks, 0);
  const avgRoas =
    campaigns.length > 0
      ? campaigns.reduce((s, c) => s + c.roas, 0) / campaigns.length
      : 0;

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-500">Overview of your advertising campaigns</p>
      </div>

      {/* Stats grid */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatsCard
          title="Active Campaigns"
          value={campaigns.filter((c) => c.status === "live").length.toString()}
          icon={Megaphone}
        />
        <StatsCard
          title="Total Spend"
          value={formatCurrency(totalSpend)}
          icon={DollarSign}
        />
        <StatsCard
          title="Total Clicks"
          value={formatNumber(totalClicks)}
          icon={MousePointerClick}
        />
        <StatsCard
          title="Avg ROAS"
          value={avgRoas.toFixed(2) + "x"}
          icon={TrendingUp}
        />
      </div>

      {/* Recent campaigns */}
      <div className="rounded-xl border bg-white">
        <div className="flex items-center justify-between border-b px-6 py-4">
          <h2 className="font-semibold text-gray-900">Recent Campaigns</h2>
          <Link
            href="/briefs/new"
            className="rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700"
          >
            New Brief
          </Link>
        </div>

        {isLoading ? (
          <div className="p-6 text-center text-gray-400">Loading...</div>
        ) : campaigns.length === 0 ? (
          <div className="p-12 text-center">
            <p className="text-gray-500">No campaigns yet.</p>
            <p className="mt-1 text-sm text-gray-400">
              Submit a brief to get started.
            </p>
          </div>
        ) : (
          <table className="w-full">
            <thead>
              <tr className="border-b text-left text-sm text-gray-500">
                <th className="px-6 py-3 font-medium">Campaign</th>
                <th className="px-6 py-3 font-medium">Status</th>
                <th className="px-6 py-3 font-medium">Spend</th>
                <th className="px-6 py-3 font-medium">Impressions</th>
                <th className="px-6 py-3 font-medium">Clicks</th>
                <th className="px-6 py-3 font-medium">ROAS</th>
              </tr>
            </thead>
            <tbody>
              {campaigns.map((c) => (
                <tr key={c.id} className="border-b last:border-0 hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <Link
                      href={`/campaigns/${c.id}`}
                      className="font-medium text-gray-900 hover:text-brand-600"
                    >
                      {c.name}
                    </Link>
                  </td>
                  <td className="px-6 py-4">
                    <span
                      className={`inline-block rounded-full px-2.5 py-0.5 text-xs font-medium ${statusColor(c.status)}`}
                    >
                      {c.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {formatCurrency(c.spend)}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {formatNumber(c.impressions)}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {formatNumber(c.clicks)}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {c.roas.toFixed(2)}x
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
