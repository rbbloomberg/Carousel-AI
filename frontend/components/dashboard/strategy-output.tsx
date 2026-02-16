"use client";

interface StrategyOutputProps {
  marketResearch: {
    market_analysis?: {
      market_size?: string;
      growth_rate?: string;
      key_trends?: string[];
      competitor_landscape?: { name: string; strength: string; weakness: string }[];
    };
    opportunities?: string[];
    recommendations?: string;
  };
  brandStrategy: {
    positioning?: string;
    messaging_framework?: {
      primary_message?: string;
      supporting_messages?: string[];
    };
    tone_of_voice?: string;
    target_personas?: {
      name: string;
      pain_points?: string[];
      motivations?: string[];
    }[];
    creative_direction?: {
      visual_style?: string;
      content_themes?: string[];
    };
  };
}

export function StrategyOutput({
  marketResearch,
  brandStrategy,
}: StrategyOutputProps) {
  return (
    <div className="space-y-6">
      {/* Market Research */}
      {marketResearch?.market_analysis && (
        <div className="rounded-xl border bg-white p-6">
          <h3 className="mb-4 font-semibold text-gray-900">Market Analysis</h3>

          <div className="grid gap-4 sm:grid-cols-2">
            {marketResearch.market_analysis.market_size && (
              <div className="rounded-lg bg-gray-50 p-3">
                <p className="text-xs font-medium text-gray-500">Market Size</p>
                <p className="mt-1 text-sm font-medium text-gray-900">
                  {marketResearch.market_analysis.market_size}
                </p>
              </div>
            )}
            {marketResearch.market_analysis.growth_rate && (
              <div className="rounded-lg bg-gray-50 p-3">
                <p className="text-xs font-medium text-gray-500">Growth Rate</p>
                <p className="mt-1 text-sm font-medium text-gray-900">
                  {marketResearch.market_analysis.growth_rate}
                </p>
              </div>
            )}
          </div>

          {marketResearch.market_analysis.key_trends &&
            marketResearch.market_analysis.key_trends.length > 0 && (
              <div className="mt-4">
                <p className="text-xs font-medium text-gray-500">Key Trends</p>
                <ul className="mt-2 space-y-1">
                  {marketResearch.market_analysis.key_trends.map((t, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-gray-700">
                      <span className="mt-1.5 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-brand-500" />
                      {t}
                    </li>
                  ))}
                </ul>
              </div>
            )}

          {marketResearch.market_analysis.competitor_landscape &&
            marketResearch.market_analysis.competitor_landscape.length > 0 && (
              <div className="mt-4">
                <p className="text-xs font-medium text-gray-500">
                  Competitor Landscape
                </p>
                <div className="mt-2 space-y-2">
                  {marketResearch.market_analysis.competitor_landscape.map(
                    (c, i) => (
                      <div
                        key={i}
                        className="flex items-center justify-between rounded-lg bg-gray-50 px-4 py-2 text-sm"
                      >
                        <span className="font-medium text-gray-900">
                          {c.name}
                        </span>
                        <div className="flex gap-4 text-xs">
                          <span className="text-green-600">+ {c.strength}</span>
                          <span className="text-red-500">- {c.weakness}</span>
                        </div>
                      </div>
                    )
                  )}
                </div>
              </div>
            )}
        </div>
      )}

      {/* Opportunities */}
      {marketResearch?.opportunities && marketResearch.opportunities.length > 0 && (
        <div className="rounded-xl border bg-white p-6">
          <h3 className="mb-3 font-semibold text-gray-900">Opportunities</h3>
          <ul className="space-y-2">
            {marketResearch.opportunities.map((o, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-gray-700">
                <span className="mt-1.5 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-green-500" />
                {o}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Brand Strategy */}
      {brandStrategy?.positioning && (
        <div className="rounded-xl border bg-white p-6">
          <h3 className="mb-4 font-semibold text-gray-900">Brand Strategy</h3>

          <div className="rounded-lg bg-brand-50 p-4">
            <p className="text-xs font-medium text-brand-600">Positioning</p>
            <p className="mt-1 text-sm font-medium text-brand-900">
              {brandStrategy.positioning}
            </p>
          </div>

          {brandStrategy.messaging_framework && (
            <div className="mt-4">
              <p className="text-xs font-medium text-gray-500">
                Messaging Framework
              </p>
              {brandStrategy.messaging_framework.primary_message && (
                <p className="mt-2 text-sm font-medium text-gray-900">
                  &ldquo;{brandStrategy.messaging_framework.primary_message}&rdquo;
                </p>
              )}
              {brandStrategy.messaging_framework.supporting_messages && (
                <ul className="mt-2 space-y-1">
                  {brandStrategy.messaging_framework.supporting_messages.map(
                    (m, i) => (
                      <li key={i} className="text-sm text-gray-600">
                        - {m}
                      </li>
                    )
                  )}
                </ul>
              )}
            </div>
          )}

          {brandStrategy.tone_of_voice && (
            <div className="mt-4">
              <p className="text-xs font-medium text-gray-500">Tone of Voice</p>
              <p className="mt-1 text-sm text-gray-700">
                {brandStrategy.tone_of_voice}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Recommendations */}
      {marketResearch?.recommendations && (
        <div className="rounded-xl border bg-white p-6">
          <h3 className="mb-3 font-semibold text-gray-900">Recommendations</h3>
          <p className="text-sm text-gray-700">
            {marketResearch.recommendations}
          </p>
        </div>
      )}
    </div>
  );
}
