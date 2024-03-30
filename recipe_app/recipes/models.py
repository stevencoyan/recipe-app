from django.db import models

class User(models.Model):
    techniques = models.TextField()
    items = models.TextField()
    n_items = models.IntegerField()
    ratings = models.TextField()
    n_ratings = models.IntegerField()

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    minutes = models.IntegerField()
    contributor = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted = models.DateField()
    nutrition = models.TextField()
    n_steps = models.IntegerField()
    steps = models.TextField()
    description = models.TextField(null=True)
    n_ingredients = models.IntegerField()

class Ingredient(models.Model):
    name_tokens = models.TextField()

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

class Interaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    date = models.DateField()
    rating = models.IntegerField()
    review = models.TextField(null=True)
