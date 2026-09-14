import ResultsView from "./ResultsView";

const STAGES = [
  { key: "analyzer", label: "1. Analyzer", subtitle: "Reads the transcript, extracts a grounded video brief" },
  { key: "generator", label: "2. Generator", subtitle: "Drafts 5 candidate titles from the brief (never sees the raw transcript)" },
  { key: "critic", label: "3. Critic", subtitle: "Scores every candidate on pCTR / VADER / BERTScore / NLI and ranks them" },
];

export default function WorkflowView({ videoBrief, generatorOutput, criticOutput }) {
  return (
    <div className="workflow-view">
      <h2>Agentic Pipeline</h2>
      <p className="workflow-note">
        All three agents ran sequentially for this request (total ~7–10s); their outputs are
        shown below in pipeline order.
      </p>

      <ol className="pipeline-track">
        {STAGES.map((s) => (
          <li key={s.key} className="pipeline-step">
            <span className="step-label">{s.label}</span>
            <span className="step-subtitle">{s.subtitle}</span>
          </li>
        ))}
      </ol>

      <section className="stage-panel">
        <h3>Stage 1 — Analyzer output (video brief)</h3>
        <dl className="brief-grid">
          <dt>Core promise</dt>
          <dd>{videoBrief.core_promise}</dd>

          <dt>Key entities</dt>
          <dd>
            {videoBrief.key_entities.length > 0 ? (
              <ul className="chip-list">
                {videoBrief.key_entities.map((e, i) => (
                  <li key={i} className="chip">{e}</li>
                ))}
              </ul>
            ) : (
              <span className="muted">none extracted</span>
            )}
          </dd>

          <dt>Emotional potential</dt>
          <dd>{(videoBrief.emotional_potential * 100).toFixed(0)}%</dd>

          <dt>Trigger candidates</dt>
          <dd>
            <ul className="chip-list">
              {videoBrief.trigger_candidates.map((t, i) => (
                <li key={i} className="chip trigger-chip">{t}</li>
              ))}
            </ul>
          </dd>
        </dl>
      </section>

      <section className="stage-panel">
        <h3>Stage 2 — Generator output (draft candidates, before scoring)</h3>
        <ul className="draft-list">
          {generatorOutput.candidates.map((c, i) => (
            <li key={i} className="draft-card">
              <span className="draft-title">{c.title}</span>
              <span className="draft-meta">
                {c.trigger_used} · {c.char_count} chars · {c.word_count} words
              </span>
            </li>
          ))}
        </ul>
      </section>

      <section className="stage-panel">
        <h3>Stage 3 — Critic output (scored &amp; ranked)</h3>
        <ResultsView criticOutput={criticOutput} />
      </section>
    </div>
  );
}
