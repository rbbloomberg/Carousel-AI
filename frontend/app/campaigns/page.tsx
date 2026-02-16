"use client";

import { useQuery } from "@tanstack/react-query";
import { listCampaigns } from "@/lib/api";
import { formatCurrency, statusColor } from "@/lib/utils";
import Link from "next/link";

export default function CampaignsPage() {
  const { data: campaigns = [], isLoading } = useQuery({
    queryKey: ["campaigns"],
    queryFn: listCampaigns,
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Campaigns</h1>
          <p className="text-gray-500">All your advertising campaigns</p>
        </div>
        <Link
          href="/briefs/new"
          className="rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700"
        >
          New Brief
        </Link>
      </div>

      {isLoading ? (
        <div className="p-12 text-center text-gray-400">Loading campaigns...</div>
      ) : campaigns.length === 0 ? (
        <div className="rounded-xl border bg-white p-12 text-center">
          <p className="text-gray-500">No campaigns yet.</p>
          <Link
            href="/briefs/new"
            className="mt-4 inline-block rounded-lg bg-brand-600 px-6 py-2 text-sm font-medium text-white hover:bg-brand-700"
          >
            Create Your First Brief
          </Link>
        </div>
      ) : (
        <div className="grid gap-4">
          {campaigns.map((c) => (
            <Link
              key={c.id}
              href={`/campaigns/${c.id}`}
              className="flex items-center justify-between rounded-xl border bg-white p-6 transition-shadow hover:shadow-md"
            >
              <div>
                <h3 className="font-semibold text-gray-900">{c.name}</h3>
                <p className="mt-1 text-sm text-gray-500">
                  Created {new Date(c.created_at).toLocaleDateString()}
                </p>
              </div>
              <div className="flex items-center gap-6">
                <div className="text-right">
                  <p className="text-sm text-gray-500">Spend</p>
                  <p className="font-medium">{formatCurrency(c.spend)}</p>
                </div>
                <span
                  className={`rounded-full px-3 py-1 text-xs font-medium ${statusColor(c.status)}`}
                >
                  {c.status}
                </span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
