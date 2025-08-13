from flask import Flask, request, jsonify
import os
import json
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
API_KEY = os.getenv("GEMINI_API_KEY")

# Try to import google.generativeai
genai = None
if API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=API_KEY)
        logger.info("Google Generative AI module loaded")
    except ImportError:
        logger.warning("Google Generative AI package not installed")
else:
    logger.warning("GEMINI_API_KEY not set. Using fallback responses.")

# Router prompt
ROUTER_PROMPT = """
You are a multi-agent orchestrator for a product recommendation system.

Your role:
1. Understand the user's product-related query.
2. Decide which agent should handle the request:
   - If the query mentions "current price", "today", "latest price", or "live price" → route to Web Research Agent.
   - If the query is about "specifications", "features", "compare", "differences" → route to RAG Agent.
   - If the query is about "best", "recommendation", "top", "under X price" → route to both RAG Agent and Web Research Agent, then summarize.
   - If unclear, route to LLM for a general response.

Output strictly as JSON:
{
  "route": "<agent_name>",  // one of: "web_research", "rag", "combined", "general"
  "reason": "<short reason for route>"
}

Rules:
- Use 'combined' if query needs both specs and live price.
- Be deterministic and concise in 'reason'.
- Do not answer the query here — only decide routing.
"""

# Summarization prompt
SUMMARY_PROMPT = """
You are a product recommendation expert. Your task is to summarize information from multiple sources:

Web Research Results:
{web_results}

Product Database Results:
{rag_products}

User Query:
{query}

Instructions:
1. Identify key information from web research (prices, reviews, availability)
2. Highlight relevant products from the database (specs, features)
3. Provide a concise recommendation summary
4. Include sources where applicable
5. Format response in Markdown

Important:
- Be objective and factual
- Highlight differences between products
- Mention price ranges if available
- Suggest the best option if appropriate
"""

@app.route("/route", methods=["POST"])
def route_query():
    """Route user query to appropriate agent"""
    try:
        query = request.json.get("query", "")
        logger.info("Routing query: %s", query)
        
        if not genai:
            # Fallback routing
            query_lower = query.lower()
            if any(kw in query_lower for kw in ["price", "live", "current", "today"]):
                return jsonify({"route": "web_research", "reason": "Price-related query"})
            elif any(kw in query_lower for kw in ["spec", "feature", "compare", "difference"]):
                return jsonify({"route": "rag", "reason": "Specs/compare query"})
            elif any(kw in query_lower for kw in ["best", "recommend", "top", "under"]):
                return jsonify({"route": "combined", "reason": "Recommendation query"})
            else:
                return jsonify({"route": "general", "reason": "General query"})
        
        # Format prompt
        full_prompt = ROUTER_PROMPT + f"\n\nUser Query: {query}"
        
        # Get response
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.0,
                response_mime_type="application/json"
            )
        )
        
        # Parse and return response
        try:
            result = json.loads(response.text)
            return jsonify(result)
        except:
            logger.warning("Failed to parse routing response: %s", response.text)
            return jsonify({"route": "general", "reason": "Response parsing failed"})
    
    except Exception as e:
        logger.error("Routing failed: %s", str(e))
        return jsonify({"route": "general", "reason": f"Error: {str(e)}"})

@app.route("/summarize", methods=["POST"])
def summarize():
    """Summarize results from multiple sources"""
    try:
        data = request.json
        query = data.get("query", "")
        web_results = data.get("web_results", [])
        rag_products = data.get("rag_products", [])
        
        logger.info("Summarizing results for: %s", query)
        
        if not genai:
            # Fallback summary
            product_names = ", ".join([p.get("name", "product") for p in rag_products[:3]])
            return jsonify({
                "summary": f"Based on your query '{query}', I recommend: {product_names}. " 
                           "For more details, please check online retailers."
            })
        
        # Format prompt
        full_prompt = SUMMARY_PROMPT.format(
            web_results=json.dumps(web_results, indent=2),
            rag_products=json.dumps(rag_products, indent=2),
            query=query
        )
        
        # Get response
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(full_prompt)
        return jsonify({"summary": response.text})
    
    except Exception as e:
        logger.error("Summarization failed: %s", str(e))
        return jsonify({"summary": f"Could not generate summary: {str(e)}"})

@app.route("/general", methods=["POST"])
def general_response():
    """Handle general queries"""
    try:
        query = request.json.get("query", "")
        logger.info("General query: %s", query)
        
        if not genai:
            return jsonify({
                "response": f"I received your query: '{query}'. " 
                            "This is a fallback response as Gemini is not configured."
            })
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(query)
        return jsonify({"response": response.text})
    except Exception as e:
        logger.error("General response failed: %s", str(e))
        return jsonify({"response": f"Could not process query: {str(e)}"})

@app.route("/")
def health_check():
    return "LLM Service is running"

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    logger.info("Starting LLM service on port %d", port)
    app.run(host="0.0.0.0", port=port)