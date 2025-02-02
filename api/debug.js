export const config = {
  runtime: 'edge',
  regions: ['iad1']
};

export default function handler(request) {
  return new Response(
    JSON.stringify({ message: 'Debug endpoint is working' }),
    {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    }
  );
} 