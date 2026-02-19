import { useState, useRef } from "react";

const SUPPORTED_DRUGS = ["CODEINE", "WARFARIN", "CLOPIDOGREL", "SIMVASTATIN", "AZATHIOPRINE", "FLUOROURACIL"];

export default function UploadSection({ onAnalyze, error }) {
  const [vcfFile, setVcfFile] = useState(null);
  const [selectedDrugs, setSelectedDrugs] = useState([]);
  const [dragging, setDragging] = useState(false);
  const fileRef = useRef();

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    if (file && file.name.endsWith(".vcf")) setVcfFile(file);
    else alert("Please upload a .vcf file");
  };

  const toggleDrug = (drug) => {
    setSelectedDrugs((prev) =>
      prev.includes(drug) ? prev.filter((d) => d !== drug) : [...prev, drug]
    );
  };

  const handleSubmit = () => {
    if (!vcfFile) return alert("Please upload a VCF file");
    if (selectedDrugs.length === 0) return alert("Select at least one drug");
    onAnalyze(vcfFile, selectedDrugs.join(","));
  };

  return (
    <div className="space-y-8">
      {/* Hero */}
      <div className="text-center space-y-3 py-6">
        <div className="inline-block px-3 py-1 rounded-full border border-emerald-800 text-emerald-400 text-xs mb-2">
          RIFT 2026 Hackathon · HealthTech Track
        </div>
        <h2 className="text-4xl font-bold text-white tracking-tight">
          Predict Drug Risk<br />
          <span className="text-emerald-400">From Your Genome</span>
        </h2>
        <p className="text-gray-400 max-w-lg mx-auto text-sm leading-relaxed">
          Upload a VCF genetic file and select a drug. PharmaGuard analyzes your pharmacogenomic profile
          and predicts personalized drug risks using CPIC guidelines + AI explanations.
        </p>
      </div>

      {/* Upload Zone */}
      <div
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        onClick={() => fileRef.current.click()}
        className={`border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-all duration-200
          ${dragging ? "border-emerald-400 bg-emerald-950/30" : "border-gray-700 hover:border-emerald-700 bg-gray-900/40"}`}
      >
        <input
          ref={fileRef}
          type="file"
          accept=".vcf"
          className="hidden"
          onChange={(e) => setVcfFile(e.target.files[0])}
        />
        <div className="text-4xl mb-3">🧬</div>
        {vcfFile ? (
          <div>
            <p className="text-emerald-400 font-bold">{vcfFile.name}</p>
            <p className="text-gray-500 text-sm mt-1">{(vcfFile.size / 1024).toFixed(1)} KB · Click to change</p>
          </div>
        ) : (
          <div>
            <p className="text-gray-300 font-medium">Drop your VCF file here</p>
            <p className="text-gray-500 text-sm mt-1">or click to browse · .vcf format · max 5MB</p>
          </div>
        )}
      </div>

      {/* Drug Selection */}
      <div>
        <p className="text-gray-400 text-sm mb-3 font-medium">Select Drug(s) to Analyze</p>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
          {SUPPORTED_DRUGS.map((drug) => (
            <button
              key={drug}
              onClick={() => toggleDrug(drug)}
              className={`px-4 py-3 rounded-lg border text-sm font-medium transition-all duration-150 text-left
                ${selectedDrugs.includes(drug)
                  ? "border-emerald-500 bg-emerald-950/50 text-emerald-300"
                  : "border-gray-700 text-gray-400 hover:border-gray-600 hover:text-gray-300"}`}
            >
              <div className="font-bold">{drug}</div>
              <div className="text-xs opacity-60 mt-0.5">{getDrugGene(drug)}</div>
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div className="bg-red-950/40 border border-red-800 rounded-lg p-4 text-red-400 text-sm">
          ⚠ {error}
        </div>
      )}

      <button
        onClick={handleSubmit}
        disabled={!vcfFile || selectedDrugs.length === 0}
        className="w-full py-4 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-gray-950 font-bold text-base
          transition-all duration-150 disabled:opacity-30 disabled:cursor-not-allowed"
      >
        Analyze Pharmacogenomic Risk →
      </button>

      <p className="text-center text-gray-600 text-xs">
        For research and educational purposes only. Not for clinical diagnosis.
      </p>
    </div>
  );
}

function getDrugGene(drug) {
  const map = {
    CODEINE: "CYP2D6", WARFARIN: "CYP2C9", CLOPIDOGREL: "CYP2C19",
    SIMVASTATIN: "SLCO1B1", AZATHIOPRINE: "TPMT", FLUOROURACIL: "DPYD"
  };
  return map[drug] || "";
}
