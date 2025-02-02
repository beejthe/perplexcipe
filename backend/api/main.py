from flask import Flask, request, jsonify
from flask_cors import CORS
import httpx
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# For Vercel serverless deployment
app.debug = False

@app.route('/')
def home():
    return jsonify({"status": "healthy"})

@app.route('/api/test')
def test_api():
    try:
        PERPLEXITY_API_KEY = os.getenv("PERPLEXCIPE_PERPLEXITY_API_KEY")
        if not PERPLEXITY_API_KEY:
            return jsonify({"error": "API key not configured"}), 500

        logger.info("Testing Perplexity API connection...")
        
        # Simple test query
        response = httpx.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                "Content-Type": "application/json",
                "accept": "application/json"
            },
            json={
                "model": "sonar-medium-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant. Please respond with 'API is working correctly.'"
                    },
                    {
                        "role": "user",
                        "content": "Hello, this is a test message."
                    }
                ]
            },
            timeout=30.0
        )
        
        logger.info(f"API Response Status: {response.status_code}")
        logger.info(f"API Response: {response.text}")

        if response.status_code != 200:
            return jsonify({
                "error": "API Error",
                "status_code": response.status_code,
                "response": response.text
            }), response.status_code

        result = response.json()
        return jsonify({
            "status": "success",
            "response": result
        })

    except Exception as e:
        logger.error(f"Error testing API: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/test-perplexity')
def test_perplexity():
    try:
        PERPLEXITY_API_KEY = os.getenv("PERPLEXCIPE_PERPLEXITY_API_KEY")
        if not PERPLEXITY_API_KEY:
            logger.error("API key not found in environment variables")
            return jsonify({"error": "API key not configured"}), 500
            
        logger.info(f"Testing with API key starting with: {PERPLEXITY_API_KEY[:10]}...")
        
        # Log the full request we're about to make
        request_data = {
            "url": "https://api.perplexity.ai/chat/completions",
            "headers": {
                "Authorization": f"Bearer {PERPLEXITY_API_KEY[:10]}...",
                "Content-Type": "application/json",
                "accept": "application/json"
            },
            "json": {
                "model": "sonar-medium-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a test assistant."
                    },
                    {
                        "role": "user",
                        "content": "Say hello"
                    }
                ]
            }
        }
        logger.info(f"Making request with data: {request_data}")
        
        try:
            response = httpx.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                    "Content-Type": "application/json",
                    "accept": "application/json"
                },
                json={
                    "model": "sonar-medium-chat",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a test assistant."
                        },
                        {
                            "role": "user",
                            "content": "Say hello"
                        }
                    ]
                },
                timeout=10.0
            )
            
            logger.info(f"Test Response Status: {response.status_code}")
            logger.info(f"Test Response Headers: {dict(response.headers)}")
            logger.info(f"Test Response Text: {response.text}")
            
            try:
                response_json = response.json()
                logger.info(f"Test Response JSON: {response_json}")
            except Exception as e:
                logger.error(f"Failed to parse response as JSON: {str(e)}")
                response_json = None
            
            if response.status_code == 200:
                return jsonify({"status": "success", "message": "API connection working", "response": response_json}), 200
            else:
                error_response = response_json if response_json else response.text
                logger.error(f"API Error: Status {response.status_code}, Response: {error_response}")
                return jsonify({"status": "error", "message": error_response}), response.status_code
                
        except httpx.RequestError as e:
            logger.error(f"HTTP Request Error: {str(e)}")
            return jsonify({"error": f"Failed to connect to Perplexity API: {str(e)}"}), 500
        except Exception as e:
            logger.error(f"API Call Error: {str(e)}")
            logger.exception("Full API call traceback:")
            return jsonify({"error": f"Error calling Perplexity API: {str(e)}"}), 500
            
    except Exception as e:
        logger.error(f"Test Error: {str(e)}")
        logger.exception("Full traceback:")
        return jsonify({"error": str(e)}), 500

