from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
from recipe_processing import find_recipes_by_ingredients, count_and_rating, recipe_info
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
    # Remove any empty strings from the list
    ingredients = [ingredient for ingredient in ingredients if ingredient]
    if not ingredients:
        return render_template('index.html', error="Please enter at least one ingredient.")
    matching_recipes = find_recipes_by_ingredients(ingredients, RAW_recipes)
    if not matching_recipes.empty:
        detailed_recipes = count_and_rating(matching_recipes, RAW_interactions)
        # Pass the recipes to a new template for display
        return render_template('results.html', recipes=detailed_recipes.to_dict(orient='records'))
    else:
        return "No matching recipes found.", 404
    
@app.route('/recipe<int:recipe_id>', methods=['GET'])
def recipe(recipe_id):
    # Call the recipe_info function to get the recipe details
    recipe_details = recipe_info(recipe_id)
    # Pass the recipe details to a new template for display dict
    recipe_details = recipe_details.to_dict(orient='records')[0]


    return render_template('recipe.html', recipe=recipe_details)


if __name__ == '__main__':
    app.run(debug=True)
