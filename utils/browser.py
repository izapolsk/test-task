import attr
import atexit

from webdriver_kaifuku import BrowserFactory as KaifukuBrowserFactory
from webdriver_kaifuku import BrowserManager as KaifukuBrowserManager

# todo: fix this
from test_task.utils.log import logger
from test_task.utils import conf


@attr.s
class BrowserManager(KaifukuBrowserManager):
    BR_FACTORY_CLASS = KaifukuBrowserFactory

    DEFAULT_CHROME_OPT_ARGS = [
        '--no-sandbox',
        '--start-maximized',
        '--disable-extensions',
        '--disable-infobars'
    ]

    def start_at_url(self, url):
        logger.info(f'starting browser and getting URL: "{url}"')
        if self.browser is not None:
            self.quit()
        self.open_fresh()
        self.browser.get(url)
        return self.browser


manager = BrowserManager.from_conf(conf.browser.get('browser', {}))
atexit.register(manager.quit)