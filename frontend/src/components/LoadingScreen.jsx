import { useEffect, useState } from "react";

const STEPS = [
  { icon: "📂", label: "Parsing VCF File" },
  { icon: "🧬", label: "Mapping Genetic Variants" },
  { icon: "⚗️", label: "Applying CPIC Guidelines" },
  { icon: "🤖", label: "Generating AI Explanation" },
];

export default function LoadingScreen() {
  const [step, setStep] = useState(0);

  useEffect(() => {
    const t = setInterval(() => setStep(s => Math.min(s + 1, STEPS.length - 1)), 2800);
    return () => clearInterval(t);
  }, []);

  return (
    <div className="relative z-10 flex flex-col items-center justify-center px-6">
      {/* Spinner */}
      <div className="relative w-24 h-24 mb-10">
        <div className="absolute inset-0 rounded-full border-4" style={{ borderColor: 'var(--glass-border)' }} />
        <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-[var(--accent-primary)]"
          style={{ animation: 'spin 1s linear infinite' }} />
        <div className="absolute inset-3 rounded-full border-4 border-transparent border-t-[var(--accent-secondary)]"
          style={{ animation: 'spin 1.5s linear infinite reverse' }} />
        <div className="absolute inset-0 flex items-center justify-center text-2xl">🧬</div>
      </div>

      <h3 className="text-2xl font-bold mb-2" style={{ color: 'var(--text-primary)' }}>Analyzing Your Genome</h3>
      <p className="text-sm mb-10" style={{ color: 'var(--text-secondary)' }}>Please wait — this takes 5 to 15 seconds</p>

      <div className="w-full max-w-sm space-y-3">
        {STEPS.map(({ icon, label }, i) => (
          <div key={label} className={`flex items-center gap-3 px-5 py-3.5 rounded-xl transition-all duration-500 ${i <= step ? 'card' : 'opacity-25'}`}
            style={{
              background: i <= step ? 'var(--card-bg)' : 'transparent',
              border: i <= step ? '1px solid var(--accent-primary)' : '1px solid var(--glass-border)'
            }}>
            <span className="text-lg">{i < step ? "✅" : i === step ? icon : "○"}</span>
            <span className={`text-sm font-medium ${i <= step ? 'text-[var(--text-primary)]' : 'text-[var(--text-secondary)]'}`}>{label}</span>
            {i === step && (
              <div className="ml-auto flex gap-1">
                {[0, 1, 2].map(j => (
                  <div key={j} className="w-1.5 h-1.5 rounded-full bg-[var(--accent-secondary)] animate-bounce"
                    style={{ animationDelay: `${j * 0.15}s` }} />
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
