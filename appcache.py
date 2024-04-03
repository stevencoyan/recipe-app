from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
from flask_caching import Cache
from recipe_processing import find_recipes_by_ingredients, count_and_rating

app = Flask(__name__)
# Configure caching
app.config['CACHE_TYPE'] = 'SimpleCache'  # There are other backends available as well.
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache for 5 minutes (300 seconds)

cache = Cache(app)

# Load your CSV data into pandas DataFrames
RAW_recipes = pd.read_csv('RAW_recipes.csv')
RAW_interactions = pd.read_csv('RAW_interactions.csv')

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
@cache.cached(timeout=50, query_string=True)  # Cache this page
def search():
    ingredients = request.form['ingredients'].split(',')
    # Clean the ingredients list from whitespace
    ingredients = [ingredient.strip() for ingredient in ingredients]
    # Create a cache key based on ingredients
    cache_key = 'results:' + ','.join(sorted(ingredients))
    cached_results = cache.get(cache_key)
    if cached_results:
        return render_template('results.html', recipes=cached_results)
    
    matching_recipes = find_recipes_by_ingredients(ingredients, RAW_recipes)
    if not matching_recipes.empty:
        detailed_recipes = count_and_rating(matching_recipes, RAW_interactions)
        # Convert to dict for caching purposes
        detailed_recipes_dict = detailed_recipes.to_dict(orient='records')
        cache.set(cache_key, detailed_recipes_dict, timeout=300)  # Cache the result
        return render_template('results.html', recipes=detailed_recipes_dict)
    else:
        return "No matching recipes found.", 404

if __name__ == '__main__':
    app.run(debug=True)
