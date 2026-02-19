import { useState, useRef } from "react";

const DRUGS = [
  { name: "CODEINE", gene: "CYP2D6", desc: "Opioid analgesic. Poor metabolizers get no pain relief; ultrarapid metabolizers risk respiratory depression from excess morphine." },
  { name: "WARFARIN", gene: "CYP2C9", desc: "Blood thinner. Poor metabolizers clear it slowly — leading to dangerous bleeding risk at standard doses." },
  { name: "CLOPIDOGREL", gene: "CYP2C19", desc: "Anti-platelet drug. Poor metabolizers cannot activate this prodrug, leaving patients unprotected against heart attacks." },
  { name: "SIMVASTATIN", gene: "SLCO1B1", desc: "Cholesterol drug. Poor transporters accumulate simvastatin in the blood, causing muscle damage (myopathy)." },
  { name: "AZATHIOPRINE", gene: "TPMT", desc: "Immunosuppressant. TPMT-deficient patients accumulate toxic metabolites — risk of fatal bone marrow failure." },
  { name: "FLUOROURACIL", gene: "DPYD", desc: "Chemotherapy. DPYD-deficient patients cannot break down the drug — standard doses cause life-threatening toxicity." },
];

const SAMPLES = [
  { tag: "✅ Normal", label: "Reference Genotype", drug: "WARFARIN", content: `##fileformat=VCFv4.2\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tPATIENT_NM\nchr10\t94942290\trs1799853\tC\tT\t99\tPASS\tGENE=CYP2C9;STAR=*2\tGT\t0|0\nchr10\t94981296\trs1057910\tA\tC\t99\tPASS\tGENE=CYP2C9;STAR=*3\tGT\t0|0` },
  { tag: "⚠️ Action", label: "Warfarin Dose Adjustment", drug: "WARFARIN", content: `##fileformat=VCFv4.2\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tPATIENT_PM\nchr10\t94942290\trs1799853\tC\tT\t99\tPASS\tGENE=CYP2C9;STAR=*2\tGT\t0|1\nchr10\t94981296\trs1057910\tA\tC\t99\tPASS\tGENE=CYP2C9;STAR=*3\tGT\t0|1` },
  { tag: "🔴 Risk", label: "Simvastatin High Risk", drug: "SIMVASTATIN", content: `##fileformat=VCFv4.2\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tPATIENT_SLCO1B1\nchr12\t21151622\trs4149056\tT\tC\t99\tPASS\tGENE=SLCO1B1;STAR=*5\tGT\t0|1\nchr12\t21142512\trs11045819\tA\tG\t99\tPASS\tGENE=SLCO1B1;STAR=*14\tGT\t0|1` },
  { tag: "☠️ Toxic", label: "Fluorouracil Contraindicated", drug: "FLUOROURACIL", content: `##fileformat=VCFv4.2\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tPATIENT_DPYD\nchr1\t97915614\trs3918290\tC\tT\t99\tPASS\tGENE=DPYD;STAR=*2A\tGT\t0|1\nchr1\t97981343\trs55886062\tA\tT\t99\tPASS\tGENE=DPYD;STAR=*13\tGT\t0|1` },
];

