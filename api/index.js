const recipe = require('./recipe');

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

  // Route requests
  const path = req.url.split('?')[0];
  
  if (path === '/api/recipe') {
    return recipe(req, res);
  }

  // Handle 404
  res.status(404).json({ error: 'Not found' });
} 