import pytest

from selenium.webdriver import Chrome, ChromeOptions
from widgetastic.browser import Browser

from lib.views.base import LoginView, BaseLoggedInView
from lib.views.board import CreateBoardView, MainBoardView
from lib.views.card import AddCardView


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
    # step 1. Go to https://sprintboards.io/auth/login
    driver.get(APP_URL)
    yield Browser(selenium=driver)


@pytest.fixture(scope='module')
def login(browser):
    # todo: replace with navmazing navigation and test application class

    # Step 2. Type "sennderqa3@gmail.com" in “Email Address” field
    # Step 3. Type “n*H7A7f@&ikbwu” as password in “Password” field
    # Step 4. Click “Login”
    login_view = LoginView(browser)
    assert login_view.is_displayed, "Login View isn't open"
    login_view.log_in(**APP_CREDS)
    assert BaseLoggedInView(browser).is_displayed, "User couldn't login into application"


@pytest.fixture(scope='module')
def board(login, browser):
    logged_in_view = BaseLoggedInView(browser)
    # Step 5. Click “CREATE BOARD”
    logged_in_view.navigation.select('Create Board')
    # Expected Result 5.1. User is taken to https://sprintboards.io/boards/create
    expected_url = 'https://sprintboards.io/boards/create'
    assert browser.url == expected_url, f"Expected url is {expected_url} whereas test got {browser.url}"

    # todo: check if below condition is right
    # Expected Result 5.2. “Create a Board” title is displayed
    expected_title = 'Create a Board'
    assert expected_title in browser.title, (f"Expected Browser title is {expected_title} "
                                             f"whereas test got {browser.title}")
    boards_view = CreateBoardView(browser)
    # todo: check if that's ok that test has to set owner. it's not in scenario
    # Step 6. Type “My first board” in “Session Name” field
    boards_view.fill(dict(session_name="My first board", owner="Sennder"))
    # Step 7. Click “Create Board” button
    boards_view.create_board.click()
    boards_view.alert.wait_displayed()
    # Expected Result 7.1. User gets a confirmation pop-up saying “Created”
    assert boards_view.alert.title == 'Created', f"Wrong alert title: {boards_view.alert.title}"
    # Expected Result 7.2. URL contains “https://sprintboards.io/boards”
    expected_url = 'https://sprintboards.io/boards'
    assert browser.url == expected_url, f"Expected url is {expected_url} whereas test got {browser.url}"
    yield
    # todo: add delete board scenario


def test_create_green_card(board):
    card_title = 'Goal was achieved'
    card_description = 'Sprint was well planned'

    # Step 8. Click green “+” button
    boards_view = MainBoardView(browser)
    boards_view.body.went_well.add.click()
    # Expected Result 8.1. A modal with title “Add a Card” is displayed
    add_card_view = AddCardView(browser)
    assert add_card_view.is_displayed, "Add a Card view hasn't been displayed"
    # Step 9. Type “Goal was achieved” as title
    # Step 10. Type “Sprint was well planned” as description
    add_card_view.body.fill(values=dict(title=card_title, description=card_description))
    # Step 11. Click “Add Card” button
    add_card_view.body.add_card.click()
    try:
        # Expected Result 11. Card is added with the title and description specified in steps 9 and 10
        next(card for card in boards_view.body.went_well.cards if card.description == card_description and
             card.title == card_title)
    except StopIteration:
        pytest.fail("Card hasn't been created or has wrong title or description")


def test_create_delete_red_card(board):
    card_title = 'Goal was not achieved'
    card_description = 'No description provided'
    # Step 12. Click red “+” button
    boards_view = MainBoardView(browser)
    boards_view.body.went_unwell.add.click()
    # Expected Result 12.1. A modal with title “Add a Card” is displayed
    add_card_view = AddCardView(browser)
    assert add_card_view.is_displayed, "Add a Card view hasn't been displayed"
    # Step 13. Type “Goal was not achieved” as title
    add_card_view.body.fill(values=dict(title=card_title))
    # Step 14. Click “Add Card” button
    add_card_view.body.add_card.click()
    try:
        # Expected Result 14.1 Card is added with the title specified in step 13
        # Expected Result 14.2 Card’s description is set to “No description provided.”
        created_card = next(card for card in boards_view.body.went_unwell.cards if card.title == card_title and
                            card.description == card_description)
    except StopIteration:
        pytest.fail("Card hasn't been created or has wrong title or description")

    # Step 15. Click thumbs up icon for the card in the first column
    created_card.like()
    # Expected Result 15. “Likes” count goes from 0 to 1
    assert created_card.liked, "Thumbs up hasn't been updated"
    # Step 16. Click “x Delete” button from the card in the second column

    # Expected Result 16. Modal appears with the following text: • “Delete Card” • “Are you sure you want to continue?”

    # Step 17. Click “Confirm” button
    # Expected Result 17. Card with title “Goal was not achieved” is removed from the board
