from flask import Flask, request, jsonify
from flask_cors import CORS
import httpx
import os
from dotenv import load_dotenv
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
logger.info("Environment variables loaded")

app = Flask(__name__)
CORS(app)

# For Replit deployment
app.debug = False

@app.route('/')
def home():
    logger.info("Home endpoint called")
    return jsonify({"status": "healthy", "message": "API is running"})

@app.route('/api')
def api_root():
    logger.info("API root endpoint called")
    return jsonify({
        "status": "healthy",
        "message": "API is running",
        "endpoints": [
            "/api/debug",
            "/api/recipe",
            "/api/test",
            "/api/test-perplexity"
        ]
    })

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
                "model": "sonar-pro",
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
                "model": "sonar-pro",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a test assistant. Please respond with a simple 'Hello! The API is working correctly.' message."
                    },
                    {
                        "role": "user",
                        "content": "Test the API connection"
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
                    "model": "sonar-pro",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a test assistant. Please respond with a simple 'Hello! The API is working correctly.' message."
                        },
                        {
                            "role": "user",
                            "content": "Test the API connection"
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
            
            response = httpx.post(
                "https://api.perplexity.ai/chat/completions",
                headers=headers,
                json={
                    "model": "sonar-pro",
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

• [Concise, helpful tip starting with action verb]"""
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
        logger.error(f"Request Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/debug')
def debug_config():
    logger.info("Debug endpoint called")
    try:
        api_key = os.getenv("PERPLEXCIPE_PERPLEXITY_API_KEY")
        logger.info(f"API key exists: {bool(api_key)}")
        
        env_vars = dict(os.environ)
        filtered_vars = {k: v[:10] + "..." for k, v in env_vars.items() if 'PERPLEXITY' in k or 'API' in k}
        logger.info(f"Found environment variables: {list(filtered_vars.keys())}")
        
        response_data = {
            "api_key_exists": bool(api_key),
            "api_key_length": len(api_key) if api_key else 0,
            "api_key_prefix": api_key[:7] + "..." if api_key else None,
            "relevant_env_vars": filtered_vars,
            "cwd": os.getcwd(),
            "env_file_exists": os.path.exists(".env")
        }
        logger.info(f"Returning debug response: {response_data}")
        return jsonify(response_data)
    except Exception as e:
        logger.error(f"Debug Error: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Listen on all available interfaces for Replit
    app.run(host='0.0.0.0', port=port) 