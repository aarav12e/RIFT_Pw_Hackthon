import { useEffect, useState } from "react";

export default function ConfidenceGauge({ score, color }) {
  const [animated, setAnimated] = useState(0);
  const pct = Math.round(score * 100);
  const r = 42;
  const circ = 2 * Math.PI * r;
  const offset = circ - (animated / 100) * circ;

  useEffect(() => {
    const t = setTimeout(() => setAnimated(pct), 150);
    return () => clearTimeout(t);
  }, [pct]);

  return (
    <div className="flex flex-col items-center gap-1">
      <div className="relative w-24 h-24">
        <svg className="w-full h-full -rotate-90" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r={r} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="7" />
          <circle cx="50" cy="50" r={r} fill="none"
            stroke={color} strokeWidth="7" strokeLinecap="round"
            strokeDasharray={circ} strokeDashoffset={offset}
            style={{ transition: 'stroke-dashoffset 1.2s cubic-bezier(0.34,1.56,0.64,1)', filter: `drop-shadow(0 0 5px ${color}80)` }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-xl font-extrabold text-white">{pct}%</span>
          <span className="text-white/35 text-xs">confidence</span>
        </div>
      </div>
    </div>
  );
}
