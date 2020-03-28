from widgetastic.widget import Widget
from widgetastic.utils import ParametrizedLocator
from widgetastic_bootstrap.dropdown import (Dropdown, DropdownItemDisabled, DropdownDisabled,
                                            UnexpectedAlertPresentException)


class AccountDropdown(Dropdown):
    ROOT = ParametrizedLocator('//a[contains(@data-toggle, "dropdown") and @id={@id|quote}]')
    ITEMS_LOCATOR = ParametrizedLocator(
        '//div[contains(@class, "dropdown-menu") and @aria-labelledby={@id|quote}]/*[self::a or self::button]')
    ITEM_LOCATOR = ParametrizedLocator(
        '//div[contains(@class, "dropdown-menu") and @aria-labelledby={@id|quote}]/*[self::a '
        'or self::button][normalize-space(.)={}]')

    def __init__(self, parent, id, logger=None):
        Widget.__init__(self, parent, logger=logger)
        self.id = id

    def _verify_enabled(self):
        if not self.is_enabled:
            raise DropdownDisabled('Dropdown "{}" is not enabled'.format(self.id))

    def item_select(self, item, handle_alert=None):
        """Opens the dropdown and selects the desired item.

        Args:
            item: Item to be selected
            handle_alert: How to handle alerts. None - no handling, True - confirm, False - dismiss.

        Raises:
            DropdownItemDisabled
        """
        self.logger.info("Selecting %r", item)
        try:
            self.open()
            if not self.item_enabled(item):
                raise DropdownItemDisabled(
                    'Item "{}" of dropdown "{}" is disabled\n'
                    'The following items are available: {}'
                        .format(item, self.id, ";".join(self.items)))
            self.browser.click(self.item_element(item), ignore_ajax=handle_alert is not None)
            if handle_alert is not None:
                self.browser.handle_alert(cancel=not handle_alert, wait=10.0)
                self.browser.plugin.ensure_page_safe()
        finally:
            try:
                self.close(ignore_nonpresent=True)
            except UnexpectedAlertPresentException:
                self.logger.warning("There is an unexpected alert present.")
                pass

    def __repr__(self):
        return "{}({!r})".format(type(self).__name__, self.id)

    @property
    def is_enabled(self):
        """Returns if the dropdown itself is enabled and therefore interactive."""
        return "disabled" not in self.browser.classes(self)

    def open(self):
        self._verify_enabled()
        if not self.is_open:
            self.browser.click(self)

    @property
    def is_open(self):
        return self.browser.get_attribute('aria-expanded', self) == 'true'
