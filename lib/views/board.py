from widgetastic.widget import TextInput, View, GenericLocatorWidget
from widgetastic.utils import WaitFillViewStrategy
from widgetastic_bootstrap.button import Button

from lib.views.base import BaseLoggedInView
from lib.widgets.card import Card
from lib.widgets.html_dropdown import HTMLDropdown
from lib.widgets.sweet_alert import SweetAlert


class CreateBoardView(BaseLoggedInView):
    fill_strategy = WaitFillViewStrategy()

    session_name = TextInput(locator='//input[@type="text" and @placeholder="Session Name"]')
    owner = HTMLDropdown(locator='//select[@class="custom-select"]')
    create_board = Button('Create Board')
    alert = SweetAlert()


class MainBoardView(BaseLoggedInView):
    @property
    def is_displayed(self):
        return all((super(MainBoardView, self).is_displayed,
                   self.body.went_well.is_displayed,
                   self.body.went_unwell.is_displayed,
                   self.body.action_points.is_displayed))

    @View.nested
    class sidebar(View):  # noqa
        pass

    @View.nested
    class body(View):  # noqa
        @View.nested
        class went_well(View):  # noqa
            ROOT = './/h5[./span[normalize-space(.)="Went well"]]'
            add = GenericLocatorWidget(locator='.//button[contains(@class, "text-success") and '
                                               './*[name()="svg" and @data-icon="plus-circle"]]')

            @property
            def cards(self):
                return Card.all(self)

        @View.nested
        class went_unwell(View):  # noqa
            ROOT = './/h5[./span[normalize-space(.)="Didn\'t go well"]]'
            add = GenericLocatorWidget(locator='.//button[contains(@class, "text-danger") and '
                                               './*[name()="svg" and @data-icon="plus-circle"]]')

            @property
            def cards(self):
                return Card.all(self)

        @View.nested
        class action_points(View):  # noqa
            ROOT = './/h5[./span[normalize-space(.)="Action items"]]'
            add = GenericLocatorWidget(locator='.//button[contains(@class, "text-primary") and '
                                               './*[name()="svg" and @data-icon="plus-circle"]]')

            @property
            def cards(self):
                return Card.all(self)
