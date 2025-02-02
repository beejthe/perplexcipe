const axios = require('axios');

async function processRecipe(url) {
  try {
    const prompt = `You are a recipe parser. Given a recipe URL, visit the page and extract the recipe in a clear, standardized format. Focus on:
1. Title of the recipe
2. List of ingredients with precise measurements
3. Step-by-step cooking instructions
4. Any special notes or tips

For the URL: ${url}

Format the output in markdown with clear sections. Be thorough but concise. Remove any unnecessary text, ads, or personal stories. Just give me the essential recipe information.`;

    const response = await axios.post('https://api.perplexity.ai/chat/completions', {
      model: 'sonar-pro',
      messages: [
        {
          role: 'system',
          content: 'You are a specialized recipe parser that extracts and formats recipes in a clear, standardized way.'
        },
        {
          role: 'user',
          content: prompt
        }
      ]
    }, {
      headers: {
        'Authorization': `Bearer ${process.env.PERPLEXITY_API_KEY}`,
        'Content-Type': 'application/json'
      }
    });

    return response.data.choices[0].message.content;
  } catch (error) {
    console.error('Error processing recipe:', error);
    throw new Error('Failed to process recipe from the provided URL');
  }
}

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

    // Validate URL
    try {
      new URL(url);
    } catch (e) {
      res.status(400).json({ error: 'Invalid URL format' });
      return;
    }

    // Process the recipe using Perplexity API
    const recipe = await processRecipe(url);
    
    res.status(200).json({ recipe });
  } catch (error) {
    console.error('Error processing request:', error);
    res.status(500).json({ 
      error: 'Failed to process recipe',
      details: error.message
    });
  }
} 