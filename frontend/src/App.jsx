import { useState } from "react";
import UploadSection from "./components/UploadSection";
import ResultsDisplay from "./components/ResultsDisplay";
import Header from "./components/Header";
import LoadingScreen from "./components/LoadingScreen";

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalysis = async (vcfFile, drugs) => {
    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append("vcf_file", vcfFile);
    formData.append("drugs", drugs);

    try {
      const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
      const res = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Analysis failed");
      }

      const data = await res.json();
      setResult(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white font-mono">
      <Header />
      <main className="max-w-5xl mx-auto px-4 py-10">
        {!result && !loading && (
          <UploadSection onAnalyze={handleAnalysis} error={error} />
        )}
        {loading && <LoadingScreen />}
        {result && <ResultsDisplay result={result} onReset={handleReset} />}
      </main>
    </div>
  );
}
