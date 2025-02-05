const axios = require('axios');

async function processRecipe(url) {
  try {
    if (!process.env.PERPLEXCIPE_PERPLEXITY_API_KEY) {
      throw new Error('PERPLEXCIPE_PERPLEXITY_API_KEY environment variable is not set');
    }

    console.log('Making request to Perplexity API for URL:', url);

    const prompt = `You are a recipe parser. Given a recipe URL, visit the page and extract the recipe in a clear, standardized format. Focus on:
1. Title of the recipe
2. List of ingredients with precise measurements
3. Step-by-step cooking instructions
4. Any special notes or tips

For the URL: ${url}

Format the output in markdown with clear sections. Be thorough but concise. Remove any unnecessary text, ads, or personal stories. Just give me the essential recipe information.`;

    const apiRequest = {
      model: 'pplx-7b-online',
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
    };

    console.log('API Request:', JSON.stringify(apiRequest, null, 2));

    const response = await axios.post('https://api.perplexity.ai/chat/completions', apiRequest, {
      headers: {
        'Authorization': `Bearer ${process.env.PERPLEXCIPE_PERPLEXITY_API_KEY.trim()}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      timeout: 30000 // 30 second timeout
    });

    console.log('API Response status:', response.status);
    
    if (!response.data || !response.data.choices || !response.data.choices[0]) {
      console.error('Invalid API response format:', response.data);
      throw new Error('Invalid response format from Perplexity API');
    }

    const recipe = response.data.choices[0].message.content;
    console.log('Successfully received recipe content');
    return recipe;
  } catch (error) {
    console.error('Error processing recipe:', {
      message: error.message,
      status: error.response?.status,
      data: error.response?.data,
      stack: error.stack
    });
    
    if (error.response?.status === 401) {
      throw new Error('Invalid API key or authentication error. Please check your Perplexity API key.');
    } else if (error.response?.status === 429) {
      throw new Error('Rate limit exceeded. Please try again later.');
    } else if (error.response?.data?.error) {
      throw new Error(`API Error: ${error.response.data.error}`);
    } else if (error.code === 'ECONNABORTED') {
      throw new Error('Request timed out. Please try again.');
    }
    
    throw new Error(`Failed to process recipe: ${error.message}`);
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

    console.log('Processing recipe for URL:', url);

    // Process the recipe using Perplexity API
    const recipe = await processRecipe(url);
    
    console.log('Successfully processed recipe');
    res.status(200).json({ recipe });
  } catch (error) {
    console.error('Error in request handler:', {
      message: error.message,
      stack: error.stack
    });

    const statusCode = error.response?.status || 500;
    const errorMessage = error.message || 'Failed to process recipe';

    res.status(statusCode).json({ 
      error: errorMessage,
      details: process.env.NODE_ENV === 'development' ? error.stack : undefined
    });
  }
} 