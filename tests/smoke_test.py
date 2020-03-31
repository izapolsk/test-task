import pytest

from selenium.webdriver import Chrome, ChromeOptions
from wait_for import TimedOutError, wait_for
from widgetastic.browser import Browser

from lib.views.base import LoginView, BaseLoggedInView
from lib.views.board import CreateBoardView, MainBoardView
from lib.views.card import AddCardView
from lib.views.modals import ConfirmModal
from utils.log import logger


pytestmark = [pytest.mark.smoke]

# todo: move to encrypted file or vault ?
APP_URL = 'https://sprintboards.io/auth/login'
APP_CREDS = dict(email="sennderqa3@gmail.com", password='n*H7A7f@&ikbwu')


@pytest.fixture(scope='session')
def browser(request):
    # todo: replace with webdriver-kaifuku and move settings and etc to config files
    logger.info("openning chrome browser")
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--headless')
    driver = Chrome(options=chrome_options)
    logger.info('step 1. Go to https://sprintboards.io/auth/login')
    driver.get(APP_URL)
    app_browser = Browser(selenium=driver)
    request.addfinalizer(app_browser.close_window)
    yield app_browser


@pytest.fixture(scope='module')
def login(browser):
    # todo: replace with navmazing navigation and test application class

    logger.info('Step 2. Type "sennderqa3@gmail.com" in “Email Address” field')
    logger.info('Step 3. Type “n*H7A7f@&ikbwu” as password in “Password” field')
    logger.info('Step 4. Click “Login”')
    login_view = LoginView(browser)
    assert login_view.is_displayed, "Login View isn't open"
    login_view.log_in(**APP_CREDS)
    try:
        BaseLoggedInView(browser).wait_displayed()
    except TimedOutError:
        pytest.fail("User couldn't login")


@pytest.fixture(scope='module')
def board(login, browser):
    logged_in_view = BaseLoggedInView(browser)
    logger.info('Step 5. Click “CREATE BOARD”')
    logged_in_view.navigation.select('Create Board')
    boards_view = CreateBoardView(browser)
    boards_view.wait_displayed()
    logger.info('Verifying Expected Result 5.1. User is taken to https://sprintboards.io/boards/create')
    expected_url = 'https://sprintboards.io/boards/create'
    assert browser.url == expected_url, f"Expected url is {expected_url} whereas test got {browser.url}"

    # todo: check if below condition is right
    logger.info('Verifying Expected Result 5.2. “Create a Board” title is displayed')
    expected_title = 'Create a Board'
    assert expected_title in browser.title, (f"Expected AppBrowser title is {expected_title} "
                                             f"whereas test got {browser.title}")
    # todo: check if that's ok that test has to set owner. it's not in scenario
    logger.info('Step 6. Type “My first board” in “Session Name” field')
    boards_view.fill(dict(session_name="My first board", owner="Sennder"))
    logger.info('Step 7. Click “Create Board” button')
    boards_view.create_board.click()
    try:
        boards_view.alert.wait_displayed()
        logger.info('Verifying Expected Result 7.1. User gets a confirmation pop-up saying “Created”')
        assert boards_view.alert.title == 'Created', f"Wrong alert title: {boards_view.alert.title}"
    except TimedOutError:
        pytest.fail("Alert hasn't been displayed")
    logger.info('Verifying Expected Result 7.2. URL contains “https://sprintboards.io/boards”')
    expected_url = 'https://sprintboards.io/boards'
    # todo: figure out is that correct that url includes board id and expected url doesn't fully match expected result
    assert browser.url.startswith(expected_url), f"Expected url is {expected_url} whereas test got {browser.url}"
    yield
    # todo: add delete board scenario


