"""
Base Page class with common methods for all page objects
"""
from playwright.sync_api import Page, expect
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class BasePage:
    """Base page class containing common page methods"""
    
    def __init__(self, page: Page):
        self.page = page
        self.default_timeout = 30000
    
    def navigate_to(self, url: str, wait_until: str = "domcontentloaded"):
        """Navigate to a URL"""
        logger.info(f"Navigating to {url}")
        self.page.goto(url, wait_until=wait_until, timeout=60000)
    
    def click(self, selector: str, timeout: Optional[int] = None):
        """Click an element"""
        timeout = timeout or self.default_timeout
        logger.info(f"Clicking element: {selector}")
        self.page.locator(selector).click(timeout=timeout)
    
    def fill(self, selector: str, text: str, timeout: Optional[int] = None):
        """Fill an input field"""
        timeout = timeout or self.default_timeout
        logger.info(f"Filling element {selector} with text")
        self.page.locator(selector).fill(text, timeout=timeout)
    
    def type_slowly(self, selector: str, text: str, delay: int = 100):
        """Type text slowly (useful for avoiding bot detection)"""
        logger.info(f"Typing slowly in element: {selector}")
        self.page.locator(selector).type(text, delay=delay)
    
    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """Get text content of an element"""
        timeout = timeout or self.default_timeout
        return self.page.locator(selector).inner_text(timeout=timeout)
    
    def is_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        """Check if element is visible"""
        timeout = timeout or self.default_timeout
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False
    
    def is_hidden(self, selector: str, timeout: Optional[int] = None) -> bool:
        """Check if element is hidden"""
        timeout = timeout or self.default_timeout
        try:
            self.page.locator(selector).wait_for(state="hidden", timeout=timeout)
            return True
        except Exception:
            return False
    
    def wait_for_selector(self, selector: str, state: str = "visible", timeout: Optional[int] = None):
        """Wait for a selector to be in a specific state"""
        timeout = timeout or self.default_timeout
        logger.info(f"Waiting for {selector} to be {state}")
        self.page.locator(selector).wait_for(state=state, timeout=timeout)
    
    def wait_for_url(self, url_pattern: str, timeout: Optional[int] = None):
        """Wait for URL to match pattern"""
        timeout = timeout or self.default_timeout
        logger.info(f"Waiting for URL to match: {url_pattern}")
        self.page.wait_for_url(url_pattern, timeout=timeout)
    
    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.page.url
    
    def get_title(self) -> str:
        """Get page title"""
        return self.page.title()
    
    def press_key(self, selector: str, key: str):
        """Press a key on an element"""
        logger.info(f"Pressing {key} on {selector}")
        self.page.locator(selector).press(key)
    
    def wait_for_load_state(self, state: str = "load"):
        """Wait for page load state"""
        logger.info(f"Waiting for load state: {state}")
        self.page.wait_for_load_state(state)
    
    def screenshot(self, path: str, full_page: bool = True):
        """Take a screenshot"""
        logger.info(f"Taking screenshot: {path}")
        self.page.screenshot(path=path, full_page=full_page)
    
    def get_attribute(self, selector: str, attribute: str) -> Optional[str]:
        """Get attribute value of an element"""
        return self.page.locator(selector).get_attribute(attribute)
    
    def count_elements(self, selector: str) -> int:
        """Count number of elements matching selector"""
        return self.page.locator(selector).count()
    
    def is_enabled(self, selector: str) -> bool:
        """Check if element is enabled"""
        return self.page.locator(selector).is_enabled()
    
    def is_checked(self, selector: str) -> bool:
        """Check if checkbox/radio is checked"""
        return self.page.locator(selector).is_checked()
    
    def select_option(self, selector: str, value: str):
        """Select option from dropdown"""
        logger.info(f"Selecting option {value} in {selector}")
        self.page.locator(selector).select_option(value)
    
    def hover(self, selector: str):
        """Hover over an element"""
        logger.info(f"Hovering over {selector}")
        self.page.locator(selector).hover()
    
    def scroll_to_element(self, selector: str):
        """Scroll to an element"""
        logger.info(f"Scrolling to {selector}")
        self.page.locator(selector).scroll_into_view_if_needed()
    
    def execute_script(self, script: str):
        """Execute JavaScript"""
        return self.page.evaluate(script)
    
    # Validation Methods using Playwright's expect
    
    def assert_visible(self, selector: str, message: str = ""):
        """Assert element is visible"""
        logger.info(f"Asserting {selector} is visible")
        expect(self.page.locator(selector)).to_be_visible()
    
    def assert_hidden(self, selector: str, message: str = ""):
        """Assert element is hidden"""
        logger.info(f"Asserting {selector} is hidden")
        expect(self.page.locator(selector)).to_be_hidden()
    
    def assert_text(self, selector: str, expected_text: str):
        """Assert element contains text"""
        logger.info(f"Asserting {selector} contains text: {expected_text}")
        expect(self.page.locator(selector)).to_contain_text(expected_text)
    
    def assert_url_contains(self, url_part: str):
        """Assert URL contains specific string"""
        logger.info(f"Asserting URL contains: {url_part}")
        expect(self.page).to_have_url(url_part)
    
    def assert_enabled(self, selector: str):
        """Assert element is enabled"""
        logger.info(f"Asserting {selector} is enabled")
        expect(self.page.locator(selector)).to_be_enabled()
    
    def assert_disabled(self, selector: str):
        """Assert element is disabled"""
        logger.info(f"Asserting {selector} is disabled")
        expect(self.page.locator(selector)).to_be_disabled()
    
    def assert_element_count(self, selector: str, count: int):
        """Assert number of elements matching selector"""
        logger.info(f"Asserting {selector} count is {count}")
        expect(self.page.locator(selector)).to_have_count(count)
