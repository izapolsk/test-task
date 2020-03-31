from widgetastic.widget.base import GenericLocatorWidget, View
from widgetastic.exceptions import NoSuchElementException


class SweetAlert(View):
    """ Sweet alert modal widget

    """
    ROOT = '//div[contains(@class, "swal-overlay") and .//div[contains(@class, "swal-modal") and @role="dialog"]]'
    TITLE = './/div[contains(@class, "swal-title")]'
    TEXT = './/div[contains(@class, "swal-text")]'

    @property
    def is_displayed(self):
        """ Is the modal currently open? """
        try:
            return "swal-overlay--show-modal" in self.browser.classes(self)
        except NoSuchElementException:
            return False

    @property
    def title(self):
        return self.browser.text(self.TITLE)

    @property
    def text(self):
        return self.browser.text(self.TEXT)

    @View.nested
    class footer(View):  # noqa
        """ The footer of the modal """
        ROOT = './/div[@class="swal-footer"]'
        accept = GenericLocatorWidget(locator='.//button[contains(@class, "swal-button--confirm")]')

    def accept(self):
        """ Submit/Save/Accept/Delete for the modal."""
        self.footer.accept.click()
