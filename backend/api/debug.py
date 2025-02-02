from http.server import BaseHTTPRequestHandler
import json
import os

def handler(event, context):
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
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(response_data)
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": str(e)})
        } 