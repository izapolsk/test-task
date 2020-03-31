from selenium.webdriver.support.ui import Select
from widgetastic.widget import Widget
from widgetastic.xpath import quote
from widgetastic_bootstrap.dropdown import (DropdownItemDisabled, DropdownItemNotFound, NoSuchElementException)


class HTMLDropdown(Widget):
    """Represents the HTML dropdown.

    Args:
        locator: locator to select element

    """
    OPTIONS_LOCATOR = "./option"
    OPTION_LOCATOR = "./option[normalize-space(.)={}]"

    def __init__(self, parent, locator, logger=None):
        Widget.__init__(self, parent, logger=logger)
        self.locator = locator

    def __locator__(self):
        return self.locator

    @property
    def items(self):
        """Returns a list of all dropdown items as strings."""
        return [self.browser.text(el) for el in self.browser.elements(self.OPTIONS_LOCATOR)]

    def has_item(self, item):
        """Returns whether the items exists.

        Args:
            item: item name

        Returns:
            Boolean - True if enabled, False if not.
        """
        return item in self.items

    def item_element(self, item):
        """Returns a WebElement for given item name."""
        try:
            return self.browser.element(self.OPTION_LOCATOR.format(quote(item)))
        except NoSuchElementException:
            try:
                items = self.items
            except NoSuchElementException:
                items = []
            if items:
                items_string = "These items are present: {}".format("; ".join(items))
            else:
                items_string = "The dropdown is probably not present"
            raise DropdownItemNotFound("Item {!r} not found. {}".format(item, items_string))

    def item_enabled(self, item):
        """Returns whether the given item is enabled.

        Args:
            item: Name of the item.

        Returns:
            Boolean - True if enabled, False if not.
        """
        el = self.item_element(item)
        return self.browser.get_attribute('disabled', el) != 'true'

    def item_select(self, item):
        """Opens the dropdown and selects the desired item.

        Args:
            item: Item to be selected

        Raises:
            DropdownItemDisabled
        """
        self.logger.info("Selecting %r", item)

        if not self.item_enabled(item):
            raise DropdownItemDisabled(
                'Item "{}" of dropdown "{}" is disabled\n'
                'The following items are available: {}'
                .format(item, self.locator, ";".join(self.items)))
        select = Select(self.browser.element(self))
        select.select_by_visible_text(item)

    def __repr__(self):
        return "{}({!r})".format(type(self).__name__, self.locator)

    @property
    def selected_item(self):
        select = Select(self.browser.element(self))
        return select.first_selected_option

    def read(self):
        return self.selected_item

    def fill(self, value):
        current_value = self.selected_item
        if value == current_value:
            return False

        self.item_select(value)
        return True
