export default function LoadingScreen() {
  return (
    <div className="flex flex-col items-center justify-center py-24 space-y-6">
      <div className="relative w-16 h-16">
        <div className="absolute inset-0 rounded-full border-4 border-gray-800" />
        <div className="absolute inset-0 rounded-full border-4 border-emerald-500 border-t-transparent animate-spin" />
      </div>
      <div className="text-center">
        <p className="text-emerald-400 font-bold text-lg">Analyzing Genome</p>
        <p className="text-gray-500 text-sm mt-1">Parsing VCF → Mapping variants → Predicting risk → Generating AI explanation</p>
      </div>
      <div className="flex gap-2">
        {["CYP2D6", "CYP2C19", "TPMT", "DPYD"].map((gene, i) => (
          <span
            key={gene}
            className="text-xs text-gray-600 border border-gray-800 rounded px-2 py-1 animate-pulse"
            style={{ animationDelay: `${i * 200}ms` }}
          >
            {gene}
          </span>
        ))}
      </div>
    </div>
  );
}
