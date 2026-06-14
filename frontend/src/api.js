export async function analyzeDispute({ text, file }) {
  const formData = new FormData();
  
  if (file) {
    formData.append('file', file);
  } else {
    formData.append('text', text);
  }

  const response = await fetch('http://127.0.0.1:8000/analyze', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Analysis failed');
  }

  return response.json();
}