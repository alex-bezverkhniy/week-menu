"""
A sample Hello World server.
"""
import datetime
import os
import pickle
import logging
import pandas as pd
import json

from flask import Flask, render_template, request, jsonify
from flaskext.markdown import Markdown


DATA_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTl9ZmUxoD6z1PT9YgehwKVg2V6shIwLiHoB0L1ak1eA-7lidZ8wiigziQIMfGKXl2twqarK5OaYPqZ/pub?gid=720294345&single=true&output=csv'
env = os.environ.get('ENV', 'PROD')
CACHE_FILENAME = './menu.pickle'

menuData= []

# pylint: disable=C0103
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["JSONIFY_MIMETYPE"] = "application/json; charset=utf-8"
Markdown(app)

### Handlers

@app.route('/', methods=['GET'])
def menu():
    global menuData
    """Return menu for a week"""
    menuData = getMenu()
    
    if 'Content-Type' in request.headers and request.headers['Content-Type'].startswith("application/json"):
        app.logger.debug(menuData)
        return menuData
    else:
        return render_template('index.html', current_weekday=(datetime.datetime.today().weekday()), debug=(env == 'DEV'), menu=menuData, week_days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    

@app.route('/dish/<dishType>/<query>', methods=['GET'])
def dish(dishType, query):
    """Return dish description for a week"""
    menuData = getMenu()

    dishData = ""
    for dish in menuData[dishType]:
        print(dish)
        if dish.startswith(query):
            dishData = dish
            break
    
    if 'Content-Type' in request.headers and request.headers['Content-Type'].startswith("application/json"):
        app.logger.debug(dishData)
        return dishData
    else:
        return render_template('dish.html', dishType=dishType, dishData=dishData, debug=(env == 'DEV'))

    

@app.route('/menu', methods=['PATCH'])
def flashMenuHandler():
    """Flash the cache with new data from Google Sheets"""
    flashMenu()
    return ('', 204)

#### Service funcs

def getMenu():
    global menuData
    if len(menuData) == 0:    
        try:
            if os.path.isfile(CACHE_FILENAME):
                with open(CACHE_FILENAME, 'rb') as cache:
                    menuData = pickle.load(cache)            
            else:
                menuData = flashMenu()
        except :
            app.logger.WARN('Cannot unpickle cache.')        
            menuData = genMenu(DATA_URL)
    
    return menuData

def flashMenu():
    global menuData
    app.logger.info('Flash the cache with new data from the remote host')
    menuData = genMenu(DATA_URL)
    with open(CACHE_FILENAME, 'wb') as cache:
        pickle.dump(menu, cache, protocol=pickle.HIGHEST_PROTOCOL)        
    return menuData


def importMenu(url):
    df = pd.read_csv(url)
    return df

def shuffleWeekMenu(df, type):
  breakfast_ser = df[type][df[type].notna()]
  return breakfast_ser.sample(frac=1).to_list()[0:7]

def genMenu(url):
    app.logger.info('Loads menu from the remote host')
    df = importMenu(url)
    breakfast_list = shuffleWeekMenu(df, 'breakfast')
    lunch_list = shuffleWeekMenu(df, 'lunch')
    dinner_list = shuffleWeekMenu(df, 'dinner')
    snacks_list = shuffleWeekMenu(df, 'snacks')
    return {'breakfast':breakfast_list,  'lunch': lunch_list, 'dinner':dinner_list, 'snacks':snacks_list}

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=(env == 'DEV'), port=server_port, host='0.0.0.0')
