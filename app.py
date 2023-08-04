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
    meal = mservice.get_random_meal(meals_list)
    meal_card(meal, breakfast_card)

@ui.refreshable
def lunch_card():
    meals_list = app.storage.user.get('lunch_list', [])
    meal = mservice.get_random_meal(meals_list)
    meal_card(meal, lunch_card)

@ui.page('/')
def index():
    breakfast_list = mservice.load_week_menu(URL, 'breakfast')
    lunch_list = mservice.load_week_menu(URL, 'lunch')
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
