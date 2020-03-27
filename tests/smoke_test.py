import pytest

from selenium.webdriver import Chrome, ChromeOptions
from widgetastic.browser import Browser

from lib.views.base import LoginView


@pytest.fixture(scope='session')
def browser():
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument('--headless')
    driver = Chrome(options=chrome_options)
    # 1.  https: // sprintboards.io / auth / login
    driver.get('https://sprintboards.io/auth/login')
    yield Browser(selenium=driver)


@pytest.fixture(scope='module')
def login(browser):
    # 2. Type "sennderqa3@gmail.com" in “Email Address” field
    # 3. Type “n*H7A7f@&ikbwu” as password in “Password” field
    # 4. Click “Login”
    login_view = LoginView(browser)
    assert login_view.is_displayed, "Login View is open"
    login_view.log_in(email="sennderqa3@gmail.com", password='n*H7A7f@&ikbwu')


@pytest.fixture(scope='function')
def app(browser, login):
    print('blabla')
    pass


def test_crud_card(app):
    pass


