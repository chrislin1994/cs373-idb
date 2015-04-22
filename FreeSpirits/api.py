# -*- coding: utf-8 -*-

import subprocess
import os

from . import app
from .models import *

from flask import jsonify
from flask.ext import restful

api = restful.Api(app)


class DrinkListing(restful.Resource):
    """
    the class that returns the entire listing of drinks
    these drinks are provided in name, id value pairs
    if it is necessary to know more about an individual drink,
    refer to the DrinkId class below
    """
    def get(self):
        drinks_name = Drink.query.values(Drink.name)
        drinks_id = Drink.query.values(Drink.id)
        drinks = {v[0]: k[0] for (k, v) in zip(drinks_name, drinks_id)}

        return jsonify(drinks)

api.add_resource(DrinkListing, '/api/drinks/')


class DrinkId(restful.Resource):
    """
    this is the class that queries an individual drink by id
    a drink will return all of it's associated fields in it
    plus the ingredients that the drink uses
    """

    def get(self, drink_id):
        drink = Drink.query.filter_by(id=drink_id)
        if drink.first():
            drink = drink.first()
            result = {
                "id": drink.id,
                "name": drink.name,
                "description": drink.description,
                "recipe": drink.recipe
            }

            quantities, ingredients = Drink.get_ingredients_by_id(drink_id)

            result["quantities"] = quantities
            result["ingredients"] = [x.name for x in ingredients]

            return jsonify(result)
        else:
            return "{}"

api.add_resource(DrinkId, '/api/drinks/<int:drink_id>')


class IngredientListing(restful.Resource):
    """
    This is the ingredients listing viewW
    This class is identical in design to the earlier DrinkListing
    """

    def get(self):
        ingredients_name = Ingredient.query.values(Ingredient.name)
        ingredients_id = Ingredient.query.values(Ingredient.id)
        ingredients = {v[0]: k[0] for (k, v) in
                       zip(ingredients_name, ingredients_id)}
        return jsonify(ingredients)

api.add_resource(IngredientListing, '/api/ingredients/')


class IngredientId(restful.Resource):
    """
    The endpoint to get an ingredient by id
    This returns all of the fields that the ingredient contains
    plus all the drinks that this ingredient is associated with
    """

    def get(self, ingredient_id):
        ingredient = Ingredient.query.filter_by(id=ingredient_id)
        if ingredient.first():
            ingredient = ingredient.first()
            result = {
                "id": ingredient.id,
                "name": ingredient.name,
                "description": ingredient.description,
                "calories": ingredient.calories,
                "energy": ingredient.energy,
                "fats": ingredient.fats,
                "carbohydrates": ingredient.carbohydrates,
                "protein": ingredient.protein,
                "fiber": ingredient.fiber,
                "sugars": ingredient.sugars,
                "cholesterol": ingredient.cholesterol,
                "sodium": ingredient.sodium,
                "alcohol": ingredient.alcohol
            }

            drinks = Ingredient.get_drinks_by_id(ingredient_id, -1)
            drinks = [x.name for x in drinks]
            result["drinks"] = drinks

            return jsonify(result)
        else:
            return "{}"

api.add_resource(IngredientId, '/api/ingredients/<int:ingredient_id>')


class UserListing(restful.Resource):
    """
    The endpoint that represents all the users in the database
    This is again similar to DrinkListing and IngredientListing
    You can create a user by sending a post request to this api
    With the correct inputs, name, email
    If these inputs are not provided, then
    """

    def get(self):
        users_email = User.query.values(User.email)
        users_id = User.query.values(User.id)
        users = {k[0]: v[0] for (k, v) in zip(users_email, users_id)}

        return jsonify(users)

api.add_resource(UserListing, '/api/users/')


class UserId(restful.Resource):
    """
    The endpoint to find a user by id in the database
    This returns all the associated fields of the user
    """

    def get(self, user_id):
        user = User.query.filter_by(id=user_id)
        if user.first():
            user = user.first()
            result = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email
            }

            return jsonify(result)
        else:
            return "{}"

api.add_resource(UserId, '/api/users/<int:user_id>')


class TestApi(restful.Resource):
    """
    The Test API
    this simply runs test.py as a subprocess and returns the output
    """

    def get(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        basedir = os.path.abspath(os.path.join(basedir, os.pardir))

        output = subprocess.check_output(['python', basedir + '/tests.py'],
                                         stderr=subprocess.STDOUT)
        output = output.decode("utf-8")
        output = output.strip()
        values = output.split("\n")

        passed_tests = values[0].count('.')
        failed_tests = values[0].count('E')
        time = values[2].find("in") + 2
        time = float(values[2][time:-1])

        result = {
            "success": failed_tests == 0,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "time": time,
            "output": output
        }

        return jsonify(result)

api.add_resource(TestApi, '/api/tests/')
