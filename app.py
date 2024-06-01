import app
# Requests is a great library for working with API's, and it's included
# in the badge libraries, so let's use it here!
#
# See https://requests.readthedocs.io/ for more information on how to use
# it properly!
import requests

from app_components import Menu, Notification, clear_background
from events.input import Buttons


class FilmScheduleApp(app.App):
    def __init__(self):
        # When we load, grab all the API data in JSON format
        # Requests will automatically convert this to a python dict
        # for us, it really is that good!
        self.schedule = requests.get("https://emffilms.org/schedule.json").json()
        self.button_states = Buttons(self)
        # Setup lists to hold our film titles and timings
        main_menu_items = []
        self.timings = []
        # Iterate over the films, adding the title to the menu
        for film in self.schedule['films']:
            text = f"{film['title']}"
            time = f"{film['showing']['text']}"
            main_menu_items.append(text)
            self.timings.append(time)
        # Create the menu object
        self.menu = Menu(
            self,
            main_menu_items,
            select_handler=self.select_handler,
            back_handler=self.back_handler,
        )
        self.notification = None

    def select_handler(self, item, position):
        self.notification = Notification('Showing at ' + self.timings[position] + '!')

    def back_handler(self):
        self.button_states.clear()
        self.minimise()

    def update(self, delta):
        self.menu.update(delta)
        if self.notification:
            self.notification.update(delta)


    def draw(self, ctx):
        clear_background(ctx)
        # Display the menu on the device
        # as a scrollable list of film titles
        self.menu.draw(ctx)
        if self.notification:
            self.notification.draw(ctx)

__app_export__ = FilmScheduleApp
