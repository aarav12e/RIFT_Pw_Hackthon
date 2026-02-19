import { useState } from "react";
import ConfidenceGauge from "./ConfidenceGauge";

const RISK = {
  "Safe": { color: "#10b981", emoji: "✅", label: "SAFE", bg: "rgba(16,185,129,0.07)", border: "rgba(16,185,129,0.25)" },
  "Adjust Dosage": { color: "#f59e0b", emoji: "⚠️", label: "ADJUST DOSAGE", bg: "rgba(245,158,11,0.07)", border: "rgba(245,158,11,0.25)" },
  "Toxic": { color: "#ef4444", emoji: "☠️", label: "TOXIC", bg: "rgba(239,68,68,0.07)", border: "rgba(239,68,68,0.3)" },
  "Ineffective": { color: "#f97316", emoji: "🚫", label: "INEFFECTIVE", bg: "rgba(249,115,22,0.07)", border: "rgba(249,115,22,0.25)" },
};

const SEV = {
  "none": { w: "8%", c: "#10b981", l: "None" },
  "low": { w: "28%", c: "#f59e0b", l: "Low" },
  "moderate": { w: "55%", c: "#f97316", l: "Moderate" },
  "high": { w: "78%", c: "#ef4444", l: "High" },
  "critical": { w: "100%", c: "#dc2626", l: "Critical" },
};