@app.route('/api/recipe', methods=['POST'])
def process_recipe():
    try:
        data = request.get_json()
        logger.info(f"Received request data: {data}")
        
        if not data or 'url' not in data:
            logger.error("Missing URL in request")
            return jsonify({"error": "URL is required"}), 400

        PERPLEXITY_API_KEY = os.getenv("PERPLEXCIPE_PERPLEXITY_API_KEY")
        logger.info(f"API Key exists: {bool(PERPLEXITY_API_KEY)}")
        logger.info(f"API Key prefix: {PERPLEXITY_API_KEY[:7] if PERPLEXITY_API_KEY else 'None'}")
        
        if not PERPLEXITY_API_KEY:
            logger.error("API key not configured")
            return jsonify({"error": "API key not configured"}), 500

        logger.info(f"Processing recipe URL: {data['url']}")

        # Call Perplexity API
        try:
            headers = {
                "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                "Content-Type": "application/json",
                "accept": "application/json"
            }
            logger.info(f"Request headers: {headers}")
            
            response = httpx.post(
                "https://api.perplexity.ai/chat/completions",
                headers=headers,
                json={
                    "model": "sonar-medium-chat",
                    "messages": [
                        {
                            "role": "system",
                            "content": """You are a helpful cooking assistant. When given a recipe URL, first determine if there is a valid recipe on the page. A valid recipe must have both ingredients and cooking instructions.

If there is NO valid recipe on the page, respond with exactly this error message:
"NO_VALID_RECIPE: Unable to find a valid recipe on this page. Please ensure the URL points to a page containing a complete recipe with ingredients and instructions."

If there IS a valid recipe, extract and organize the key components in this beautiful format:

[Recipe Title in Title Case]

**Ingredients**

For the [First Component]:
• [ingredient with precise measurement, capitalize ingredient names]

• [ingredient with precise measurement, capitalize ingredient names]

• [ingredient with precise measurement, capitalize ingredient names]

For the [Second Component]:
• [ingredient with precise measurement, capitalize ingredient names]

• [ingredient with precise measurement, capitalize ingredient names]

• [ingredient with precise measurement, capitalize ingredient names]

**Instructions**

1. [Start with action verb] [rest of the instruction as a clear, complete sentence]

2. [Start with action verb] [rest of the instruction as a clear, complete sentence]

3. [Start with action verb] [rest of the instruction as a clear, complete sentence]

[For steps with sub-steps, format like this:]
4. [Main step title with action verb]:
   • [Sub-step starting with action verb]
   • [Sub-step starting with action verb]
   • [Sub-step starting with action verb]

5. [Main step title with action verb]:
   • [Sub-step starting with action verb]
   • [Sub-step starting with action verb]

**Key Tips**
• [Concise, helpful tip starting with action verb]

• [Concise, helpful tip starting with action verb]

• [Concise, helpful tip starting with action verb]

Important formatting rules:
1. Format section headings ('Ingredients', 'Instructions', 'Key Tips') in bold using **text**
2. Use consistent bullet points (•) for all ingredients and sub-steps
3. Write measurements in full (e.g., 'tablespoon' not 'tbsp')
4. Each ingredient MUST be on its own line with a blank line between ingredients
5. Instruction numbers MUST be on the same line as their text (inline)
6. Sub-steps should be indented with exactly three spaces before the bullet point
7. Leave exactly one blank line before each major section heading
8. Start each instruction and tip with an action verb
9. Capitalize ingredient names and proper nouns
10. Use consistent punctuation throughout
11. Keep instructions clear and direct
12. Format measurements consistently (e.g., '1 tablespoon' not 'one tablespoon')
13. Use parallel structure in all lists and steps
14. CRITICAL: Keep ingredients on separate lines with blank lines between them, but instruction numbers inline with text"""
                        },
                        {
                            "role": "user",
                            "content": f"Please extract the important parts of the recipe from this URL: {data['url']}"
                        }
                    ]
                },
                timeout=30.0
            )
            
            logger.info(f"API Response Status: {response.status_code}")
            logger.info(f"API Response Headers: {dict(response.headers)}")
            
            if response.status_code != 200:
                error_response = response.json() if response.text else "No error details available"
                logger.error(f"Perplexity API Error: Status {response.status_code}, Response: {error_response}")
                return jsonify({
                    "error": f"Error from Perplexity API (Status {response.status_code})",
                    "details": error_response
                }), response.status_code

            result = response.json()
            logger.info("Successfully received API response")
            content = result["choices"][0]["message"]["content"]
            
            # Check if the response indicates no valid recipe was found
            if content.startswith("NO_VALID_RECIPE:"):
                return jsonify({"error": content[15:].strip()}), 400
                
            return jsonify({
                "recipe": content
            })

        except httpx.RequestError as e:
            logger.error(f"HTTP Request Error: {str(e)}")
            return jsonify({"error": f"Failed to connect to Perplexity API: {str(e)}"}), 500
        except Exception as e:
            logger.error(f"API Call Error: {str(e)}")
            return jsonify({"error": f"Error calling Perplexity API: {str(e)}"}), 500

    except Exception as e:
        logger.error(f"General Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/debug')
def debug_config():
    try:
        api_key = os.getenv("PERPLEXCIPE_PERPLEXITY_API_KEY")
        return jsonify({
            "api_key_exists": bool(api_key),
            "api_key_length": len(api_key) if api_key else 0,
            "api_key_prefix": api_key[:7] + "..." if api_key else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# For Vercel deployment
if __name__ == '__main__':
    app.run() 