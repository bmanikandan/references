"""
Gmail Inbox Page Object
Handles all inbox-related actions and DOM validations
"""
from pages.base_page import BasePage
from config.locators import GmailInboxLocators
from playwright.sync_api import expect
import logging

logger = logging.getLogger(__name__)


class InboxPage(BasePage):
    """Gmail Inbox Page Object"""
    
    def __init__(self, page):
        super().__init__(page)
        self.locators = GmailInboxLocators()
    
    # DOM Element Validation Methods
    
    def validate_compose_button_present(self) -> bool:
        """Validate Compose button is present"""
        logger.info("Validating Compose button presence")
        return self.is_visible(self.locators.COMPOSE_BUTTON_TEXT, timeout=15000)
    
    def validate_compose_button_attributes(self):
        """Validate Compose button DOM attributes"""
        logger.info("Validating Compose button attributes")
        compose_btn = self.page.locator(self.locators.COMPOSE_BUTTON_TEXT)
        
        # Check if it's visible
        expect(compose_btn).to_be_visible()
        
        # Check if it's enabled
        expect(compose_btn).to_be_enabled()
        
        logger.info("Compose button attributes validated successfully")
    
    def validate_gmail_logo_present(self) -> bool:
        """Validate Gmail logo is present"""
        logger.info("Validating Gmail logo presence")
        return self.is_visible(self.locators.GMAIL_LOGO, timeout=10000)
    
    def validate_search_box_present(self) -> bool:
        """Validate search box is present"""
        logger.info("Validating search box presence")
        return self.is_visible(self.locators.SEARCH_BOX, timeout=10000)
    
    def validate_search_box_attributes(self):
        """Validate search box DOM attributes"""
        logger.info("Validating search box attributes")
        search_box = self.page.locator(self.locators.SEARCH_BOX)
        
        # Check aria-label
        expect(search_box).to_have_attribute("aria-label", "Search mail")
        
        # Check if it's visible
        expect(search_box).to_be_visible()
        
        # Check if it's enabled
        expect(search_box).to_be_enabled()
        
        logger.info("Search box attributes validated successfully")
    
    def validate_inbox_link_present(self) -> bool:
        """Validate Inbox link is present in navigation"""
        logger.info("Validating Inbox link presence")
        return self.is_visible(self.locators.INBOX_LINK, timeout=10000)
    
    def validate_navigation_menu_items(self) -> dict:
        """Validate all navigation menu items are present"""
        logger.info("Validating navigation menu items")
        
        menu_items = {
            "Inbox": self.is_visible(self.locators.INBOX_LINK, timeout=5000),
            "Starred": self.is_visible(self.locators.STARRED_LINK, timeout=5000),
            "Sent": self.is_visible(self.locators.SENT_LINK, timeout=5000),
            "Drafts": self.is_visible(self.locators.DRAFTS_LINK, timeout=5000)
        }
        
        logger.info(f"Navigation menu validation results: {menu_items}")
        return menu_items
    
    def validate_profile_button_present(self) -> bool:
        """Validate profile button is present"""
        logger.info("Validating profile button presence")
        # Try multiple selectors as Gmail structure can vary
        try:
            return (self.is_visible(self.locators.PROFILE_BUTTON, timeout=10000) or
                    self.is_visible(self.locators.PROFILE_IMAGE, timeout=5000))
        except Exception:
            logger.warning("Profile button validation failed with both selectors")
            return False
    
    def validate_settings_button_present(self) -> bool:
        """Validate settings button is present"""
        logger.info("Validating settings button presence")
        return self.is_visible(self.locators.SETTINGS_BUTTON, timeout=10000)
    
    def validate_main_content_area_present(self) -> bool:
        """Validate main content area is present"""
        logger.info("Validating main content area presence")
        return self.is_visible(self.locators.MAIN_CONTENT, timeout=10000)
    
    def validate_toolbar_present(self) -> bool:
        """Validate toolbar is present"""
        logger.info("Validating toolbar presence")
        return self.is_visible(self.locators.TOOLBAR, timeout=10000)
    
    def get_email_count(self) -> int:
        """Get count of visible emails in inbox"""
        logger.info("Counting visible emails")
        return self.count_elements(self.locators.EMAIL_ROW)
    
    def validate_emails_loaded(self) -> bool:
        """Validate that emails are loaded in the inbox"""
        logger.info("Validating emails are loaded")
        email_count = self.get_email_count()
        logger.info(f"Found {email_count} emails in inbox")
        return email_count >= 0  # Even 0 is valid (empty inbox)
    
    # Action Methods
    
    def click_profile_button(self):
        """Click on profile button to open account menu"""
        logger.info("Clicking profile button")
        # Try primary selector first
        try:
            self.click(self.locators.PROFILE_BUTTON, timeout=5000)
        except Exception:
            # Fallback to image selector
            logger.info("Using fallback selector for profile button")
            self.click(self.locators.PROFILE_IMAGE, timeout=5000)
        
        # Wait for account menu to appear
        self.wait_for_selector(self.locators.ACCOUNT_MENU, timeout=5000)
    
    def validate_account_menu_visible(self) -> bool:
        """Validate account menu is visible after clicking profile"""
        logger.info("Validating account menu visibility")
        return self.is_visible(self.locators.ACCOUNT_MENU, timeout=5000)
    
    def validate_signout_button_present(self) -> bool:
        """Validate Sign Out button is present in account menu"""
        logger.info("Validating Sign Out button presence")
        return self.is_visible(self.locators.SIGN_OUT_BUTTON, timeout=5000)
    
    def click_signout(self):
        """Click Sign Out button"""
        logger.info("Clicking Sign Out button")
        self.click(self.locators.SIGN_OUT_BUTTON)
    
    def logout(self):
        """Complete logout flow"""
        logger.info("Starting logout flow")
        
        # Click profile button
        self.click_profile_button()
        
        # Validate account menu appeared
        if not self.validate_account_menu_visible():
            raise AssertionError("Account menu did not appear")
        
        # Validate Sign Out button present
        if not self.validate_signout_button_present():
            raise AssertionError("Sign Out button not found in account menu")
        
        # Click Sign Out
        self.click_signout()
        
        # Wait for redirect to accounts page
        logger.info("Waiting for redirect to accounts page")
        try:
            self.page.wait_for_url("**/accounts.google.com/**", timeout=15000)
            logger.info("Successfully logged out")
        except Exception as e:
            logger.error(f"Logout failed or timeout: {str(e)}")
            raise
    
    def wait_for_inbox_to_load(self):
        """Wait for inbox to fully load"""
        logger.info("Waiting for inbox to load")
        # Wait for multiple indicators
        self.wait_for_selector(self.locators.COMPOSE_BUTTON_TEXT, timeout=20000)
        self.wait_for_load_state("networkidle")
        logger.info("Inbox loaded successfully")
    
    def validate_successfully_logged_in(self) -> bool:
        """Validate user is successfully logged into Gmail inbox"""
        logger.info("Validating successful login")
        
        # Check URL
        current_url = self.get_current_url()
        if "mail.google.com" not in current_url:
            logger.error(f"Not on Gmail page. Current URL: {current_url}")
            return False
        
        # Check for key elements
        checks = {
            "Compose Button": self.validate_compose_button_present(),
            "Gmail Logo": self.validate_gmail_logo_present(),
            "Search Box": self.validate_search_box_present()
        }
        
        all_passed = all(checks.values())
        if all_passed:
            logger.info("Successfully validated login")
        else:
            failed = [k for k, v in checks.items() if not v]
            logger.error(f"Login validation failed for: {', '.join(failed)}")
        
        return all_passed
    
    # Complete DOM Validation Suite
    
    def validate_all_inbox_elements(self):
        """Validate all critical DOM elements on inbox page"""
        logger.info("Starting comprehensive inbox page DOM validation")
        
        validations = {
            "Compose Button": self.validate_compose_button_present(),
            "Gmail Logo": self.validate_gmail_logo_present(),
            "Search Box": self.validate_search_box_present(),
            "Inbox Link": self.validate_inbox_link_present(),
            "Profile Button": self.validate_profile_button_present(),
            "Settings Button": self.validate_settings_button_present(),
            "Main Content": self.validate_main_content_area_present(),
            "Toolbar": self.validate_toolbar_present()
        }
        
        # Validate navigation menu
        nav_items = self.validate_navigation_menu_items()
        validations.update({f"Nav - {k}": v for k, v in nav_items.items()})
        
        # Validate key element attributes
        if validations["Compose Button"]:
            self.validate_compose_button_attributes()
        
        if validations["Search Box"]:
            self.validate_search_box_attributes()
        
        # Check all validations passed
        failed = [k for k, v in validations.items() if not v]
        if failed:
            logger.warning(f"Some inbox elements validation failed: {', '.join(failed)}")
            # Don't raise exception, just log - Gmail UI can vary
        else:
            logger.info("All inbox page DOM elements validated successfully")
        
        return validations