def test_create_green_card(board, browser):
    """
        This smoke test covers creation of Went Well card scenario.
        In addition, it goes thru and checks side things like logging in, board creation and etc
    """
    card_title = 'Goal was achieved'
    card_description = 'Sprint was well planned'

    logger.info('Step 8. Click green “+” button')
    boards_view = MainBoardView(browser)
    boards_view.wait_displayed()
    boards_view.body.went_well.add.click()
    logger.info('Verifying Expected Result 8.1. A modal with title “Add a Card” is displayed')
    add_card_view = AddCardView(browser)
    assert add_card_view.is_displayed, "Add a Card view hasn't been displayed"
    logger.info('Step 9. Type “Goal was achieved” as title')
    logger.info('Step 10. Type “Sprint was well planned” as description')
    add_card_view.body.fill(dict(title=card_title, description=card_description))
    logger.info('Step 11. Click “Add Card” button')
    add_card_view.footer.add_card.click()
    boards_view.wait_displayed()
    browser.plugin.ensure_page_safe()
    try:
        logger.info('Verifying Expected Result 11. Card is added with the title '
                    'and description specified in steps 9 and 10')
        card = next(card for card in boards_view.body.went_well.cards if card.description == card_description and
                    card.title == card_title)
    except StopIteration:
        pytest.fail("Card hasn't been created or has wrong title or description")


def test_create_delete_red_card(board, browser):
    """
        This smoke test covers create/update/delete of "Didn't go Well" card scenario.
        In addition, it goes thru and checks side things like logging in, board creation and etc
    """

    card_title = 'Goal was not achieved'
    card_description = 'No description provided'
    logger.info('Step 12. Click red “+” button')
    boards_view = MainBoardView(browser)
    boards_view.wait_displayed()
    boards_view.body.went_unwell.add.click()
    logger.info('Verifying Expected Result 12.1. A modal with title “Add a Card” is displayed')
    add_card_view = AddCardView(browser)
    assert add_card_view.is_displayed, "Add a Card view hasn't been displayed"
    logger.info('Step 13. Type “Goal was not achieved” as title')
    add_card_view.body.fill(dict(title=card_title))
    logger.info('Step 14. Click “Add Card” button')
    add_card_view.footer.add_card.click()
    browser.plugin.ensure_page_safe()
    boards_view.wait_displayed()
    try:
        logger.info('Verifying Expected Result 14.1 Card is added with the title specified in step 13')
        logger.info('Verifying Expected Result 14.2 Card’s description is set to “No description provided.”')
        wait_for(lambda: bool(boards_view.body.went_unwell.cards), timeout='5s', delay=1)  # todo: turn into method
        created_card = next(card for card in boards_view.body.went_unwell.cards if card.title == card_title and
                            card_description in card.description)
        # todo: ask if that correct there is an issue that expected description doesn't fully match card's description
        # it has a point at the end
    except (StopIteration, TimedOutError):
        pytest.fail("Card hasn't been created or has wrong title or description")

    logger.info('Step 15. Click thumbs up icon for the card in the first column')
    created_card.like()
    logger.info('Expected Result 15. “Likes” count goes from 0 to 1')
    assert created_card.wait_liked(True), "Thumbs up hasn't been updated"
    logger.info('Step 16. Click “x Delete” button from the card in the second column')
    created_card.delete()
    logger.info('Verifying Expected Result 16. Modal appears with the following text: '
                '• “Delete Card” • “Are you sure you want to continue?”')
    confirm_modal = ConfirmModal(browser)
    expected_title = "Delete Card"
    expected_description = "Are you sure you want to continue?"
    assert confirm_modal.header.is_displayed, "Confirm delete modal hasn't been displayed"
    assert confirm_modal.header.title.text == expected_title, (f"Expected modal title {expected_title}, "
                                                               f"whereas got title {confirm_modal.header.title}")
    assert (confirm_modal.body.description.text == expected_description,
            f"Expected modal description {expected_description} whereas got description {expected_description}")
    logger.info('Step 17. Click “Confirm” button')
    confirm_modal.accept()
    logger.info('Expected Result 17. Card with title “Goal was not achieved” is removed from the board')
    assert created_card.wait_displayed(), "The card hasn't been removed"
