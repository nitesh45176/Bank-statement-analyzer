const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function streamChat(
  statementId,
  message,
  onEvent
) {
  let response;
  try {
    response = await fetch(
      `${API_URL}/chat/stream`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          statement_id: statementId,
          message,
        }),
      }
    );
  } catch (netErr) {
    throw new Error(
      `Cannot connect to backend server at ${API_URL}. Please ensure the backend is running.`
    );
  }

  if (!response.ok) {
    let errorMessage = `Error (${response.status}): Failed to communicate with AI assistant.`;

    try {
      const errorData = await response.json();
      if (errorData.detail) {
        errorMessage = errorData.detail;
      }
    } catch {
      // Ignore JSON parsing errors
    }

    throw new Error(errorMessage);
  }

  if (!response.body) {
    throw new Error("Streaming is not supported by this browser/response.");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();

    if (done) {
      break;
    }

    buffer += decoder.decode(value, {
      stream: true,
    });

    const events = buffer.split("\n\n");
    buffer = events.pop() || "";

    for (const event of events) {
      const line = event
        .split("\n")
        .find((line) => line.startsWith("data:"));

      if (!line) {
        continue;
      }

      const data = line
        .replace(/^data:\s*/, "")
        .trim();

      if (!data) {
        continue;
      }

      try {
        const parsedEvent = JSON.parse(data);
        onEvent(parsedEvent);
      } catch (error) {
        console.error(
          "Failed to parse SSE event:",
          error
        );
      }
    }
  }
}