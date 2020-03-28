from widgetastic.widget import TextInput
from widgetastic_bootstrap.button import Button

from lib.views.base import BaseLoggedInView
from lib.widgets.html_dropdown import HTMLDropdown


class CreateBoardView(BaseLoggedInView):
    session_name = TextInput(locator='//input[@type="text" and @placeholder="Session Name"]')
    owner = HTMLDropdown(locator='//select[@class="custom-select"]')
    create_board = Button('Create Board')


class MainBoardView(BaseLoggedInView):
    pass