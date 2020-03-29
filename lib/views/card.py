from widgetastic.exceptions import NoSuchElementException
from widgetastic.widget import TextInput, Text, View
from widgetastic_patternfly import Modal, Button

from lib.widgets.html_dropdown import HTMLDropdown


class AddCardView(Modal):
    @property
    def is_displayed(self):
        """ Is the modal currently open? """
        try:
            return "show" in self.browser.classes(self)
        except NoSuchElementException:
            return False

    @View.nested
    class header(View):  # noqa
        """ The header of the modal """
        ROOT = './/div[contains(@class, "modal-header")]'
        close = Text(locator='.//button[@class="close"]')
        title = Text(locator='.//div[contains(@class,"modal-title")]')

    @View.nested
    class body(View):  # noqa
        """ The body of the modal """
        ROOT = './/div[@class="modal-body"]'
        title = TextInput(locator='.//input[@type="text"]')
        description = TextInput(locator='.//textarea')
        card_type = HTMLDropdown(locator='.//select[@class="custom-select"]')

    @View.nested
    class footer(View):  # noqa
        """ The footer of the modal """
        ROOT = './/div[contains(@class, "modal-footer")]'
        accept = Button(classes=Button.SUCCESS)
