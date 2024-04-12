# This is a new header
import pandas as pd
import ast
from typing import List
import warnings
warnings.filterwarnings("ignore") # Ignore warnings for cleaner output, remove if needed

class RecipeAnalyzer:
    """
    A class used to analyze recipes and user reviews.
    
    Attributes:
        recipes_df (pd.DataFrame): DataFrame containing recipe data.
        reviews_df (pd.DataFrame): DataFrame containing user review data.
        review_summary (pd.DataFrame): Precomputed summary of average rating and review count for each recipe.
    """
    
    def __init__(self, recipes_df: pd.DataFrame, reviews_df: pd.DataFrame):
        """
        Initializes the RecipeAnalyzer with the recipe and review data.
        
        Args:
            recipes_df (pd.DataFrame): The recipes dataset with recipes, description, etc.
            reviews_df (pd.DataFrame): The review dataset with recipe ratings and reviews.
        """
        self.recipes_df = recipes_df
        self.reviews_df = reviews_df
        self.review_summary = self.precompute_review_summary()

    def precompute_review_summary(self) -> pd.DataFrame:
        """
        Precomputes the average rating and review count for each recipe.
        
        Returns:
            pd.DataFrame: DataFrame containing average rating and review count for each recipe.
        """
        review_summary = self.reviews_df.groupby('recipe_id')['rating'].agg(['mean', 'count']).reset_index()
        review_summary.columns = ['id', 'average_rating', 'review_count']
        return review_summary

    def find_recipes_by_ingredients(self, ingredients: List[str]) -> pd.DataFrame:
        """
        Finds recipes that include all specified ingredients.
        
        Args:
            ingredients (List[str]): A list of ingredients to search for.
        
        Returns:
            pd.DataFrame: DataFrame with recipes containing all the ingredients, displaying name and ID.
        """
        matching_recipes = self.recipes_df[self.recipes_df['ingredients'].apply(
            lambda ingredient_list: all(ingredient.lower() in ingredient_list.lower() for ingredient in ingredients))]
        matching_recipes['name'] = matching_recipes['name'].str.title()
        return matching_recipes[['name', 'id']]

    def count_and_rating(self, recipes: pd.DataFrame) -> pd.DataFrame:
        """
        Returns the top 10 most reviewed and highest rated recipes with the specified ingredients.
        
        Args:
            recipes (pd.DataFrame): DataFrame of recipes to augment with count and rating.
        
        Returns:
            pd.DataFrame: DataFrame containing top 10 recipes sorted by review count and average rating.
        """
        recipes = recipes.merge(self.review_summary, left_on='id', right_on='id', how='left')
        recipes['average_rating'] = recipes['average_rating'].fillna(0)
        top_recipes = recipes.sort_values(['review_count', 'average_rating'], ascending=False).head(10)
        top_recipes['average_rating'] = top_recipes['average_rating'].round(2)
        return top_recipes[['name', 'id', 'review_count', 'average_rating']]

    def recipe_info(self, recipe_id: int) -> pd.DataFrame:
        """
        Retrieves detailed information for a specified recipe by ID.
        
        Args:
            recipe_id (int): The ID of the recipe.
        
        Returns:
            pd.DataFrame: DataFrame containing detailed info about the recipe, including calculated nutrition facts.
        """
        recipe = self.recipes_df[self.recipes_df['id'] == recipe_id]
        if recipe.empty:
            raise ValueError("Recipe ID not found in dataset.")
        recipe_info = recipe[['name', 'minutes', 'n_steps', 'n_ingredients', 'description', 'ingredients', 'steps', 'nutrition']]
        recipe_info.columns = ['Recipe Name', 'Minutes', 'Number of Steps', 'Number of Ingredients', 'Description', 'Ingredients', 'Steps', 'Nutrition']
        # Convert the ingredients string representation of list to actual list
        recipe_info['Ingredients'] = recipe_info['Ingredients'].apply(ast.literal_eval)
        
        # Convert the nutrition string representation of list to actual list
        recipe_info['Nutrition'] = recipe_info['Nutrition'].apply(ast.literal_eval)
        
        # Extract calories, fat, and protein from the nutrition list
        recipe_info['Calories'] = recipe_info['Nutrition'].apply(lambda x: x[0])
        recipe_info['Fat'] = recipe_info['Nutrition'].apply(lambda x: x[1])
        recipe_info['Protein'] = recipe_info['Nutrition'].apply(lambda x: x[5])
        
        return recipe_info
    
# Load recipe and review data into pandas DataFrames from CSV files
# recipes = pd.read_csv('RAW_recipes.csv')
# reviews = pd.read_csv('RAW_interactions.csv')

# # Instantiate the RecipeAnalyzer with the loaded data
# recipe_analyzer = RecipeAnalyzer(recipes, reviews)

# # Test the RecipeAnalyzer class with a sample search
# ingredients = ['chicken', 'rice', 'soy sauce']
# matching_recipes = recipe_analyzer.find_recipes_by_ingredients(ingredients)
# detailed_recipes = recipe_analyzer.count_and_rating(matching_recipes)
# info = recipe_analyzer.recipe_info(detailed_recipes.iloc[0]['id'])// print(detailed_recipes)

# print(info.columns)




    
