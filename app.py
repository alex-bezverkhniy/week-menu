import secrets
import meals_service as mservice

from nicegui import ui, app


URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTl9ZmUxoD6z1PT9YgehwKVg2V6shIwLiHoB0L1ak1eA-7lidZ8wiigziQIMfGKXl2twqarK5OaYPqZ/pub?gid=720294345&single=true&output=csv'

# @ui.refreshable
def meal_card(meal: str, card: ui.refreshable):
    with ui.card().tight():
        title = mservice.get_meal_title(meal)
        image_url = mservice.get_meal_image(meal)
        desc = mservice.get_meal_description(meal)
        with ui.image(image_url).style('min-width: 15em; max-width: 35em; min-height: 15em; max-height: 35em;'):
            ui.label(title).classes(
                'absolute-bottom text-subtitle2 text-center')            
        with ui.card_section():
            ui.markdown(desc)
        with ui.card_actions():
            ui.button(icon='refresh', on_click=card.refresh).props('flat color=blue')

@ui.refreshable
def breakfast_card():
    meals_list = app.storage.user.get('breakfast_list', [])
    meal = mservice.get_random_meal(meals_list)
    with ui.column():
        ui.label('Breakfast').classes('text-h4 text-center')
        meal_card(meal, breakfast_card)

@ui.refreshable
def lunch_card():
    meals_list = app.storage.user.get('lunch_list', [])
    meal = mservice.get_random_meal(meals_list)
    with ui.column():
        ui.label('Lunch').classes('text-h4 text-center')
        meal_card(meal, lunch_card)

@ui.refreshable
def dinner_card():
    meals_list = app.storage.user.get('dinner_list', [])
    meal = mservice.get_random_meal(meals_list)
    with ui.column():
        ui.label('Dinner').classes('text-h4 text-center')
        meal_card(meal, dinner_card)

@ui.page('/')
def index():
    df = mservice.load_menu(URL)
    breakfast_list = mservice.week_menu(df, 'breakfast')
    lunch_list = mservice.week_menu(df, 'lunch')
    dinner_list = mservice.week_menu(df, 'dinner')
    
    app.storage.user['breakfast_list'] = breakfast_list
    app.storage.user['lunch_list'] = lunch_list
    app.storage.user['dinner_list'] = dinner_list
    

    with ui.row():                
        breakfast_card()
        lunch_card()
        dinner_card()
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
