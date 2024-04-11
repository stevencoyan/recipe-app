from flask import Flask, render_template, request
import pandas as pd
from recipe_processing import RecipeAnalyzer  # Ensure this module has the correct path or is in the same directory
from flask_caching import Cache

app = Flask(__name__)
# Configure cache, set up with simple cache type for ease of use and development
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

# Load recipe and review data into pandas DataFrames from CSV files
recipes = pd.read_csv('RAW_recipes.csv')
reviews = pd.read_csv('RAW_interactions.csv')

# Instantiate the RecipeAnalyzer with the loaded data
recipe_analyzer = RecipeAnalyzer(recipes, reviews)

@app.route('/', methods=['GET'])
@cache.cached(timeout=300)  # Cache the homepage for 5 minutes to improve load times
def home():
    """ Render the homepage template. """
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def search():
    """
    Process the search form, find recipes based on user ingredient requests,
    display results in /results template, or return 404 if no matches found.
    """
    # Extract ingredients list from the form data, clean it, and convert to lower case
    ingredients = request.form['ingredients'].split(',')
    ingredients = [ingredient.strip().lower() for ingredient in ingredients if ingredient.strip()]

    # Redirect back to home with an error if no ingredients are provided
    if not ingredients:
        return render_template('index.html', error="Please enter at least one ingredient.")

    # Use the analyzer to find matching recipes based on ingredients
    matching_recipes = recipe_analyzer.find_recipes_by_ingredients(ingredients)
    
    # If there are matching recipes, calculate their review counts and ratings, then render results
    if not matching_recipes.empty:
        detailed_recipes = recipe_analyzer.count_and_rating(matching_recipes)
        return render_template('results.html', recipes=detailed_recipes.to_dict(orient='records'))
    else:
        return "No matching recipes found.", 404
    
@app.route('/recipe<int:recipe_id>', methods=['GET'])
def recipe(recipe_id):
    """
    Fetch detailed recipe information using the recipe ID and render the recipe detail page,
    or return an error message if the recipe ID is not found.
    """
    try:
        # Fetch detailed recipe info from the analyzer
        recipe_details = recipe_analyzer.recipe_info(recipe_id)
        recipe_details = recipe_details.to_dict(orient='records')[0]
        return render_template('recipe.html', recipe=recipe_details)
    except ValueError as e:
        return str(e), 404

if __name__ == '__main__':
    app.run(debug=True)