from widgetastic.utils import ParametrizedLocator
from widgetastic.widget.base import GenericLocatorWidget
from widgetastic.widget.base import View
from widgetastic_patternfly import Button
from wait_for import wait_for


class Card(View):
    ROOT = ParametrizedLocator('//div[contains(@class, "card") and boolean(@data-card) and @data-card={@id|quote}]')
    ALL_CARDS = '//div[contains(@class, "card") and boolean(@data-card)]'
    TITLE = './/h6'
    DESCRIPTION = './/div[contains(@class, "card-body")]/p[1]'

    like_button = GenericLocatorWidget(locator='.//button[./*[name()="svg" and @data-icon="thumbs-up"]]')
    delete_button = Button('Delete')

    def __init__(self, parent, id, logger=None):
        View.__init__(self, parent, logger=logger)
        self.id = id

    @property
    def title(self):
        return self.browser.text(self.TITLE)

    @property
    def description(self):
        return self.browser.text(self.DESCRIPTION)

    @property
    def liked(self):
        return bool(int(self.browser.text(self.like_button)))

    def wait_liked(self, liked, timeout='5s'):
        return wait_for(lambda: self.like_button.is_displayed and self.liked == liked, timeout=timeout, delay=1)[0]

    def like(self):
        if not self.liked:
            self.like_button.click()
            return True
        else:
            return False

    def unlike(self):
        if self.liked:
            self.like_button.click()
            return True
        else:
            return False

    def delete(self):
        self.delete_button.click()

    @classmethod
    def all(cls, parent):
        cards = []
        for el in parent.browser.elements(cls.ALL_CARDS):
            card_id = parent.browser.get_attribute('data-card', el)
            cards.append(cls(parent, id=card_id))
        return cards