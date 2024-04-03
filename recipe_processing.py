import pandas as pd

# Assume RAW_recipes and RAW_interactions are passed as arguments

def find_recipes_by_ingredients(ingredients, RAW_recipes):
    matching_recipes = RAW_recipes[RAW_recipes['ingredients'].apply(lambda ingredient_list: all(ingredient.lower() in ingredient_list.lower() for ingredient in ingredients))]
    return matching_recipes[['name', 'id']]

def count_and_rating(recipes, RAW_interactions):
    recipes['count'] = recipes['id'].apply(lambda x: RAW_interactions[RAW_interactions['recipe_id'] == x].shape[0])
    recipes['rating'] = recipes['id'].apply(lambda x: RAW_interactions[RAW_interactions['recipe_id'] == x]['rating'].mean())
    recipes_sorted = recipes[['name', 'count', 'rating']].sort_values(by=['count', 'rating'], ascending=[False, False]).head(10)
    recipes_sorted.columns = ['Recipe Name', 'Reviews (#)', 'Average Rating']
    return recipes_sorted
