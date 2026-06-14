export async function analyzeDispute({ text, file }) {
  const formData = new FormData();
  
  if (file) {
    formData.append('file', file);
  } else {
    formData.append('text', text);
  }

  const response = await fetch('https://disputeiq.onrender.com/analyze', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Analysis failed');
  }

  return response.json();
}