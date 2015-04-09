# -*- coding: utf-8 -*-

import subprocess
import os

from . import app
from .models import *

from flask import render_template
from flask import jsonify


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/builder')
def builder():
    return render_template("builder.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/drinks')
@app.route('/drinks/')
@app.route('/drinks/<drink_id>')
def drinks(drink_id=None):
    if drink_id is None:
        return render_template("drinks.html", drinks=Drink.query.order_by(Drink.name))
    if IngredientToDrink.query.filter_by(drink_id=drink_id).first() is None:
        return page_not_found(404)
    quantities = []
    ingredients = []
    for ingredient in IngredientToDrink.query.filter_by(drink_id=drink_id):
        quantities.append(ingredient.quantity)
        ingredients.append(Ingredient.query.filter_by(id=ingredient.ingredient_id).first())
    return render_template("drink.html", drink=Drink.query.filter_by(id=drink_id).first(), quantities=quantities, ingredients=ingredients)

@app.route('/ingredients')
@app.route('/ingredients/')
@app.route('/ingredients/<ingredient_id>')
def ingredients(ingredient_id=None):
    if ingredient_id is None:
        return render_template("ingredients.html", ingredients=Ingredient.query.order_by(Ingredient.name))
    ingredient_page = Ingredient.query.filter_by(id=ingredient_id).first()
    if ingredient_page is None:
        return page_not_found(404)
    return render_template("ingredient.html", ingredient=ingredient_page)

@app.route('/users')
@app.route('/users/')
@app.route('/users/<user_id>')
def users(user_id=None):
    if user_id is None:
        return render_template("users.html", users=User.query.order_by(User.name))
    user_page = User.query.filter_by(id=user_id).first()
    if user_page is None:
        return page_not_found(404)
    return render_template("user.html", user=user_page)

@app.route('/api/drinks')
@app.route('/api/drinks/')
@app.route('/api/drinks/<drink_id>')
def api_drinks(drink_id=None):
    if drink_id is None:
        drinks_name = Drink.query.values(Drink.name)
        drinks_id   = Drink.query.values(Drink.id)

        drinks_zip = zip(drinks_name, drinks_id)
        drinks = {k[0]: v[0] for (k, v) in drinks_zip}
        
        return jsonify(drinks)
    return None

@app.route('/api/ingredients')
@app.route('/api/ingredients/')
@app.route('/api/ingredients/<ingredient_id>')
def api_ingredients(ingredient_id=None):
    if ingredient_id is None:
        ingredients_name = Ingredient.query.values(Ingredient.name)
        ingredients_id   = Ingredient.query.values(Ingredient.id)

        ingredients_zip = zip(ingredients_name, ingredients_id)
        ingredients = {k[0]: v[0] for (k, v) in ingredients_zip}
        
        return jsonify(ingredients)
    return None

@app.route('/api/tests')
def api_tests():
    basedir = os.path.abspath(os.path.dirname(__file__))
    basedir = os.path.abspath(os.path.join(basedir, os.pardir))

    output = subprocess.check_output(['python', basedir + '/tests.py'], stderr=subprocess.STDOUT)

    return output

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
