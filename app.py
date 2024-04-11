from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
from recipe_processing import RecipeAnalyzer
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

# Load your CSV data into pandas DataFrames
recipes = pd.read_csv('RAW_recipes.csv')
reviews = pd.read_csv('RAW_interactions.csv')

# Create an instance of RecipeAnalyzer
recipe_analyzer = RecipeAnalyzer(recipes, reviews)

@app.route('/', methods=['GET'])
@cache.cached(timeout=300)
def home():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def search():
    ingredients = request.form['ingredients'].split(',')
    ingredients = [ingredient.strip().lower() for ingredient in ingredients if ingredient.strip()]
    
    if not ingredients:
        return render_template('index.html', error="Please enter at least one ingredient.")
    
    matching_recipes = recipe_analyzer.find_recipes_by_ingredients(ingredients)
    if not matching_recipes.empty:
        detailed_recipes = recipe_analyzer.count_and_rating(matching_recipes)
        return render_template('results.html', recipes=detailed_recipes.to_dict(orient='records'))
    else:
        return "No matching recipes found.", 404
    
@app.route('/recipe<int:recipe_id>', methods=['GET'])
def recipe(recipe_id):
    try:
        recipe_details = recipe_analyzer.recipe_info(recipe_id)
        recipe_details = recipe_details.to_dict(orient='records')[0]
        return render_template('recipe.html', recipe=recipe_details)
    except ValueError as e:
        return str(e), 404

if __name__ == '__main__':
    app.run(debug=True)
