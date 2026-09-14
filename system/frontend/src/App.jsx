import { useState } from "react";
import TitleForm from "./components/TitleForm";
import WorkflowView from "./components/WorkflowView";
import { generateTitles } from "./api";
import "./App.css";

function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  async function handleSubmit(formValues) {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const response = await generateTitles(formValues);
      setResult(response);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app">
      <h1>AI-Powered YouTube Title Optimizer</h1>
      <p className="subtitle">Analyzer → Generator → Critic pipeline</p>

      <TitleForm onSubmit={handleSubmit} loading={loading} />

      {error && <div className="error-banner">{error}</div>}

      {result && (
        <WorkflowView
          videoBrief={result.video_brief}
          generatorOutput={result.generator_output}
          criticOutput={result.critic_output}
        />
      )}
    </main>
  );
}

export default App;
