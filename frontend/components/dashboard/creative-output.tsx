"use client";

interface Headline {
  text: string;
  platform: string;
  character_count: number;
}

interface CreativeConcept {
  concept_name: string;
  description: string;
  image_prompt: string;
  format: string;
  platform: string;
}

interface CreativeOutputProps {
  adCopy: {
    headlines?: Headline[];
    primary_text?: { text: string; platform: string }[];
    ctas?: string[];
    reasoning?: string;
  };
  visualCreative: {
    creative_concepts?: CreativeConcept[];
    reasoning?: string;
  };
}

export function CreativeOutput({ adCopy, visualCreative }: CreativeOutputProps) {
  return (
    <div className="space-y-6">
      {/* Headlines */}
      {adCopy?.headlines && adCopy.headlines.length > 0 && (
        <div className="rounded-xl border bg-white p-6">
          <h3 className="mb-3 font-semibold text-gray-900">
            Headlines ({adCopy.headlines.length})
          </h3>
          <div className="space-y-2">
            {adCopy.headlines.map((h, i) => (
              <div
                key={i}
                className="flex items-center justify-between rounded-lg bg-gray-50 px-4 py-2"
              >
                <span className="text-sm font-medium text-gray-800">
                  &ldquo;{h.text}&rdquo;
                </span>
                <div className="flex items-center gap-2">
                  <span className="rounded bg-blue-50 px-2 py-0.5 text-xs text-blue-600">
                    {h.platform}
                  </span>
                  <span className="text-xs text-gray-400">
                    {h.character_count} chars
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Primary Text */}
      {adCopy?.primary_text && adCopy.primary_text.length > 0 && (
        <div className="rounded-xl border bg-white p-6">
          <h3 className="mb-3 font-semibold text-gray-900">
            Ad Copy ({adCopy.primary_text.length} variations)
          </h3>
          <div className="space-y-3">
            {adCopy.primary_text.map((p, i) => (
              <div key={i} className="rounded-lg bg-gray-50 px-4 py-3">
                <p className="text-sm text-gray-700">{p.text}</p>
                <span className="mt-1 inline-block rounded bg-blue-50 px-2 py-0.5 text-xs text-blue-600">
                  {p.platform}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* CTAs */}
      {adCopy?.ctas && adCopy.ctas.length > 0 && (
        <div className="rounded-xl border bg-white p-6">
          <h3 className="mb-3 font-semibold text-gray-900">
            Call-to-Action Options
          </h3>
          <div className="flex flex-wrap gap-2">
            {adCopy.ctas.map((cta, i) => (
              <span
                key={i}
                className="rounded-full bg-brand-50 px-4 py-1.5 text-sm font-medium text-brand-700"
              >
                {cta}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Visual Concepts */}
      {visualCreative?.creative_concepts &&
        visualCreative.creative_concepts.length > 0 && (
          <div className="rounded-xl border bg-white p-6">
            <h3 className="mb-3 font-semibold text-gray-900">
              Visual Concepts ({visualCreative.creative_concepts.length})
            </h3>
            <div className="grid gap-4 md:grid-cols-2">
              {visualCreative.creative_concepts.map((c, i) => (
                <div key={i} className="rounded-lg border p-4">
                  <div className="flex items-center justify-between">
                    <h4 className="font-medium text-gray-900">
                      {c.concept_name}
                    </h4>
                    <span className="rounded bg-purple-50 px-2 py-0.5 text-xs text-purple-600">
                      {c.format}
                    </span>
                  </div>
                  <p className="mt-2 text-sm text-gray-600">{c.description}</p>
                  <div className="mt-3 rounded bg-gray-50 p-3">
                    <p className="text-xs font-medium text-gray-500">
                      Image Prompt
                    </p>
                    <p className="mt-1 text-xs text-gray-700">
                      {c.image_prompt}
                    </p>
                  </div>
                  <span className="mt-2 inline-block rounded bg-blue-50 px-2 py-0.5 text-xs text-blue-600">
                    {c.platform}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

      {/* Reasoning */}
      {(adCopy?.reasoning || visualCreative?.reasoning) && (
        <div className="rounded-xl border bg-white p-6">
          <h3 className="mb-3 font-semibold text-gray-900">
            Creative Rationale
          </h3>
          {adCopy?.reasoning && (
            <div className="mb-3">
              <p className="text-xs font-medium text-gray-500">Copy Strategy</p>
              <p className="mt-1 text-sm text-gray-700">{adCopy.reasoning}</p>
            </div>
          )}
          {visualCreative?.reasoning && (
            <div>
              <p className="text-xs font-medium text-gray-500">
                Visual Strategy
              </p>
              <p className="mt-1 text-sm text-gray-700">
                {visualCreative.reasoning}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
