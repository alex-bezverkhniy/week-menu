import re

import requests

import constants
import csv
from dataclasses import dataclass

NO_IMAGE_URL = 'https://placehold.co/600x400?text=No+Image'


def get_content(url) -> requests.Response:
    return requests.get(url)


@dataclass
class Meal:
    title: str
    img_url: str = ''
    ingredients: str = ''


class DataAPI():
    def __init__(self, base_url: str = constants.BASE_URL):
        self.base_url = base_url

    def get_csv(self) -> str:
        resp = requests.get(self.base_url)
        if resp is not None and resp.ok and len(resp.content) > 0:
            content = resp.content.decode('utf-8')
            return str(content)
        else:
            raise Exception('No data found')

    def get_data(self) -> list[list[Meal]]:
        try:
            csv_data = self.get_csv()
            cr = csv.reader(csv_data.splitlines(), delimiter=',')
            table = list(cr)

            # collect meals
            breakfast_meals_list = [meal[0] for meal in table[1:] if len(meal[0]) > 0]
            lunch_meals_list = [meal[1] for meal in table[1:] if len(meal[1]) > 0]
            dinner_meals_list = [meal[2] for meal in table[1:] if len(meal[2]) > 0]
            snack_meals_list = [meal[3] for meal in table[1:] if len(meal[3]) > 0]

            breakfast_meals = self.parse_meals_list(breakfast_meals_list)
            lunch_meals = self.parse_meals_list(lunch_meals_list)
            dinner_meals = self.parse_meals_list(dinner_meals_list)
            snack_meals = self.parse_meals_list(snack_meals_list)

            return [breakfast_meals, lunch_meals, dinner_meals, snack_meals]
        except Exception as error:
            raise Exception('Cannot read csv') from error

    def parse_meals_list(self, breakfast_meals_list):
        breakfast_meals = list[Meal]()
        for m in breakfast_meals_list:
            meal = self.parse_meal(m)
            breakfast_meals.append(meal)
        return breakfast_meals

    def parse_meal(self, m) -> Meal:
        meal_title = self.get_meal_title(m)
        meal_img = self.get_meal_image(m)
        meal_ingredients = self.get_meal_ingredients(m)
        meal = Meal(title=meal_title, img_url=meal_img, ingredients=meal_ingredients)
        return meal

    def get_meal_title(self, txt: str):
        res = ''
        try:
            i = txt.index('!')
            res = txt[:i]
        except:
            res = txt.splitlines()[0]
        return res.strip()

    def get_meal_image(self, txt):
        res = re.search(r"!\[[^\]]*\]\((.*?)\s*(\"(?:.*[^\"])\")?\s*\)", txt)
        if res != None:
            return res.group(1)
        else:
            return NO_IMAGE_URL

    def get_meal_ingredients(self, txt: str):
        res = ''
        try:
            i = txt.index('**ingredients:**')
            res = txt[i:]
        except:
            pass
        return res
