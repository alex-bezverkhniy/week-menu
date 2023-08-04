import pandas as pd
import secrets
import random
import re

from nicegui import ui, app


URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTl9ZmUxoD6z1PT9YgehwKVg2V6shIwLiHoB0L1ak1eA-7lidZ8wiigziQIMfGKXl2twqarK5OaYPqZ/pub?gid=720294345&single=true&output=csv'


def load_menu(url):
    df = pd.read_csv(url)
    return df


def shuffle_week_menu(df, type):
    breakfast_ser = df[type][df[type].notna()]
    return breakfast_ser.sample(frac=1).to_list()[0:7]


def week_menu(df, type):
    meal_ser = df[type][df[type].notna()]
    return meal_ser.to_list()[0:7]


def load_week_menu(url, meal_type):
    df = load_menu(url)
    return week_menu(df, meal_type)


def gen_menu(url):
    df = load_menu(url)
    breakfast_list = shuffle_week_menu(df, 'breakfast')
    lunch_list = shuffle_week_menu(df, 'lunch')
    dinner_list = shuffle_week_menu(df, 'dinner')
    snacks_list = shuffle_week_menu(df, 'snacks')
    return {'breakfast': breakfast_list,  'lunch': lunch_list, 'dinner': dinner_list, 'snacks': snacks_list}


def get_random_meal(meal_list):
    l = len(meal_list)
    if l > 0:
        return meal_list[random.randrange(0, l)]


def get_meal_image(txt):
    res = re.search(r"!\[[^\]]*\]\((.*?)\s*(\"(?:.*[^\"])\")?\s*\)", txt)
    if res != None:
        return res.group(1)
    else:
        return 'https://placehold.co/600x400?text=No+Image'


def get_meal_title(txt: str):
    try:
        i = txt.index('!')
    except:
        i = 0
    return txt[:i]


def get_meal_description(txt: str):
    try:
        i = txt.index('**ingredients:**')
    except:
        i = 0
    return txt[i:]


# @ui.refreshable
def meal_card(meal: str, card: ui.refreshable):
    with ui.card().tight():
        title = get_meal_title(meal)
        image_url = get_meal_image(meal)
        desc = get_meal_description(meal)
        with ui.image(image_url).style('min-width: 20em; max-width: 35em; min-height: 20em; max-height: 35em;'):
            ui.label(title).classes(
                'absolute-bottom text-subtitle2 text-center')
        with ui.card_section():
            ui.markdown(desc)
        with ui.card_actions():
            ui.button(icon='refresh', on_click=card.refresh).props('flat color=blue')

@ui.refreshable
def breakfast_card():
    meals_list = app.storage.user.get('breakfast_list', [])
    meal = get_random_meal(meals_list)
    meal_card(meal, breakfast_card)

@ui.refreshable
def lunch_card():
    meals_list = app.storage.user.get('lunch_list', [])
    meal = get_random_meal(meals_list)
    meal_card(meal, lunch_card)

@ui.page('/')
def index():
    breakfast_list = load_week_menu(URL, 'breakfast')
    lunch_list = load_week_menu(URL, 'lunch')
    app.storage.user['breakfast_list'] = breakfast_list
    app.storage.user['lunch_list'] = lunch_list

    with ui.row():                
        breakfast_card()
        lunch_card()
    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
        ui.label('Week menu')
        ui.button(icon='refresh').props('flat color=white')
    # mean_card(breakfast_list[0])
    # mean_card(breakfast_list[1])
    # mean_card(breakfast_list[2])
    # mean_card(breakfast_list[3])
    # mean_card(breakfast_list[4])
    # mean_card(breakfast_list[5])
    # mean_card(breakfast_list[6])


ui.run(storage_secret=secrets.token_urlsafe(16))
