"""
A sample Hello World server.
"""
import os
import pandas as pd

from flask import Flask, render_template

DATA_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTl9ZmUxoD6z1PT9YgehwKVg2V6shIwLiHoB0L1ak1eA-7lidZ8wiigziQIMfGKXl2twqarK5OaYPqZ/pub?gid=720294345&single=true&output=csv'
env = os.environ.get('ENV', 'PROD')


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

@app.route('/menu')
def menu():
    """Return menu for a week"""
    
    """Load data from Google Sheets"""
    menu = gen_menu(DATA_URL)
  
    return render_template('menu.html', DEBUG=(env == 'DEV'), menu=menu, week_days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])


def load_menu(url):
    df = pd.read_csv(url)
    return df

def shuffle_week_menu(df, type):
  breakfast_ser = df[type][df[type].notna()]
  return breakfast_ser.sample(frac=1).to_list()[0:7]

def gen_menu(url):
    df = load_menu(url)
    breakfast_list = shuffle_week_menu(df, 'breakfast')
    lunch_list = shuffle_week_menu(df, 'lunch')
    dinner_list = shuffle_week_menu(df, 'dinner')
    snacks_list = shuffle_week_menu(df, 'snacks')
    return {'breakfast':breakfast_list,  'lunch': lunch_list, 'dinner':dinner_list, 'snacks':snacks_list}

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=(env == 'DEV'), port=server_port, host='0.0.0.0')
