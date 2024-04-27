from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the environment variable
token = os.getenv("HUGGING_FACE_TOKEN_NEW")
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
HEADERS = {"Authorization": f"Bearer {token}"}

def query(payload):
	response = requests.post(API_URL, headers=HEADERS, json=payload)
	return response.json()

app = Flask(__name__)

# Getting information from the user for prompt engineering 
@app.route('/')
def index():
    return render_template('survey.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        base_liquor = request.form['baseLiquor']
        strength = request.form['strength']
        flavour = request.form['flavour']
        additional_info = request.form['additionalInfoHidden']
        print("Additional info: ", additional_info)
        
        # Constructing the prompt based on user's selections to generate the cocktail name
        prompt_name = f"Create a cocktail with the following characteristics:\n\n"
        prompt_name += f"Base Liquor: {base_liquor}\n"
        prompt_name += f"Strength: {strength}\n"
        prompt_name += f"Flavour: {flavour}\n"
        prompt_name += f"Other ingredients and/or characteristics: {additional_info}\n\n"
        prompt_name += "Generate a pre-existing or fancy name for a cocktail with these characteristics. Make sure to include other ingredients and/or characteristics."
        
        # Payload for query to Hugging Face model to generate the cocktail name
        payload_name = {"inputs": prompt_name}
        
        # Querying the model to generate the cocktail name
        try:
            response_text = query(payload_name)
            print("Response text (name): ", response_text)
            
            # Extracting the generated cocktail name
            cocktail_name = response_text[0].get('generated_text')
            
            # Constructing the prompt based on user's selections and the generated cocktail name to generate ingredients
            prompt_ingredients = f"Create a cocktail named {cocktail_name} with the following characteristics:\n\n"
            prompt_ingredients += f"Base Liquor: {base_liquor}\n"
            prompt_ingredients += f"Strength: {strength}\n"
            prompt_ingredients += f"Flavour: {flavour}\n"
            prompt_ingredients += f"Other ingredients and/or characteristics: {additional_info}\n\n"
            prompt_ingredients += "Generate a list of unique ingredients for a cocktail with these characteristics. Make sure to include other ingredients and/or characteristics."
            
            # Payload for query to Hugging Face model to generate ingredients
            payload_ingredients = {"inputs": prompt_ingredients}
            
            # Querying the model to generate ingredients
            response_text = query(payload_ingredients)
            print("Response text (ingredients): ", response_text)
            
            # Extracting the generated ingredients
            ingredients = response_text[0].get('generated_text')
            
            print("Cocktail name: ", cocktail_name)
            print("Ingredients: ", ingredients)
            
            # Return the cocktail name and ingredients to the user
            return render_template('results.html', cocktail_name=cocktail_name, ingredients=ingredients)
        except Exception as e:
            # Handle any errors that occur during the queries
            return f"An error occurred: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
