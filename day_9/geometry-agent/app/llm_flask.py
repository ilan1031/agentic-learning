from flask import Flask, request, jsonify
import os
import json
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
API_KEY = os.getenv("GEMINI_API_KEY", "")

# Try to import google.generativeai with fallback
try:
    import google.generativeai as genai
    if API_KEY:
        genai.configure(api_key=API_KEY)
    GENAI_AVAILABLE = True
    logger.info("Google Generative AI module loaded successfully.")
except ImportError:
    GENAI_AVAILABLE = False
    logger.warning("Google Generative AI module not available. Using fallback mode.")

def extract_numbers(text):
    """Extract numbers from text with units"""
    numbers = re.findall(r"(\d+\.?\d*)", text)
    return [float(num) for num in numbers] if numbers else []

@app.route("/")
def home():
    return "LLM Service is running"

@app.route("/llm", methods=["POST"])
def llm_endpoint():
    try:
        payload = request.json or {}
        query = payload.get("query", "")
        
        logger.info(f"Received query: {query}")
        
        # Create prompt with strict instructions
        prompt = f"""
        You are an AI assistant that classifies queries and responds in JSON format.
        
        Instructions:
        1. If the query is about geometry (circle area, rectangle perimeter, cube volume, triangle area):
           - Respond ONLY with JSON: {{"tool_call": "<tool_name>", "args": {{...}}, "explain": "<explanation>"}}
        2. For non-geometry queries:
           - Respond ONLY with JSON: {{"tool_call": null, "response": "<your_answer>"}}
        
        Important rules:
        - Always output valid JSON
        - For geometry queries, extract exact numbers from the query
        - Never add extra text outside the JSON
        - If unsure, treat as non-geometry query
        
        Query: {query}
        """
        
        if GENAI_AVAILABLE and API_KEY:
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.0,
                        response_mime_type="application/json"
                    )
                )
                
                # Try to parse as JSON
                try:
                    response_data = json.loads(response.text)
                    logger.info(f"Gemini response: {response_data}")
                    return jsonify(response_data)
                except json.JSONDecodeError:
                    logger.warning(f"Failed to parse Gemini response: {response.text}")
                    # Fallback to simple response
                    return jsonify({
                        "tool_call": None, 
                        "response": response.text
                    })
            except Exception as e:
                logger.error(f"Gemini API error: {str(e)}")
                # Fallback to simple response
                return jsonify({
                    "tool_call": None, 
                    "response": f"Gemini API error: {str(e)}"
                })
        else:
            logger.info("Gemini not available, using fallback")
            # Fallback for testing
            numbers = extract_numbers(query)
            if "circle" in query.lower() and numbers:
                return jsonify({
                    "tool_call": "circle_area",
                    "args": {"radius": numbers[0]},
                    "explain": "Detected circle area query (fallback)"
                })
            elif "rectangle" in query.lower() and len(numbers) >= 2:
                return jsonify({
                    "tool_call": "rectangle_perimeter",
                    "args": {"length": numbers[0], "width": numbers[1]},
                    "explain": "Detected rectangle perimeter query (fallback)"
                })
            elif "cube" in query.lower() and numbers:
                return jsonify({
                    "tool_call": "cube_volume",
                    "args": {"side": numbers[0]},
                    "explain": "Detected cube volume query (fallback)"
                })
            elif "triangle" in query.lower() and len(numbers) >= 2:
                return jsonify({
                    "tool_call": "triangle_area",
                    "args": {"base": numbers[0], "height": numbers[1]},
                    "explain": "Detected triangle area query (fallback)"
                })
            else:
                return jsonify({
                    "tool_call": None,
                    "response": f"Test response for: {query} (Gemini not configured)"
                })
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            "error": str(e),
            "response": "An error occurred while processing your query."
        }), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    logger.info(f"Starting LLM service on port {port}")
    app.run(host="0.0.0.0", port=port)