function ResultCard({ result, index }) {
  const [open, setOpen] = useState({});
  const toggle = k => setOpen(p => ({ ...p, [k]: !p[k] }));

  const risk = result.risk_assessment;
  const profile = result.pharmacogenomic_profile;
  const rec = result.clinical_recommendation;
  const llm = result.llm_generated_explanation;
  const cfg = RISK[risk?.risk_label] || RISK["Safe"];
  const sev = SEV[risk?.severity] || SEV["none"];

  return (
    <div className="rounded-2xl p-6 sm:p-8 space-y-6 slide-up"
      style={{ background: cfg.bg, border: `1px solid ${cfg.border}`, animationDelay: `${index * 0.1}s` }}>

      {/* Header row */}
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <div className="flex items-center gap-3 mb-3">
            <span className="text-3xl">{cfg.emoji}</span>
            <div>
              <p className="text-xs font-semibold uppercase tracking-widest mb-1" style={{ color: cfg.color }}>Risk Assessment</p>
              <h3 className="text-2xl font-extrabold" style={{ color: 'var(--text-primary)' }}>{cfg.label}</h3>
            </div>
          </div>
          <div className="flex flex-wrap gap-2">
            {[result.drug, `Gene: ${profile?.primary_gene}`, result.patient_id].map(t => (
              <span key={t} className="px-3 py-1 rounded-full text-xs border"
                style={{ color: 'var(--text-secondary)', borderColor: 'var(--glass-border)', background: 'var(--card-bg)' }}>{t}</span>
            ))}
          </div>
        </div>
        <ConfidenceGauge score={risk?.confidence_score || 0} color={cfg.color} />
      </div>

      {/* Severity bar */}
      <div>
        <div className="flex justify-between text-xs mb-2">
          <span className="font-medium uppercase tracking-wider" style={{ color: 'var(--text-secondary)' }}>Severity</span>
          <span className="font-semibold" style={{ color: sev.c }}>{sev.l}</span>
        </div>
        <div className="h-2.5 rounded-full overflow-hidden" style={{ background: 'var(--border-color)' }}>
          <div className="h-full rounded-full transition-all duration-1000"
            style={{ width: sev.w, background: sev.c, boxShadow: `0 0 10px ${sev.c}60` }} />
        </div>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-3 gap-3">
        {[
          { label: "Diplotype", value: profile?.diplotype || "*1/*1" },
          { label: "Phenotype", value: profile?.phenotype || "NM" },
          { label: "PGx Variants", value: profile?.detected_variants?.length ?? 0 },
        ].map(({ label, value }) => (
          <div key={label} className="rounded-xl p-4 text-center" style={{ background: 'var(--card-bg)', border: '1px solid var(--glass-border)' }}>
            <p className="text-xs mb-1 font-medium" style={{ color: 'var(--text-secondary)' }}>{label}</p>
            <p className="font-extrabold text-lg" style={{ color: 'var(--text-primary)' }}>{value}</p>
          </div>
        ))}
      </div>

      {/* Recommendation */}
      <div className="rounded-xl p-5" style={{ background: 'rgba(0,0,0,0.05)', border: '1px solid var(--glass-border)' }}>
        <p className="text-xs font-semibold uppercase tracking-widest mb-2" style={{ color: cfg.color }}>
          ⚕ Clinical Recommendation
        </p>
        <p className="text-sm leading-relaxed" style={{ color: 'var(--text-primary)' }}>{rec?.action}</p>
        <p className="text-xs mt-2 italic" style={{ color: 'var(--text-secondary)' }}>{rec?.cpic_guideline}</p>
      </div>

      {/* Variants table */}
      {(profile?.detected_variants?.length ?? 0) > 0 && (
        <div>
          <button onClick={() => toggle("v")}
            className="flex items-center gap-2 text-xs transition mb-3 font-semibold uppercase tracking-wider"
            style={{ color: 'var(--text-secondary)' }}>
            <span style={{ color: cfg.color }}>{open.v ? "▾" : "▸"}</span>
            Detected Variants ({profile.detected_variants.length})
          </button>
          {open.v && (
            <div className="rounded-xl overflow-hidden" style={{ border: '1px solid var(--glass-border)' }}>
              <table className="w-full text-xs">
                <thead>
                  <tr style={{ background: 'var(--card-bg)' }}>
                    {["rsID", "Star Allele", "Function", "Genotype"].map(h => (
                      <th key={h} className="text-left py-3 px-4 font-semibold uppercase tracking-wider"
                        style={{ color: 'var(--text-secondary)' }}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {profile.detected_variants.map((v, i) => (
                    <tr key={i} style={{ borderTop: '1px solid var(--glass-border)' }}>
                      <td className="py-3 px-4 font-mono font-bold" style={{ color: cfg.color }}>{v.rsid}</td>
                      <td className="py-3 px-4 font-medium" style={{ color: 'var(--text-primary)' }}>{v.star_allele}</td>
                      <td className="py-3 px-4 capitalize" style={{ color: 'var(--text-secondary)' }}>{v.function_status?.replace(/_/g, " ")}</td>
                      <td className="py-3 px-4 font-mono" style={{ color: 'var(--text-secondary)' }}>{v.genotype}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* AI Explanation */}
      {llm && (
        <div>
          <button onClick={() => toggle("llm")}
            className="flex items-center gap-2 text-xs transition mb-3 font-semibold uppercase tracking-wider"
            style={{ color: 'var(--text-secondary)' }}>
            <span style={{ color: cfg.color }}>{open.llm ? "▾" : "▸"}</span>
            🤖 AI Clinical Explanation
          </button>
          {open.llm && (
            <div className="space-y-4 pl-4" style={{ borderLeft: `2px solid ${cfg.color}35` }}>
              {[
                { key: "summary", label: "Summary" },
                { key: "mechanism_explanation", label: "Mechanism" },
                { key: "patient_friendly", label: "For Patient" },
                { key: "clinical_significance", label: "Clinical Significance" },
                { key: "monitoring_parameters", label: "Monitoring Parameters" },
                { key: "alternative_drugs", label: "Alternative Drugs" },
              ].filter(({ key }) => llm[key]).map(({ key, label }) => (
                <div key={key}>
                  <p className="text-xs font-semibold uppercase tracking-wider mb-1" style={{ color: cfg.color }}>{label}</p>
                  <p className="text-sm leading-relaxed" style={{ color: 'var(--text-secondary)' }}>{llm[key]}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Metrics */}
      <div className="flex flex-wrap gap-4 text-xs pt-2 border-t" style={{ color: 'var(--text-secondary)', borderColor: 'var(--glass-border)' }}>
        <span>Parse: {result.quality_metrics?.vcf_parsing_success ? "✓" : "✗"}</span>
        <span>Total Variants: {result.quality_metrics?.total_variants_in_vcf}</span>
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
    const a = document.createElement("a"); a.href = url;
    a.download = `pharmaguard_${result.patient_id}_${Date.now()}.json`;
    a.click(); URL.revokeObjectURL(url);
  };

  return (
    <div className="max-w-5xl mx-auto px-6 pb-16 relative z-10 space-y-6">
      {/* Top bar */}
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <h2 className="text-2xl font-extrabold" style={{ color: 'var(--text-primary)' }}>Analysis Complete</h2>
          <p className="text-sm mt-1" style={{ color: 'var(--text-secondary)' }}>{result.patient_id} · {analyses.length} drug{analyses.length > 1 ? "s" : ""} analyzed</p>
        </div>
        <div className="flex flex-wrap gap-2 no-print">
          <button onClick={() => navigator.clipboard.writeText(JSON.stringify(result, null, 2))}
            className="px-4 py-2 text-xs font-semibold rounded-xl card transition"
            style={{ color: 'var(--text-secondary)', background: 'var(--card-bg)', border: '1px solid var(--glass-border)' }}>
            📋 Copy JSON
          </button>
          <button onClick={downloadJSON}
            className="px-4 py-2 text-xs font-semibold rounded-xl text-blue-300 transition"
            style={{ background: 'rgba(37,99,235,0.15)', border: '1px solid rgba(37,99,235,0.3)' }}>
            ↓ Download JSON
          </button>
          <button onClick={() => window.print()}
            className="px-4 py-2 text-xs font-semibold rounded-xl text-amber-300 transition"
            style={{ background: 'rgba(245,158,11,0.1)', border: '1px solid rgba(245,158,11,0.25)' }}>
            🖨 Print Report
          </button>
          <button onClick={onReset}
            className="px-4 py-2 text-xs font-semibold rounded-xl card transition"
            style={{ color: 'var(--text-primary)', background: 'var(--card-bg)', border: '1px solid var(--glass-border)' }}>
            ← New Analysis
          </button>
        </div>
      </div>

      {/* Cards */}
      <div className="stagger space-y-5">
        {analyses.map((r, i) => <ResultCard key={i} result={r} index={i} />)}
      </div>

      <p className="text-center text-xs pt-2" style={{ color: 'var(--text-secondary)' }}>
        PharmaGuard · CPIC-aligned · RIFT 2026 Hackathon · For research use only
      </p>
    </div>
  );
}
