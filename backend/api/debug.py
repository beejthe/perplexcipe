from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os

app = FastAPI()

@app.get("/api/debug")
async def debug_config():
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
        
        return response_data
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        ) 