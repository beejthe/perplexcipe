from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            api_key = os.getenv("PERPLEXCIPE_PERPLEXITY_API_KEY")
            env_vars = dict(os.environ)
            filtered_vars = {k: v[:10] + "..." for k, v in env_vars.items() if 'PERPLEXITY' in k or 'API' in k}
            
            response_data = {
                "api_key_exists": bool(api_key),
                "api_key_length": len(api_key) if api_key else 0,
                "api_key_prefix": api_key[:7] + "..." if api_key else None,
                "relevant_env_vars": filtered_vars,
                "cwd": os.getcwd(),
                "env_file_exists": os.path.exists(".env")
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            error_response = {
                "error": str(e)
            }
            self.wfile.write(json.dumps(error_response).encode('utf-8')) 