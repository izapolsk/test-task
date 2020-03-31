from widgetastic.widget.base import View
from widgetastic_bootstrap.button import Button
from widgetastic.widget.input import TextInput
from widgetastic.widget.text import Text
from widgetastic_patternfly import BootstrapNav

from lib.widgets.account_dropdown import AccountDropdown


class LoginView(View):
    title = Text(locator='//h2[normalize-space(.)="Login"]')
    email = TextInput(locator='//input[@type="email"]')
    password = TextInput(locator='//input[@type="password"]')

    login = Button('Login')

    def log_in(self, email, password):
        self.fill({
            'email': email,
            'password': password,
        })
        self.login.click()

    @property
    def logged_in(self):
        raise NotImplementedError("This check is going to be implemented later due to limited time")

    @property
    def is_displayed(self):
        return self.title.is_displayed


class BaseLoggedInView(View):

    # todo: turn into navbar widget
    @View.nested
    class navbar(View):
        account = AccountDropdown(id="account-dropdown")

    # merge this with dropdown above
    navigation = BootstrapNav('.//div/ul')

    @property
    def is_displayed(self):
        return self.navbar.account.is_displayed
