import { useState, useEffect } from "react";
import Lenis from 'lenis';
import { Toaster } from 'react-hot-toast';
import Header from "./components/Header";
import Hero from "./components/Hero";
import UploadSection from "./components/UploadSection";
import ResultsDisplay from "./components/ResultsDisplay";
import LoadingScreen from "./components/LoadingScreen";
import Footer from "./components/Footer";

// Expanded icon set for better density
const MEDICAL_ICONS = [
  "💊", "🩺", "🧬", "💉", "🏥", "⚕️", "🔬", "🫀", "🧪", "🦠",
  "💊", "🩺", "🧬", "💉", "🔬", "🧠", "🦷", "🦴", "🩸", "🩹",
  "💊", "🩺", "🧬", "💉", "⚕️", "🔬", "🧬", "💉", "🏥", "🧪",
  "💊", "🩺", "🧬", "💉", "🔬", "🫀", "🧠", "🦠", "🩸", "⚕️"
];

function FloatingIcons() {
  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden" style={{ zIndex: 0 }}>
      {MEDICAL_ICONS.map((icon, i) => {
        // Randomize positions and animations more naturally
        const left = Math.floor(Math.random() * 100);
        const duration = 15 + Math.random() * 20; // 15-35s
        const delay = Math.random() * 20; // 0-20s
        const size = 24 + Math.random() * 30; // 24-48px

        return (
          <div key={i} className="medical-icon" style={{
            left: `${left}%`,
            animationDuration: `${duration}s`,
            animationDelay: `-${delay}s`, // Negative delay to start mid-animation
            fontSize: `${size}px`,
            opacity: 0.1 + Math.random() * 0.1, // Varied opacity
          }}>
            {icon}
          </div>
        );
      })}
    </div>
  );
}

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [theme, setTheme] = useState("dark");

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  useEffect(() => {
    const lenis = new Lenis();

    function raf(time) {
      lenis.raf(time);
      requestAnimationFrame(raf);
    }

    requestAnimationFrame(raf);

    return () => {
      lenis.destroy();
    };
  }, []);


  const toggleTheme = () => {
    setTheme(prev => prev === "dark" ? "light" : "dark");
  };

  const handleAnalysis = async (vcfFile, drugs) => {
    setLoading(true); setError(null); setResult(null);
    const formData = new FormData();
    formData.append("vcf_file", vcfFile);
    formData.append("drugs", drugs);
    try {
      const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
      const res = await fetch(`${API_URL}/analyze`, { method: "POST", body: formData });
      if (!res.ok) { const e = await res.json(); throw new Error(e.detail || "Analysis failed"); }
      setResult(await res.json());
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen relative transition-colors duration-500">
      <div className="bg-medical" />
      <div className="grid-overlay" />
      <FloatingIcons />
      <div className="relative z-10 flex flex-col min-h-screen">
        <Header theme={theme} toggleTheme={toggleTheme} />
        <main className="flex-1 flex flex-col justify-center">
          {!result && !loading && <><Hero /><UploadSection onAnalyze={handleAnalysis} error={error} /></>}
          {loading && <LoadingScreen />}
          {result && <ResultsDisplay result={result} onReset={() => { setResult(null); setError(null); }} />}
        </main>
        <div className="mt-auto">
          <Footer />
        </div>
        <Toaster position="bottom-center" toastOptions={{
          style: {
            background: 'var(--card-bg)',
            color: 'var(--text-primary)',
            border: '1px solid var(--glass-border)',
            backdropFilter: 'blur(10px)',
          },
        }} />
      </div>
    </div>
  );
}
