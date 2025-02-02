export const config = {
  runtime: 'edge'
};

export default async function handler(request) {
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
    
    return new Response(
      JSON.stringify(response_data),
      {
        status: 200,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        }
      }
    );
  } catch (e) {
    return new Response(
      JSON.stringify({ error: e.message }),
      {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        }
      }
    );
  }
} 