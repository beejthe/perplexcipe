const axios = require('axios');
const cheerio = require('cheerio');

async function scrapeRecipe(url) {
  try {
    const response = await axios.get(url);
    const $ = cheerio.load(response.data);
    
    // Extract ingredients
    const ingredients = [];
    $('.recipe-ingredients__list li').each((i, el) => {
      const text = $(el).text().trim();
      if (text) ingredients.push(text);
    });

    // Extract instructions
    const instructions = [];
    $('.recipe-directions__list li').each((i, el) => {
      const text = $(el).text().trim();
      if (text) instructions.push(text);
    });

    // If we couldn't find ingredients/instructions with specific classes,
    // try some common selectors
    if (ingredients.length === 0) {
      $('ul li').each((i, el) => {
        const text = $(el).text().trim();
        if (text.match(/^[\d½¼¾⅓⅔⅛⅜⅝⅞]|cup|tablespoon|teaspoon|pound|ounce|oz|lb|gram|g|ml|piece|slice/i)) {
          ingredients.push(text);
        }
      });
    }

    if (instructions.length === 0) {
      $('ol li').each((i, el) => {
        const text = $(el).text().trim();
        if (text.length > 10) {  // Basic filter for instruction-like content
          instructions.push(text);
        }
      });
    }

    // Get recipe title
    const title = $('h1').first().text().trim() || 'Recipe';

    // Format the response in markdown
    const markdown = `# ${title}\n\n` +
                    '## Ingredients\n' +
                    ingredients.map(i => `- ${i}`).join('\n') + '\n\n' +
                    '## Instructions\n' +
                    instructions.map((i, idx) => `${idx + 1}. ${i}`).join('\n');

    return markdown;
  } catch (error) {
    console.error('Error scraping recipe:', error);
    throw new Error('Failed to scrape recipe from the provided URL');
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

    // Scrape and parse the recipe
    const recipe = await scrapeRecipe(url);
    
    res.status(200).json({ recipe });
  } catch (error) {
    console.error('Error processing request:', error);
    res.status(500).json({ 
      error: 'Failed to process recipe',
      details: error.message
    });
  }
} 