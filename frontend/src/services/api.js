
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

/**
 * Sends conversation history and selected agent role to the backend.
 * Returns the assistant's reply.
 */
export async function sendChatMessage(messages, role = 'founder') {
  const cleanBaseUrl = API_BASE_URL.replace(/\/+$/, '');
  const url = `${cleanBaseUrl}/chat/completions`;

  const payload = {
    model: 'foundrai',
    messages,
    stream: false,
    role,
  };

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      let errorMessage = `Server error: ${response.status} ${response.statusText}`;

      try {
        const errorJson = await response.json();
        if (errorJson?.detail) {
          errorMessage = errorJson.detail;
        }
      } catch {
        // Keep the original status-based error message.
      }

      throw new Error(errorMessage);
    }

    const data = await response.json();

    if (data?.choices?.[0]?.message?.content) {
      return data.choices[0].message.content;
    }

    throw new Error('Invalid response structure received from server.');
  } catch (err) {
    console.error('API Error details:', err);
    throw err;
  }
}
