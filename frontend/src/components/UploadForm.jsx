import { useState } from "react";

export default function UploadForm({ onSubmit, loading, onModeChange }) {
  const [mode, setMode] = useState("text");
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (mode === "text" && text.trim()) {
      onSubmit({ text });
    } else if (mode === "file" && file) {
      onSubmit({ file });
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow p-6">
      <div className="flex gap-4 mb-6">
        <button
          onClick={() => { setMode("text"); setFile(null); onModeChange(); }}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            mode === "text"
              ? "bg-indigo-600 text-white"
              : "bg-gray-100 text-gray-600 hover:bg-gray-200"
          }`}
        >
          Paste Text
        </button>
        <button
          onClick={() => { setMode("file"); setText(""); onModeChange(); }}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            mode === "file"
              ? "bg-indigo-600 text-white"
              : "bg-gray-100 text-gray-600 hover:bg-gray-200"
          }`}
        >
          Upload PDF
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        {mode === "text" ? (
          <textarea
            className="w-full border border-gray-200 rounded-xl p-4 text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-400 min-h-[160px] resize-none"
            placeholder="Paste dispute evidence here... e.g. 'I ordered headphones from SoundCo on 2024-03-10 for $149.99. The item arrived broken.'"
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
        ) : (
          <div className="border-2 border-dashed border-gray-200 rounded-xl p-8 text-center">
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setFile(e.target.files[0])}
              className="hidden"
              id="pdf-upload"
            />
            <label htmlFor="pdf-upload" className="cursor-pointer">
              <p className="text-gray-500 text-sm">
                {file ? file.name : "Click to upload a PDF"}
              </p>
            </label>
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="mt-4 w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 rounded-xl transition-colors disabled:opacity-50"
        >
          {loading ? "Analyzing..." : "Analyze Dispute"}
        </button>
      </form>
    </div>
  );
}