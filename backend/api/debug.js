module.exports = (req, res) => {
  try {
    const api_key = process.env.PERPLEXCIPE_PERPLEXITY_API_KEY;
    const env_vars = process.env;
    const filtered_vars = Object.fromEntries(
      Object.entries(env_vars)
        .filter(([k, v]) => k.includes('PERPLEXITY') || k.includes('API'))
        .map(([k, v]) => [k, v.slice(0, 10) + '...'])
    );
    
    const response_data = {
      api_key_exists: Boolean(api_key),
      api_key_length: api_key ? api_key.length : 0,
      api_key_prefix: api_key ? api_key.slice(0, 7) + '...' : null,
      relevant_env_vars: filtered_vars,
      cwd: process.cwd(),
      env_file_exists: false // Not applicable in serverless environment
    };
    
    res.status(200).json(response_data);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
}; 