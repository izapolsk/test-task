from widgetastic.exceptions import NoSuchElementException
from widgetastic.widget import Text, View
from widgetastic_patternfly import Modal, Button


class BootstrapModal(Modal):
    @property
    def is_displayed(self):
        """ Is the modal currently open? """
        try:
            return "show" in self.browser.classes(self)
        except NoSuchElementException:
            return False

    def dismiss(self):
        """ Cancel the modal"""
        self.header.close.click()

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
        description = Text(locator='.//p')

    @View.nested
    class footer(View):  # noqa
        """ The footer of the modal """
        ROOT = './/div[contains(@class, "modal-footer")]'
        accept = Button(classes=[Button.SUCCESS])
