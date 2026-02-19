import { useState } from "react";

const RISK_CONFIG = {
  "Safe": { color: "emerald", emoji: "✅", bg: "bg-emerald-950/50", border: "border-emerald-700", text: "text-emerald-400", badge: "bg-emerald-900 text-emerald-300" },
  "Adjust Dosage": { color: "yellow", emoji: "⚠️", bg: "bg-yellow-950/30", border: "border-yellow-700", text: "text-yellow-400", badge: "bg-yellow-900/50 text-yellow-300" },
  "Toxic": { color: "red", emoji: "☠️", bg: "bg-red-950/40", border: "border-red-700", text: "text-red-400", badge: "bg-red-900/50 text-red-300" },
  "Ineffective": { color: "orange", emoji: "🚫", bg: "bg-orange-950/30", border: "border-orange-700", text: "text-orange-400", badge: "bg-orange-900/50 text-orange-300" },
};

const SEVERITY_BAR = {
  "none": { width: "10%", color: "bg-emerald-500" },
  "low": { width: "30%", color: "bg-yellow-400" },
  "moderate": { width: "55%", color: "bg-orange-400" },
  "high": { width: "75%", color: "bg-red-400" },
  "critical": { width: "100%", color: "bg-red-600" },
};

function SingleResult({ result }) {
  const [expanded, setExpanded] = useState({});
  const risk = result.risk_assessment;
  const profile = result.pharmacogenomic_profile;
  const rec = result.clinical_recommendation;
  const llm = result.llm_generated_explanation;
  const config = RISK_CONFIG[risk?.risk_label] || RISK_CONFIG["Safe"];
  const severity = SEVERITY_BAR[risk?.severity] || SEVERITY_BAR["none"];

  const toggle = (k) => setExpanded((p) => ({ ...p, [k]: !p[k] }));

  return (
    <div className={`rounded-xl border ${config.border} ${config.bg} p-6 space-y-5`}>
      {/* Risk Header */}
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-2xl">{config.emoji}</span>
            <h3 className={`text-2xl font-bold ${config.text}`}>{risk?.risk_label}</h3>
          </div>
          <p className="text-gray-400 text-sm">
            <span className="text-white font-bold">{result.drug}</span> · Gene: <span className="text-white">{profile?.primary_gene}</span> · Patient: <span className="text-gray-300">{result.patient_id}</span>
          </p>
        </div>
        <div className={`px-4 py-2 rounded-lg text-sm font-bold ${config.badge}`}>
          Confidence: {Math.round((risk?.confidence_score || 0) * 100)}%
        </div>
      </div>

      {/* Severity Bar */}
      <div>
        <div className="flex justify-between text-xs text-gray-500 mb-1">
          <span>Severity</span>
          <span className="capitalize font-medium text-gray-300">{risk?.severity}</span>
        </div>
        <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
          <div className={`h-full rounded-full transition-all ${severity.color}`} style={{ width: severity.width }} />
        </div>
      </div>

      {/* Pharmacogenomic Profile */}
      <div className="grid grid-cols-3 gap-3">
        {[
          { label: "Diplotype", value: profile?.diplotype },
          { label: "Phenotype", value: profile?.phenotype },
          { label: "Variants Found", value: profile?.detected_variants?.length || 0 },
        ].map(({ label, value }) => (
          <div key={label} className="bg-gray-900/60 rounded-lg p-3 text-center">
            <div className="text-gray-500 text-xs mb-1">{label}</div>
            <div className="text-white font-bold text-sm">{value}</div>
          </div>
        ))}
      </div>

      {/* Variants Table */}
      {profile?.detected_variants?.length > 0 && (
        <div>
          <button onClick={() => toggle("variants")} className="text-xs text-gray-400 hover:text-white flex items-center gap-1 mb-2">
            {expanded.variants ? "▾" : "▸"} Detected Variants ({profile.detected_variants.length})
          </button>
          {expanded.variants && (
            <div className="overflow-x-auto">
              <table className="w-full text-xs border-collapse">
                <thead>
                  <tr className="border-b border-gray-700 text-gray-500">
                    <th className="text-left py-2 pr-4">rsID</th>
                    <th className="text-left py-2 pr-4">Star Allele</th>
                    <th className="text-left py-2 pr-4">Function</th>
                    <th className="text-left py-2">Genotype</th>
                  </tr>
                </thead>
                <tbody>
                  {profile.detected_variants.map((v, i) => (
                    <tr key={i} className="border-b border-gray-800/50">
                      <td className="py-2 pr-4 text-emerald-400 font-mono">{v.rsid}</td>
                      <td className="py-2 pr-4 text-white">{v.star_allele}</td>
                      <td className="py-2 pr-4 text-gray-300 capitalize">{v.function_status?.replace("_", " ")}</td>
                      <td className="py-2 text-gray-400 font-mono">{v.genotype}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* Clinical Recommendation */}
      <div className="bg-gray-900/50 rounded-lg p-4 border border-gray-800">
        <p className="text-gray-400 text-xs mb-2 font-semibold uppercase tracking-widest">Clinical Recommendation</p>
        <p className="text-gray-200 text-sm leading-relaxed">{rec?.action}</p>
        <p className="text-gray-500 text-xs mt-2 italic">{rec?.cpic_guideline}</p>
      </div>

      {/* LLM Explanation */}
      {llm && (
        <div className="space-y-3">
          <button onClick={() => toggle("llm")} className="text-xs text-gray-400 hover:text-white flex items-center gap-1">
            {expanded.llm ? "▾" : "▸"} AI Clinical Explanation
          </button>
          {expanded.llm && (
            <div className="space-y-3 pl-3 border-l-2 border-gray-700">
              {[
                { label: "Summary", key: "summary" },
                { label: "Mechanism", key: "mechanism_explanation" },
                { label: "For Patient", key: "patient_friendly" },
                { label: "Clinical Significance", key: "clinical_significance" },
                { label: "Monitoring", key: "monitoring_parameters" },
                { label: "Alternatives", key: "alternative_drugs" },
              ].map(({ label, key }) => llm[key] && (
                <div key={key}>
                  <p className="text-gray-500 text-xs font-semibold uppercase tracking-wider mb-1">{label}</p>
                  <p className="text-gray-300 text-sm leading-relaxed">{llm[key]}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Quality Metrics */}
      <div className="flex gap-4 text-xs text-gray-600">
        <span>Parse: {result.quality_metrics?.vcf_parsing_success ? "✓" : "✗"}</span>
        <span>Variants: {result.quality_metrics?.total_variants_in_vcf}</span>
        <span>PGx Hits: {result.quality_metrics?.pharmacogenomic_variants_found}</span>
        <span>Time: {result.quality_metrics?.processing_time_seconds}s</span>
      </div>
    </div>
  );
}

export default function ResultsDisplay({ result, onReset }) {
  const isMulti = !!result.multi_drug_analysis;
  const analyses = isMulti ? result.multi_drug_analysis : [result];

  const downloadJSON = () => {
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `pharmaguard_${result.patient_id}_${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const copyJSON = () => {
    navigator.clipboard.writeText(JSON.stringify(result, null, 2));
  };

  return (
    <div className="space-y-6">
      {/* Top Bar */}
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <h2 className="text-xl font-bold text-white">Analysis Complete</h2>
          <p className="text-gray-500 text-sm">Patient: {result.patient_id} · {analyses.length} drug(s) analyzed</p>
        </div>
        <div className="flex gap-2">
          <button onClick={copyJSON} className="px-3 py-2 text-xs border border-gray-700 rounded-lg text-gray-400 hover:text-white hover:border-gray-500 transition">
            Copy JSON
          </button>
          <button onClick={downloadJSON} className="px-3 py-2 text-xs border border-emerald-700 rounded-lg text-emerald-400 hover:bg-emerald-950/50 transition">
            ↓ Download JSON
          </button>
          <button onClick={onReset} className="px-3 py-2 text-xs bg-gray-800 rounded-lg text-gray-300 hover:bg-gray-700 transition">
            New Analysis
          </button>
        </div>
      </div>

      {/* Results */}
      <div className="space-y-5">
        {analyses.map((r, i) => (
          <SingleResult key={i} result={r} />
        ))}
      </div>

      <p className="text-center text-gray-600 text-xs pt-2">
        ⚕ PharmaGuard · CPIC-aligned · For research use only
      </p>
    </div>
  );
}
