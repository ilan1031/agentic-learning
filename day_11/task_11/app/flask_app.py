from flask import Flask, request, jsonify
import sys
import os
import logging

# Add parent directory to path - FIXED LINE CONTINUATION
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.crew_setup import create_validation_crew

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/validate', methods=['POST'])
def validate_json():
    try:
        data = request.get_json()
        json_str = data.get('json_str', '')
        
        if not json_str:
            return jsonify({"error": "No JSON provided"}), 400
        
        logger.info("Starting JSON validation process")
        result = create_validation_crew(json_str)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/')
def health_check():
    return "JSON Validation Service is running"

if __name__ == '__main__':
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(host='0.0.0.0', port=port)