export default function ResultsView({ criticOutput }) {
  const { scored_candidates: candidates, top_title: topTitle, rejection_log: rejectionLog } = criticOutput;

  return (
    <div className="results-view">
      <h2>Generated Titles</h2>

      <div className="candidates">
        {candidates.map((c, i) => (
          <div key={i} className={`candidate-card ${c.title === topTitle ? "top-pick" : ""}`}>
            {c.title === topTitle && <span className="top-badge">TOP PICK</span>}
            <p className="candidate-title">{c.title}</p>
            <p className="trigger">{c.trigger_used}</p>
            <div className="badges">
              <span className="badge">pCTR {(c.pctr_score * 100).toFixed(1)}%</span>
              <span className="badge">VADER {c.vader_compound.toFixed(2)}</span>
              <span className="badge">BERTScore {c.bert_similarity.toFixed(2)}</span>
              <span className={`badge nli-${c.nli_label}`}>NLI: {c.nli_label}</span>
              <span className="badge composite">Composite {c.composite_score.toFixed(3)}</span>
              <span className={`badge ${c.is_valid ? "valid" : "invalid"}`}>
                {c.is_valid ? "Valid" : "Rejected"}
              </span>
            </div>
          </div>
        ))}
      </div>

      {rejectionLog.length > 0 && (
        <div className="rejection-log">
          <h3>Rejection Log</h3>
          <ul>
            {rejectionLog.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
