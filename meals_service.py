import random
import re
import pandas as pd

NO_IMAGE_URL = 'https://placehold.co/600x400?text=No+Image'


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

def get_meal_image(txt):
    res = re.search(r"!\[[^\]]*\]\((.*?)\s*(\"(?:.*[^\"])\")?\s*\)", txt)
    if res != None:
        return res.group(1)
    else:
        return NO_IMAGE_URL

def get_meal_title(txt: str):
    res = ''
    try:
        i = txt.index('!')
        res = txt[:i]
    except:
        res = txt.splitlines()[0]
    
    return res.strip()

def get_meal_description(txt: str):
    res = ''
    try:
        i = txt.index('**ingredients:**')
        res = txt[i:]
    except:
        pass    
    return res
    
def get_random_meal(meal_list):
    l = len(meal_list)
    if l > 0:
        return meal_list[random.randrange(0, l)]