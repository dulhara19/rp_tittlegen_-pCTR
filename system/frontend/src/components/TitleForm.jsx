import { useState } from "react";

export default function TitleForm({ onSubmit, loading }) {
  const [videoTranscript, setVideoTranscript] = useState("");
  const [videoDescription, setVideoDescription] = useState("");
  const [videoCategory, setVideoCategory] = useState("");

  const wordCount = videoTranscript.trim() ? videoTranscript.trim().split(/\s+/).length : 0;

  function handleSubmit(e) {
    e.preventDefault();
    onSubmit({ videoTranscript, videoDescription, videoCategory });
  }

  return (
    <form className="title-form" onSubmit={handleSubmit}>
      <label>
        Video transcript
        <textarea
          rows={8}
          value={videoTranscript}
          onChange={(e) => setVideoTranscript(e.target.value)}
          placeholder="Paste the video's spoken transcript here (at least 50 words)..."
          required
        />
        <span className="hint">{wordCount} words</span>
      </label>

      <label>
        Video description (optional)
        <textarea
          rows={3}
          value={videoDescription}
          onChange={(e) => setVideoDescription(e.target.value)}
          placeholder="Optional short description of the video"
        />
      </label>

      <label>
        Video category
        <input
          type="text"
          value={videoCategory}
          onChange={(e) => setVideoCategory(e.target.value)}
          placeholder="e.g. Science & Technology"
          required
        />
      </label>

      <button type="submit" disabled={loading}>
        {loading ? "Generating titles… (~10s)" : "Generate Titles"}
      </button>
    </form>
  );
}
