"""
A sample Hello World server.
"""
import os
import pickle
import logging
import pandas as pd

from flask import Flask, render_template

DATA_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTl9ZmUxoD6z1PT9YgehwKVg2V6shIwLiHoB0L1ak1eA-7lidZ8wiigziQIMfGKXl2twqarK5OaYPqZ/pub?gid=720294345&single=true&output=csv'
env = os.environ.get('ENV', 'PROD')
CACHE_FILENAME = './menu.pickle'

# pylint: disable=C0103
app = Flask(__name__)


@app.route('/')
def index():
    """Return a friendly HTTP greeting."""
    message = "It's running!"

    """Get Cloud Run environment variables."""
    service = os.environ.get('K_SERVICE', 'Unknown service')
    revision = os.environ.get('K_REVISION', 'Unknown revision')

    return render_template('index.html',
        message=message,
        Service=service,
        Revision=revision)

@app.route('/menu', methods=['GET'])
def menu():
    """Return menu for a week"""
    menu = []
    try:
        if os.path.isfile(CACHE_FILENAME):
            with open(CACHE_FILENAME, 'rb') as cache:
                menu = pickle.load(cache)            
        else:
            menu = flashMenu()
    except :
        app.logger.WARN('Cannot unpickle cache.')        
        menu = genMenu(DATA_URL)
  
    return render_template('menu.html', debug=(env == 'DEV'), menu=menu, week_days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

@app.route('/menu', methods=['PATCH'])
def flashMenuHandler():
    """Flash the cache with new data from Google Sheets"""
    flashMenu()
    return ('', 204)

def flashMenu():
    app.logger.info('Flash the cache with new data from the remote host')
    menu = genMenu(DATA_URL)
    with open(CACHE_FILENAME, 'wb') as cache:
        pickle.dump(menu, cache, protocol=pickle.HIGHEST_PROTOCOL)        
    return menu


def importMenu(url):
    df = pd.read_csv(url)
    return df

def shuffle_week_menu(df, type):
  breakfast_ser = df[type][df[type].notna()]
  return breakfast_ser.sample(frac=1).to_list()[0:7]

def genMenu(url):
    app.logger.info('Loads menu from the remote host')
    df = importMenu(url)
    breakfast_list = shuffle_week_menu(df, 'breakfast')
    lunch_list = shuffle_week_menu(df, 'lunch')
    dinner_list = shuffle_week_menu(df, 'dinner')
    snacks_list = shuffle_week_menu(df, 'snacks')
    return {'breakfast':breakfast_list,  'lunch': lunch_list, 'dinner':dinner_list, 'snacks':snacks_list}

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=(env == 'DEV'), port=server_port, host='0.0.0.0')
