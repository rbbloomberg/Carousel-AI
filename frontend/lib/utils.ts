import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(value: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(value);
}

export function formatNumber(value: number): string {
  return new Intl.NumberFormat("en-US").format(value);
}

export function statusColor(status: string): string {
  const colors: Record<string, string> = {
    draft: "bg-gray-100 text-gray-700",
    submitted: "bg-blue-100 text-blue-700",
    in_progress: "bg-yellow-100 text-yellow-700",
    planning: "bg-yellow-100 text-yellow-700",
    strategy: "bg-purple-100 text-purple-700",
    creative: "bg-indigo-100 text-indigo-700",
    approval: "bg-orange-100 text-orange-700",
    live: "bg-green-100 text-green-700",
    paused: "bg-red-100 text-red-700",
    completed: "bg-green-100 text-green-700",
  };
  return colors[status] || "bg-gray-100 text-gray-700";
}
