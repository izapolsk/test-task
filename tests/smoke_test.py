import pytest

from selenium.webdriver import Chrome, ChromeOptions
from widgetastic.browser import Browser

from lib.views.base import LoginView, BaseLoggedInView
from lib.views.board import CreateBoardView, MainBoardView


APP_URL = 'https://sprintboards.io/auth/login'
APP_CREDS = dict(email="sennderqa3@gmail.com", password='n*H7A7f@&ikbwu')


@pytest.fixture(scope='session')
def browser():
    # todo: replace with webdriver-kaifuku and move settings and etc to config files
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument('--headless')
    driver = Chrome(options=chrome_options)
    # 1.  https://sprintboards.io/auth/login
    driver.get(APP_URL)
    yield Browser(selenium=driver)


@pytest.fixture(scope='module')
def login(browser):
    # todo: replace with navmazing navigation and test application class

    # 2. Type "sennderqa3@gmail.com" in “Email Address” field
    # 3. Type “n*H7A7f@&ikbwu” as password in “Password” field
    # 4. Click “Login”
    login_view = LoginView(browser)
    assert login_view.is_displayed, "Login View isn't open"
    login_view.log_in(**APP_CREDS)
    assert BaseLoggedInView(browser).is_displayed, "User couldn't login into application"


@pytest.fixture(scope='function')
def board(login, browser):
    logged_in_view = BaseLoggedInView(browser)
    logged_in_view.navigation.select('Create Board')
    expected_url = 'https://sprintboards.io/boards/create'
    assert browser.url == expected_url, f"Expected url is {expected_url} whereas test got {browser.url}"

    # todo: check if below condition is right
    expected_title = 'Create a Board'
    assert expected_title in browser.title, (f"Expected Browser title is {expected_title} "
                                             f"whereas test got {browser.title}")
    boards_view = CreateBoardView(browser)
    # todo: check if that's ok that test has to set owner. it's not in scenario
    boards_view.fill(dict(session_name="My first board", owner="Sennder"))
    boards_view.create_board.click()
    boards_view.alert.wait_displayed()
    assert boards_view.alert.title == 'Created', f"Wrong alert title: {boards_view.alert.title}"
    yield
    # todo: add delete board scenario



def test_crud_card(app):
    pass


