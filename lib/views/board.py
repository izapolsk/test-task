from widgetastic.widget import TextInput, View, GenericLocatorWidget, Text
from widgetastic_bootstrap.button import Button

from lib.views.base import BaseLoggedInView
from lib.widgets.html_dropdown import HTMLDropdown
from lib.widgets.sweet_alert import SweetAlert


class CreateBoardView(BaseLoggedInView):
    session_name = TextInput(locator='//input[@type="text" and @placeholder="Session Name"]')
    owner = HTMLDropdown(locator='//select[@class="custom-select"]')
    create_board = Button('Create Board')
    alert = SweetAlert()


class MainBoardView(BaseLoggedInView):
    @property
    def is_displayed(self):
        return all((super(MainBoardView, self).is_displayed,
                   self.body.add_well.is_displayed,
                   self.body.add_not_well.is_displayed,
                   self.body.add_action_point.is_displayed))

    @View.nested
    class sidebar(View):  # noqa
        pass

    class body(View):  # noqa
        add_well = GenericLocatorWidget(locator='.//button[contains(@class, "card") and '
                                                'contains(@class, "text-success")]')
        add_not_well = GenericLocatorWidget(locator='.//button[contains(@class, "card") and '
                                                    'contains(@class, "text-danger")]')
        add_action_point = GenericLocatorWidget(locator='.//button[contains(@class, "card") and '
                                                        'contains(@class, "text-primary")]')
