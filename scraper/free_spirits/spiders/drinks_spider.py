from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from bs4 import BeautifulSoup
from free_spirits.items import DrinkItem
from common import *

import re


class DrinkSpider(CrawlSpider):
    """
    the DrinkSpider
    """

    name = "drinks"
    allowed_domains = ["drinksmixer.com"]

    start_urls = [
        "http://www.drinksmixer.com/cat/1/%d" % p for p in xrange(1, 125)
    ]

    rules = (
        Rule(LinkExtractor(allow='http://www\.drinksmixer\.com/.*\.html'),
             callback='parse_drink'),
    )

    def parse_drink(self, response):
        """
        parsing the drinks
        note that this function has no notion of what the drink is (cocktail, shot)
        """

        drink = DrinkItem()
        soup = BeautifulSoup(response.body, "lxml")

        title       = soup.find("title").contents[0].rstrip("recipe")
        recipe      = soup.find("div", {"class": "RecipeDirections instructions"})
        description = soup.find("div", {"class": "summary RecipeDirections"})
        ingredients = soup.find("div", {"class": "ingredients"})

        drink['ingredients'] = {}

        if ingredients:
            for ingredient in ingredients.find_all("span", {"class": "ingredient"}):
                if ingredient.contents:
                    value = ingredient.find("span", {"class": "amount"}).contents[0]
                    key = ingredient.find("span", {"class": "name"})
                    key = key.find("a")
                    key = key['href']
                    key = re.findall(r'\d+', key)[0]

                    drink['ingredients'][key] = value

        drink['name']        = title.rstrip()
        drink['recipe']      = recipe.contents[0].rstrip() if recipe else ""
        drink['description'] = description.contents[0].rstrip() if description else ""

        return drink
