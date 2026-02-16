"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { createBrief, submitBrief } from "@/lib/api";

const PLATFORMS = ["meta", "google", "tiktok", "linkedin"];
const OBJECTIVES = [
  "Brand Awareness",
  "Traffic / Website Visits",
  "Lead Generation",
  "Sales / Conversions",
  "App Installs",
  "Engagement",
];
const KPI_OPTIONS = ["ROAS", "CTR", "CPA", "CPM", "Conversions", "Impressions"];

export default function NewBriefPage() {
  const router = useRouter();
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [form, setForm] = useState({
    title: "",
    campaign_objective: "",
    budget_total: 1000,
    budget_duration_days: 30,
    platforms: ["meta"] as string[],
    kpis: [] as string[],
    brand_voice: "",
    target_audience: {
      demographics: {} as Record<string, string>,
      interests: [] as string[],
      behaviors: [] as string[],
    },
  });

  const [interestsInput, setInterestsInput] = useState("");

  function togglePlatform(p: string) {
    setForm((prev) => ({
      ...prev,
      platforms: prev.platforms.includes(p)
        ? prev.platforms.filter((x) => x !== p)
        : [...prev.platforms, p],
    }));
  }

  function toggleKpi(k: string) {
    setForm((prev) => ({
      ...prev,
      kpis: prev.kpis.includes(k)
        ? prev.kpis.filter((x) => x !== k)
        : [...prev.kpis, k],
    }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);

    try {
      // Parse comma-separated interests
      const interests = interestsInput
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean);

      const brief = await createBrief({
        ...form,
        target_audience: { ...form.target_audience, interests },
      });

      // Immediately submit to start the pipeline
      await submitBrief(brief.id);
      router.push("/campaigns");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="mx-auto max-w-2xl space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Create Campaign Brief</h1>
        <p className="text-gray-500">
          Fill out the details below and our AI agents will build your campaign.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6 rounded-xl border bg-white p-6">
        {/* Title */}
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Campaign Title
          </label>
          <input
            type="text"
            required
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
            className="mt-1 w-full rounded-lg border px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
            placeholder="e.g. Summer Product Launch"
          />
        </div>

        {/* Objective */}
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Campaign Objective
          </label>
          <select
            required
            value={form.campaign_objective}
            onChange={(e) =>
              setForm({ ...form, campaign_objective: e.target.value })
            }
            className="mt-1 w-full rounded-lg border px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
          >
            <option value="">Select an objective...</option>
            {OBJECTIVES.map((o) => (
              <option key={o} value={o}>
                {o}
              </option>
            ))}
          </select>
        </div>

        {/* Budget */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Total Budget ($)
            </label>
            <input
              type="number"
              min={100}
              required
              value={form.budget_total}
              onChange={(e) =>
                setForm({ ...form, budget_total: Number(e.target.value) })
              }
              className="mt-1 w-full rounded-lg border px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Duration (days)
            </label>
            <input
              type="number"
              min={1}
              required
              value={form.budget_duration_days}
              onChange={(e) =>
                setForm({
                  ...form,
                  budget_duration_days: Number(e.target.value),
                })
              }
              className="mt-1 w-full rounded-lg border px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
            />
          </div>
        </div>

        {/* Platforms */}
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Platforms
          </label>
          <div className="mt-2 flex flex-wrap gap-2">
            {PLATFORMS.map((p) => (
              <button
                key={p}
                type="button"
                onClick={() => togglePlatform(p)}
                className={`rounded-full px-4 py-1.5 text-sm font-medium transition-colors ${
                  form.platforms.includes(p)
                    ? "bg-brand-600 text-white"
                    : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                }`}
              >
                {p.charAt(0).toUpperCase() + p.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* KPIs */}
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Key Performance Indicators
          </label>
          <div className="mt-2 flex flex-wrap gap-2">
            {KPI_OPTIONS.map((k) => (
              <button
                key={k}
                type="button"
                onClick={() => toggleKpi(k)}
                className={`rounded-full px-4 py-1.5 text-sm font-medium transition-colors ${
                  form.kpis.includes(k)
                    ? "bg-brand-600 text-white"
                    : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                }`}
              >
                {k}
              </button>
            ))}
          </div>
        </div>

        {/* Target Audience Interests */}
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Target Audience Interests
          </label>
          <input
            type="text"
            value={interestsInput}
            onChange={(e) => setInterestsInput(e.target.value)}
            className="mt-1 w-full rounded-lg border px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
            placeholder="e.g. fitness, technology, fashion (comma-separated)"
          />
        </div>

        {/* Brand Voice */}
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Brand Voice / Tone
          </label>
          <textarea
            value={form.brand_voice}
            onChange={(e) => setForm({ ...form, brand_voice: e.target.value })}
            rows={3}
            className="mt-1 w-full rounded-lg border px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
            placeholder="Describe your brand's tone of voice, personality, and communication style..."
          />
        </div>

        {/* Error */}
        {error && (
          <div className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-600">
            {error}
          </div>
        )}

        {/* Submit */}
        <button
          type="submit"
          disabled={submitting}
          className="w-full rounded-lg bg-brand-600 py-3 text-sm font-medium text-white hover:bg-brand-700 disabled:opacity-50"
        >
          {submitting ? "Submitting to AI Agents..." : "Submit Brief & Launch Pipeline"}
        </button>
      </form>
    </div>
  );
}