export default function UploadSection({ onAnalyze, error }) {
  const [vcfFile, setVcfFile] = useState(null);
  const [selectedDrugs, setSelectedDrugs] = useState([]);
  const [dragging, setDragging] = useState(false);
  const fileRef = useRef();

  const handleDrop = (e) => {
    e.preventDefault(); setDragging(false);
    const file = e.dataTransfer.files[0];
    if (file?.name.endsWith(".vcf")) setVcfFile(file);
    else alert("Please upload a .vcf file");
  };

  const toggleDrug = (drug) => setSelectedDrugs(p => p.includes(drug) ? p.filter(d => d !== drug) : [...p, drug]);

  const loadSample = (s) => {
    const blob = new Blob([s.content], { type: "text/plain" });
    setVcfFile(new File([blob], `${s.label.replace(/ /g, "_")}.vcf`));
    setSelectedDrugs([s.drug]);
  };

  const isSelected = (drug) => selectedDrugs.includes(drug);

  return (
    <div className="max-w-5xl mx-auto px-6 pb-16 relative z-10 space-y-6">

      {/* Quick load */}
      <div className="card rounded-2xl p-5" style={{ background: 'var(--card-bg)' }}>
        <p className="text-xs font-semibold uppercase tracking-widest mb-3" style={{ color: 'var(--text-secondary)' }}>
          Load Predefined Clinical Scenarios
        </p>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
          {SAMPLES.map((s) => (
            <button key={s.label} onClick={() => loadSample(s)}
              className="rounded-xl px-4 py-3 text-left transition-colors duration-200"
              style={{ background: 'var(--card-hover)', border: '1px solid var(--glass-border)' }}>
              <div className="text-sm font-semibold mb-0.5" style={{ color: 'var(--text-primary)' }}>{s.tag}</div>
              <div className="text-xs" style={{ color: 'var(--text-secondary)' }}>{s.label}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Upload zone */}
      <div
        className={`upload-zone rounded-2xl p-14 text-center ${dragging ? 'drag-over' : ''}`}
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        onClick={() => fileRef.current.click()}
      >
        <input ref={fileRef} type="file" accept=".vcf" className="hidden"
          onChange={(e) => setVcfFile(e.target.files[0])} />
        {vcfFile ? (
          <div>
            <div className="text-4xl mb-3">🧬</div>
            <p className="font-semibold text-lg" style={{ color: 'var(--text-primary)' }}>{vcfFile.name}</p>
            <p className="text-sm mt-1" style={{ color: 'var(--text-secondary)' }}>Ready to analyze · Click to change file</p>
            <div className="inline-block mt-3 px-3 py-1 rounded-full text-xs font-medium text-emerald-400"
              style={{ background: 'rgba(16,185,129,0.1)', border: '1px solid rgba(16,185,129,0.25)' }}>
              VCF File Loaded ✓
            </div>
          </div>
        ) : (
          <div>
            <div className="text-5xl mb-4">🧬</div>
            <p className="font-semibold text-lg mb-1" style={{ color: 'var(--text-primary)' }}>Drop your VCF file here</p>
            <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>or click to browse · .vcf format · max 5MB</p>
          </div>
        )}
      </div>

      {/* Drug selection */}
      <div>
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-1 bg-gradient-to-r from-[var(--accent-primary)] to-[var(--accent-secondary)] rounded-full" />
          <p className="font-semibold text-sm" style={{ color: 'var(--text-primary)' }}>Select Drug(s) to Analyze</p>
          {selectedDrugs.length > 0 &&
            <span className="ml-auto text-xs font-medium accent-text">{selectedDrugs.length} selected</span>}
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
          {DRUGS.map(({ name, gene, desc }) => (
            <div key={name} className="tooltip">
              <button onClick={() => toggleDrug(name)}
                className={`w-full rounded-2xl px-5 py-4 text-left transition-all duration-200 border`}
                style={{
                  background: isSelected(name) ? 'rgba(37,99,235,0.1)' : 'var(--card-bg)', // Slight tint for selection
                  borderColor: isSelected(name) ? 'var(--accent-primary)' : 'var(--glass-border)',
                  boxShadow: isSelected(name) ? '0 0 15px var(--shadow-color)' : 'none'
                }}>
                <div className="flex items-center justify-between mb-1">
                  <span className={`font-bold text-sm ${isSelected(name) ? 'accent-text' : ''}`}
                    style={{ color: isSelected(name) ? 'var(--accent-primary)' : 'var(--text-primary)' }}>
                    {name}
                  </span>
                  {isSelected(name) && <span className="text-xs accent-text">✓</span>}
                </div>
                <div className="text-xs font-mono" style={{ color: 'var(--text-secondary)' }}>{gene}</div>
              </button>
              <div className="tip">
                <strong style={{ color: 'var(--text-primary)' }}>{name}</strong><br />{desc}
              </div>
            </div>
          ))}
        </div>
      </div>

      {error && (
        <div className="rounded-xl p-4 text-sm text-red-400"
          style={{ background: 'rgba(239,68,68,0.08)', border: '1px solid rgba(239,68,68,0.25)' }}>
          ⚠ {error}
        </div>
      )}

      <button onClick={() => onAnalyze(vcfFile, selectedDrugs.join(","))}
        disabled={!vcfFile || !selectedDrugs.length}
        className="btn-primary w-full py-4 rounded-2xl text-base font-bold shadow-lg ring-1 ring-white/10"
        style={{ color: '#fff' }}>
        {vcfFile && selectedDrugs.length
          ? `Analyze ${selectedDrugs.length} Drug${selectedDrugs.length > 1 ? 's' : ''} →`
          : 'Upload VCF & Select Drug to Continue'}
      </button>


    </div>
  );
}
