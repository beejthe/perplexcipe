from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecipeUrl(BaseModel):
    url: str

@app.get("/")
async def read_root():
    return {"status": "healthy"}

@app.post("/api/recipe")
async def process_recipe(recipe_url: RecipeUrl):
    try:
        PERPLEXITY_API_KEY = os.getenv("PERPLEXCIPE_PERPLEXITY_API_KEY")
        if not PERPLEXITY_API_KEY:
            raise HTTPException(status_code=500, detail="API key not configured")

        # Prepare the prompt
        prompt = f"""take a look at this website: {recipe_url.url}

you are tasked with extracting only the important parts of the recipe or recipes and providing me explicit instructions."""

        # Call Perplexity API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "sonar-medium-online",
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                },
                timeout=30.0
            )

            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Error from Perplexity API")

            result = response.json()
            return {
                "recipe": result["choices"][0]["message"]["content"]
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 