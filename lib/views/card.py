from widgetastic.widget import TextInput, View
from widgetastic_bootstrap.button import Button

from lib.widgets.bootstrap_modal import BootstrapModal
from lib.widgets.html_dropdown import HTMLDropdown


class AddCardView(BootstrapModal):
    @View.nested
    class body(View):  # noqa
        """ The body of the modal """
        ROOT = './/div[@class="modal-body"]'
        title = TextInput(locator='.//input[@type="text"]')
        description = TextInput(locator='.//textarea')
        card_type = HTMLDropdown(locator='.//select[@class="custom-select"]')
        add_card = Button('Add Card')
