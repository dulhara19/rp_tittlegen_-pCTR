const API_BASE_URL = "http://localhost:8000";

export async function generateTitles({ videoTranscript, videoDescription, videoCategory }) {
  const response = await fetch(`${API_BASE_URL}/generate-titles`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      video_transcript: videoTranscript,
      video_description: videoDescription || undefined,
      video_category: videoCategory,
    }),
  });

  const body = await response.json();

  if (!response.ok) {
    const error = new Error(formatErrorDetail(body.detail));
    error.status = response.status;
    throw error;
  }

  return body;
}

function formatErrorDetail(detail) {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail.map((d) => d.msg || JSON.stringify(d)).join("; ");
  }
  return "Something went wrong.";
}
