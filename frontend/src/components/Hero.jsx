export default function Hero() {
  const stats = [
    { value: "6", label: "Genes Analyzed" },
    { value: "6", label: "Drugs Supported" },
    { value: "CPIC", label: "Guidelines" },
    { value: "AI", label: "Powered" },
  ];

  return (
    <section className="relative z-10 pt-14 pb-10 px-6 text-center max-w-5xl mx-auto">
      {/* Tag */}
      <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full card mb-8 text-sm"
        style={{ border: '1px solid var(--glass-border)' }}>
        <span>⚕️</span>
        <span style={{ color: 'var(--text-secondary)' }}>Adverse drug reactions kill</span>
        <span className="font-semibold accent-text">100,000+ Americans annually</span>
      </div>

      {/* Heading - clean, single color, professional */}
      <h2 className="text-5xl sm:text-6xl font-extrabold leading-tight mb-5 tracking-tight"
        style={{ fontFamily: 'Plus Jakarta Sans, sans-serif', color: 'var(--text-primary)' }}>
        Know Your Drug Risk
        <br />
        <span className="accent-text">Before It's Too Late</span>
      </h2>

      <p className="text-base max-w-2xl mx-auto mb-10 leading-relaxed"
        style={{ color: 'var(--text-secondary)' }}>
        Upload your genetic VCF file. Select a drug. Get AI-powered pharmacogenomic risk predictions
        aligned with CPIC clinical guidelines — in seconds.
      </p>

      {/* Stats */}
      <div className="flex flex-wrap justify-center gap-3 mb-2">
        {stats.map(({ value, label }) => (
          <div key={label} className="card rounded-2xl px-8 py-4 text-center min-w-[110px]"
            style={{ border: '1px solid var(--glass-border)' }}>
            <div className="text-2xl font-extrabold mb-1 accent-text"
              style={{ fontFamily: 'Plus Jakarta Sans, sans-serif' }}>{value}</div>
            <div className="text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>{label}</div>
          </div>
        ))}
      </div>
    </section>
  );
}
