from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
from recipe_processing import find_recipes_by_ingredients, count_and_rating
from flask_caching import Cache

app = Flask(__name__)

# Load your CSV data into pandas DataFrames
RAW_recipes = pd.read_csv('RAW_recipes.csv')
RAW_interactions = pd.read_csv('RAW_interactions.csv')

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def search():
    ingredients = request.form['ingredients'].split(',')
    # Clean the ingredients list from whitespace
    ingredients = [ingredient.strip() for ingredient in ingredients]
    matching_recipes = find_recipes_by_ingredients(ingredients, RAW_recipes)
    if not matching_recipes.empty:
        detailed_recipes = count_and_rating(matching_recipes, RAW_interactions)
        # Pass the recipes to a new template for display
        return render_template('results.html', recipes=detailed_recipes.to_dict(orient='records'))
    else:
        return "No matching recipes found.", 404

if __name__ == '__main__':
    app.run(debug=True)
