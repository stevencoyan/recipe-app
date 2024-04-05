import pandas as pd
import ast

# Load your CSV data into pandas DataFrames
RAW_recipes = pd.read_csv('RAW_recipes.csv')
RAW_interactions = pd.read_csv('RAW_interactions.csv')

# Assume RAW_recipes and RAW_interactions are passed as arguments

def find_recipes_by_ingredients(ingredients, RAW_recipes):
    matching_recipes = RAW_recipes[RAW_recipes['ingredients'].apply(lambda ingredient_list: all(ingredient.lower() in ingredient_list.lower() for ingredient in ingredients))]
    # make upper case the first letter of each word in the recipe name
    matching_recipes['name'] = matching_recipes['name'].apply(lambda x: x.title())
    return matching_recipes[['name', 'id']]

def count_and_rating(recipes, RAW_interactions):
    recipes.loc[:,'count'] = recipes['id'].apply(lambda x: RAW_interactions[RAW_interactions['recipe_id'] == x].shape[0])
    recipes['count'] = recipes['count'].astype(int)
    recipes.loc[:,'rating'] = recipes['id'].apply(lambda x: round(RAW_interactions[RAW_interactions['recipe_id'] == x]['rating'].mean(),2)) 
    recipes_sorted = recipes[['name', 'count', 'rating', 'id']].sort_values(by=['count', 'rating'], ascending=[False, False]).head(10)
    recipes_sorted.columns = ['Recipe Name', 'Reviews (#)', 'Average Rating', 'id']
    return recipes_sorted

def recipe_info(recipe_id):
    recipe = RAW_recipes[RAW_recipes['id'] == recipe_id]
    recipe_info = recipe[['name', 'minutes', 'n_steps', 'n_ingredients', 'description', 'ingredients', 'steps', 'nutrition']]
    recipe_info.columns = ['Recipe Name', 'Minutes', 'Number of Steps', 'Number of Ingredients', 'Description', 'Ingredients', 'Steps', 'Nutrition']
    
    # Convert the nutrition column from a string to a list
    recipe_info['Nutrition'] = recipe_info['Nutrition'].apply(ast.literal_eval)
    # create calories, fat and protein columns being the 0th, 1st and 5nd element of the nutrition list
    recipe_info['Calories'] = recipe_info['Nutrition'].apply(lambda x: x[0])
    recipe_info['Fat'] = recipe_info['Nutrition'].apply(lambda x: x[1])
    recipe_info['Protein'] = recipe_info['Nutrition'].apply(lambda x: x[5])

    return recipe_info


# Test the functions
#ingredients = ['hummus', 'pita', 'tomato']
#matching_recipes = find_recipes_by_ingredients(ingredients, RAW_recipes)
#print(matching_recipes)
#detailed_recipes = count_and_rating(matching_recipes, RAW_interactions)
#print(detailed_recipes)
#recipe_details = recipe_info(169389)
#print(recipe_details)

