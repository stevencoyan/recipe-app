import pandas as pd

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

# Example usage
ingredients = ['chicken', 'rice']
matching_recipes = find_recipes_by_ingredients(ingredients, RAW_recipes)
detailed_recipes = count_and_rating(matching_recipes, RAW_interactions)
print(detailed_recipes)
