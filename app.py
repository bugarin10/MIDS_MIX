import sys

sys.path.append("00_code/")


from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField
from utils import return_image, retrieve_random_coktails, closest_vector
import os
import requests

# Flask setup
app = Flask(__name__)
app.config["SECRET_KEY"] = "1234"

# Access the environment variable for Hugging Face token
token = os.getenv("HUGGING_FACE_TOKEN_NEW")
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
HEADERS = {"Authorization": f"Bearer {token}"}


# Query function to Hugging Face model
def query(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()


# Form for selecting user type
class UserTypeForm(FlaskForm):
    user_type = HiddenField("User Type")
    submit_customer = SubmitField("I'm a Customer")
    submit_owner = SubmitField("I'm an Owner")


# Index route for selecting user type
@app.route("/", methods=["GET", "POST"])
def index():
    form = UserTypeForm()
    if form.validate_on_submit():
        user_type = form.user_type.data
        if user_type == "Rapid Fire":
            return redirect(url_for("customer"))
        elif user_type == "Survey":
            return redirect(url_for("owner"))
    return render_template("index.html", form=form)


# Route for customer page
@app.route("/Rapid Fire")
def customer():
    refresh = request.args.get("refresh", "false") == "true"
    id = request.args.get("id", None)
    if refresh and id is not None:

        vector = closest_vector(id)
        IDs = list(vector.keys())
    else:
        vector = retrieve_random_coktails()
        IDs = list(vector.keys())

    return render_template(
        "Customer.html",
        user_type="Rapid Fire",
        images_urls=return_image(base=None, random_retrieve=True),
        vector=vector,
        IDs=IDs,
    )


# Route for owner page
@app.route("/Survey")
def owner():
    return render_template("survey.html", user_type="Owner")


# Route for survey form submission
@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        base_liquor = request.form["baseLiquor"]
        strength = request.form["strength"]
        flavour = request.form["flavour"]
        additional_info = request.form["additionalInfoHidden"]

        # Constructing the prompt based on user's selections to generate the cocktail name
        prompt_name = f"Create a cocktail with the following characteristics:\n\n"
        prompt_name += f"Base Liquor: {base_liquor}\n"
        prompt_name += f"Strength: {strength}\n"
        prompt_name += f"Flavour: {flavour}\n"
        prompt_name += (
            f"Other ingredients and/or characteristics: {additional_info}\n\n"
        )
        prompt_name += "Generate a pre-existing or fancy name for a cocktail with these characteristics. Make sure to include the other ingredients and/or characteristics in the name."

        # Payload for query to Hugging Face model to generate the cocktail name
        payload_name = {"inputs": prompt_name}

        # Querying the model to generate the cocktail name
        try:
            response_text = query(payload_name)
            print("Response text (name): ", response_text)

            # Extracting the generated cocktail name
            cocktail_name = response_text[0].get("generated_text")

            # Constructing the prompt based on user's selections and the generated cocktail name to generate ingredients
            prompt_ingredients = f"Create a cocktail named {cocktail_name} with the following characteristics:\n\n"
            prompt_ingredients += f"Base Liquor: {base_liquor}\n"
            prompt_ingredients += f"Strength: {strength}\n"
            prompt_ingredients += f"Flavour: {flavour}\n"
            prompt_ingredients += (
                f"Other ingredients and/or characteristics: {additional_info}\n\n"
            )
            prompt_ingredients += "Generate a list of unique ingredients for a cocktail with these characteristics. Make sure to include the other ingredients and/or characteristics in the ingredients."

            # Payload for query to Hugging Face model to generate ingredients
            payload_ingredients = {"inputs": prompt_ingredients}

            # Querying the model to generate ingredients
            response_text = query(payload_ingredients)
            print("Response text (ingredients): ", response_text)

            # Extracting the generated ingredients
            ingredients = response_text[0].get("generated_text")

            print("Cocktail name: ", cocktail_name)
            print("Ingredients: ", ingredients)

            # Return the cocktail name and ingredients to the user
            return render_template(
                "results.html", cocktail_name=cocktail_name, ingredients=ingredients
            )
        except Exception as e:
            # Handle any errors that occur during the queries
            return f"An error occurred: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
