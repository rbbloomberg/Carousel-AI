"use client";

import { useState } from "react";
import { CheckCircle2, Circle, ExternalLink } from "lucide-react";

const PLATFORMS = [
  {
    key: "meta",
    name: "Meta Ads",
    description: "Facebook & Instagram advertising",
    color: "bg-blue-500",
  },
  {
    key: "google",
    name: "Google Ads",
    description: "Search, Display, YouTube, Performance Max",
    color: "bg-red-500",
  },
  {
    key: "tiktok",
    name: "TikTok Ads",
    description: "TikTok video advertising",
    color: "bg-gray-900",
  },
  {
    key: "linkedin",
    name: "LinkedIn Ads",
    description: "Professional B2B advertising",
    color: "bg-blue-700",
  },
];

const TIERS = [
  {
    key: "starter",
    name: "Starter",
    price: "$499/mo",
    assets: 10,
    platforms: 2,
    campaigns: "5/month",
  },
  {
    key: "professional",
    name: "Professional",
    price: "$1,499/mo",
    assets: 50,
    platforms: 5,
    campaigns: "Unlimited",
  },
  {
    key: "enterprise",
    name: "Enterprise",
    price: "Custom",
    assets: "Unlimited",
    platforms: 5,
    campaigns: "Unlimited",
  },
];

export default function SettingsPage() {
  const [connected] = useState<Record<string, boolean>>({
    meta: false,
    google: false,
    tiktok: false,
    linkedin: false,
  });
  const [currentTier] = useState("starter");

  return (
    <div className="mx-auto max-w-4xl space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-500">
          Manage your account, platforms, and subscription
        </p>
      </div>

      {/* Platform Connections */}
      <div className="rounded-xl border bg-white p-6">
        <h2 className="mb-4 text-lg font-semibold text-gray-900">
          Platform Connections
        </h2>
        <p className="mb-4 text-sm text-gray-500">
          Connect your advertising platform accounts to enable campaign
          deployment.
        </p>
        <div className="grid gap-4 sm:grid-cols-2">
          {PLATFORMS.map((platform) => {
            const isConnected = connected[platform.key];
            return (
              <div
                key={platform.key}
                className="flex items-center justify-between rounded-lg border p-4"
              >
                <div className="flex items-center gap-3">
                  <div
                    className={`h-10 w-10 rounded-lg ${platform.color} flex items-center justify-center text-xs font-bold text-white`}
                  >
                    {platform.name[0]}
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      {platform.name}
                    </p>
                    <p className="text-xs text-gray-500">
                      {platform.description}
                    </p>
                  </div>
                </div>
                {isConnected ? (
                  <span className="flex items-center gap-1 text-xs font-medium text-green-600">
                    <CheckCircle2 className="h-4 w-4" />
                    Connected
                  </span>
                ) : (
                  <button className="rounded-lg bg-gray-100 px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-gray-200">
                    Connect
                  </button>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Subscription */}
      <div className="rounded-xl border bg-white p-6">
        <h2 className="mb-4 text-lg font-semibold text-gray-900">
          Subscription
        </h2>
        <div className="grid gap-4 sm:grid-cols-3">
          {TIERS.map((tier) => {
            const isCurrent = tier.key === currentTier;
            return (
              <div
                key={tier.key}
                className={`rounded-lg border-2 p-4 ${
                  isCurrent
                    ? "border-brand-600 bg-brand-50"
                    : "border-gray-200"
                }`}
              >
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold text-gray-900">{tier.name}</h3>
                  {isCurrent && (
                    <span className="rounded-full bg-brand-600 px-2 py-0.5 text-xs font-medium text-white">
                      Current
                    </span>
                  )}
                </div>
                <p className="mt-1 text-2xl font-bold text-gray-900">
                  {tier.price}
                </p>
                <ul className="mt-3 space-y-1.5 text-sm text-gray-600">
                  <li className="flex items-center gap-2">
                    <Circle className="h-3 w-3 text-gray-400" />
                    {typeof tier.assets === "number"
                      ? `${tier.assets} active assets`
                      : `${tier.assets} active assets`}
                  </li>
                  <li className="flex items-center gap-2">
                    <Circle className="h-3 w-3 text-gray-400" />
                    {tier.platforms} platforms
                  </li>
                  <li className="flex items-center gap-2">
                    <Circle className="h-3 w-3 text-gray-400" />
                    {tier.campaigns} campaigns
                  </li>
                </ul>
                {!isCurrent && (
                  <button className="mt-4 w-full rounded-lg bg-brand-600 py-2 text-xs font-medium text-white hover:bg-brand-700">
                    Upgrade
                  </button>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Brand Guidelines */}
      <div className="rounded-xl border bg-white p-6">
        <h2 className="mb-4 text-lg font-semibold text-gray-900">
          Brand Guidelines
        </h2>
        <p className="mb-4 text-sm text-gray-500">
          Upload your brand guidelines so AI agents can maintain brand
          consistency.
        </p>
        <div className="grid gap-4 sm:grid-cols-2">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Brand Colors (hex codes, comma-separated)
            </label>
            <input
              type="text"
              placeholder="#4263eb, #1c1c1c, #ffffff"
              className="mt-1 w-full rounded-lg border px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Primary Font
            </label>
            <input
              type="text"
              placeholder="Inter, Helvetica, Arial"
              className="mt-1 w-full rounded-lg border px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
            />
          </div>
          <div className="sm:col-span-2">
            <label className="block text-sm font-medium text-gray-700">
              Tone of Voice
            </label>
            <textarea
              rows={3}
              placeholder="Describe your brand voice (e.g., professional, friendly, bold...)"
              className="mt-1 w-full rounded-lg border px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
            />
          </div>
        </div>
        <button className="mt-4 rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700">
          Save Brand Guidelines
        </button>
      </div>
    </div>
  );
}
