module.exports = async (req, res) => {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle preflight requests
  if (req.method === 'OPTIONS') {
    res.status(204).end();
    return;
  }

  // Only allow POST requests
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  try {
    const { url } = req.body;

    if (!url) {
      res.status(400).json({ error: 'URL is required' });
      return;
    }

    // For now, return a placeholder response
    res.status(200).json({
      recipe: `# Recipe from ${url}\n\n` +
             '## Ingredients\n' +
             '- Placeholder ingredient 1\n' +
             '- Placeholder ingredient 2\n\n' +
             '## Instructions\n' +
             '1. Placeholder step 1\n' +
             '2. Placeholder step 2'
    });
  } catch (error) {
    console.error('Error processing request:', error);
    res.status(500).json({ 
      error: 'Failed to process recipe',
      details: error.message
    });
  }
} 