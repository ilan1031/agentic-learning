from flask import Flask, request, jsonify
from recipe_crew import RecipeCrew
import os
from datetime import datetime
import re
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def save_recipe_markdown(recipe_text, ingredients):
    # Create recipes directory if it doesn't exist
    if not os.path.exists('recipes'):
        os.makedirs('recipes')
    
    # Generate a filename from the current timestamp and ingredients
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Clean the ingredients string for filename
    clean_ingredients = re.sub(r'[^a-zA-Z0-9 ]', '', ingredients).replace(' ', '_')[:20]
    filename = f"recipes/recipe_{timestamp}_{clean_ingredients}.md"
    
    with open(filename, 'w') as f:
        f.write(recipe_text)
    
    return filename

@app.route('/generate_recipe', methods=['POST'])
def generate_recipe():
    try:
        data = request.get_json()
        ingredients = data.get('ingredients', '')
        
        if not ingredients:
            return jsonify({'error': 'No ingredients provided'}), 400
        
        # Initialize and run the recipe crew
        recipe_crew = RecipeCrew()
        result = recipe_crew.run(ingredients)
        
        # Save the recipe to a markdown file
        filename = save_recipe_markdown(result, ingredients)
        
        return jsonify({
            'recipe': result,
            'saved_file': filename
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)