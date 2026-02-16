/**
 * API client for the AdForge backend.
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function apiFetch<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token =
    typeof window !== "undefined" ? localStorage.getItem("token") : null;

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `API error ${res.status}`);
  }

  return res.json();
}

// ---- Auth ----

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export async function register(data: {
  email: string;
  password: string;
  full_name: string;
  company_name: string;
  industry?: string;
}): Promise<TokenResponse> {
  return apiFetch("/api/v1/auth/register", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function login(
  email: string,
  password: string
): Promise<TokenResponse> {
  return apiFetch("/api/v1/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

// ---- Briefs ----

export interface Brief {
  id: string;
  client_id: string;
  title: string;
  campaign_objective: string;
  target_audience: Record<string, unknown>;
  budget_total: number;
  budget_duration_days: number;
  platforms: string[];
  kpis: string[];
  brand_voice: string | null;
  status: string;
  created_at: string;
  submitted_at: string | null;
}

export async function createBrief(
  data: Omit<Brief, "id" | "client_id" | "status" | "created_at" | "submitted_at">
): Promise<Brief> {
  return apiFetch("/api/v1/briefs", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function listBriefs(): Promise<Brief[]> {
  return apiFetch("/api/v1/briefs");
}

export async function submitBrief(briefId: string): Promise<Brief> {
  return apiFetch(`/api/v1/briefs/${briefId}/submit`, { method: "POST" });
}

// ---- Campaigns ----

export interface Campaign {
  id: string;
  brief_id: string;
  client_id: string;
  name: string;
  status: string;
  platform_data: Record<string, unknown>;
  impressions: number;
  clicks: number;
  conversions: number;
  spend: number;
  roas: number;
  strategy_output: Record<string, unknown>;
  creative_output: Record<string, unknown>;
  created_at: string;
  launched_at: string | null;
}

export async function listCampaigns(): Promise<Campaign[]> {
  return apiFetch("/api/v1/campaigns");
}

export async function getCampaign(id: string): Promise<Campaign> {
  return apiFetch(`/api/v1/campaigns/${id}`);
}

export async function approveCampaign(id: string): Promise<Campaign> {
  return apiFetch(`/api/v1/campaigns/${id}/approve`, { method: "POST" });
}

// ---- SSE ----

export function subscribeToCampaignEvents(
  campaignId: string,
  onEvent: (data: Record<string, unknown>) => void
): EventSource {
  const token = localStorage.getItem("token");
  const es = new EventSource(
    `${API_BASE}/api/v1/agents/stream/${campaignId}?token=${token}`
  );
  es.addEventListener("agent_update", (e) => {
    onEvent(JSON.parse(e.data));
  });
  return es;
}
