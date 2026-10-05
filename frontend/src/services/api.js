const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

/**
 * Sends the full messages array to the backend and returns the assistant's reply.
 * Uses the exact schema: choices[0].message.content
 * 
 * @param {Array<{role: string, content: string}>} messages 
 * @returns {Promise<string>} Content of the assistant's message
 */
export async function sendChatMessage(messages, role = null) {
  const cleanBaseUrl = API_BASE_URL.replace(/\/$/, '');
  const url = `${cleanBaseUrl}/chat/completions`;

  const payload = {
    model: 'fondrai',
    messages: messages,
    stream: false,
    role: role
  };

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      let errorMessage = `Server error: ${response.status} ${response.statusText}`;
      try {
        const errorJson = await response.json();
        if (errorJson && errorJson.detail) {
          errorMessage = errorJson.detail;
        }
      } catch (jsonErr) {
        // Fallback to text or status if parsing fails
      }
      throw new Error(errorMessage);
    }

    const data = await response.json();
    
    // Extract choice message content
    if (data && data.choices && data.choices[0] && data.choices[0].message) {
      return data.choices[0].message.content;
    }
    
    throw new Error('Invalid response structure received from server.');
  } catch (err) {
    console.error('API Error details:', err);
    throw err;
  }
}
