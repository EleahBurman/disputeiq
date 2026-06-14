import { useState } from "react";
import UploadForm from "./components/UploadForm";
import ResultsPanel from "./components/ResultsPanel";
import { analyzeDispute } from "./api";

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (input) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await analyzeDispute(input);
      setResult(data);
    } catch (err) {
      setError("Something went wrong. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-2xl mx-auto space-y-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-indigo-600">DisputeIQ</h1>
          <p className="mt-2 text-gray-500 text-sm">
            AI-powered dispute evidence extraction and outcome classification
          </p>
        </div>

        <UploadForm onSubmit={handleSubmit} loading={loading} />

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 rounded-xl p-4 text-sm">
            {error}
          </div>
        )}

        {result && <ResultsPanel result={result} />}
      </div>
    </div>
  );
}