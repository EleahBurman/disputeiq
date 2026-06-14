import DisputeCard from "./DisputeCard";

const outcomeStyles = {
  approved: "bg-green-100 text-green-700",
  denied: "bg-red-100 text-red-700",
  needs_review: "bg-yellow-100 text-yellow-700",
};

const outcomeLabels = {
  approved: "✅ Approved",
  denied: "❌ Denied",
  needs_review: "⚠️ Needs Review",
};

export default function ResultsPanel({ result }) {
  const { extracted, outcome, confidence, explanation } = result;

  return (
    <div className="bg-white rounded-2xl shadow p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-bold text-gray-800">Analysis Result</h2>
        <span
          className={`px-4 py-1.5 rounded-full text-sm font-semibold ${outcomeStyles[outcome]}`}
        >
          {outcomeLabels[outcome]}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <DisputeCard label="Merchant" value={extracted.merchant_name} />
        <DisputeCard
          label="Amount"
          value={
            extracted.transaction_amount
              ? `$${extracted.transaction_amount}`
              : null
          }
        />
        <DisputeCard label="Date" value={extracted.transaction_date} />
        <DisputeCard
          label="Reason"
          value={extracted.dispute_reason?.replace(/_/g, " ")}
        />
        <DisputeCard
          label="Evidence Strength"
          value={
            extracted.evidence_strength
              ? `${extracted.evidence_strength} / 10`
              : null
          }
        />
        <DisputeCard
          label="Confidence"
          value={`${(confidence * 100).toFixed(0)}%`}
        />
      </div>

      <div className="bg-indigo-50 rounded-xl p-4">
        <p className="text-xs font-medium text-indigo-400 uppercase tracking-wide mb-1">
          Explanation
        </p>
        <p className="text-sm text-indigo-800">{explanation}</p>
      </div>

      <div className="bg-gray-50 rounded-xl p-4">
        <p className="text-xs font-medium text-gray-400 uppercase tracking-wide mb-1">
          Customer Claim
        </p>
        <p className="text-sm text-gray-700">{extracted.customer_claim}</p>
      </div>
    </div>
  );
}