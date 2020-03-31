from widgetastic.widget import View
from widgetastic_patternfly import Button

from lib.widgets.bootstrap_modal import BootstrapModal


class ConfirmModal(BootstrapModal):
    @View.nested
    class footer(View):  # noqa
        """ The footer of the modal """
        ROOT = './/div[contains(@class, "modal-footer")]'
        accept = Button('Confirm')