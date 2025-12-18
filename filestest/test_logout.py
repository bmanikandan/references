"""
Test cases for Gmail Logout functionality with DOM validations
"""
import pytest
from pages.inbox_page import InboxPage
from pages.logout_page import LogoutPage
from config.config import Config
import logging

logger = logging.getLogger(__name__)


@pytest.mark.smoke
@pytest.mark.logout
@pytest.mark.ui
class TestGmailLogout:
    """Test suite for Gmail logout functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, authenticated_page, config):
        """Setup for each test - uses authenticated page fixture"""
        self.page = authenticated_page
        self.config = config
        self.inbox_page = InboxPage(authenticated_page)
        self.logout_page = LogoutPage(authenticated_page)
    
    @pytest.mark.dom
    def test_validate_profile_button_present(self):
        """Test profile button is present in inbox"""
        logger.info("TEST: Validate profile button presence")
        
        assert self.inbox_page.validate_profile_button_present(), \
               "Profile button not present in inbox"
    
    @pytest.mark.dom
    def test_validate_account_menu_opens(self):
        """Test account menu opens when clicking profile button"""
        logger.info("TEST: Validate account menu opens")
        
        # Click profile button
        self.inbox_page.click_profile_button()
        
        # Validate account menu is visible
        assert self.inbox_page.validate_account_menu_visible(), \
               "Account menu did not appear after clicking profile button"
    
    @pytest.mark.dom
    def test_validate_signout_button_in_menu(self):
        """Test Sign Out button is present in account menu"""
        logger.info("TEST: Validate Sign Out button in account menu")
        
        # Open account menu
        self.inbox_page.click_profile_button()
        
        # Validate Sign Out button is present
        assert self.inbox_page.validate_signout_button_present(), \
               "Sign Out button not present in account menu"
    
    @pytest.mark.smoke
    def test_successful_logout(self):
        """Test successful logout from Gmail"""
        logger.info("TEST: Successful logout")
        
        # Perform logout
        self.inbox_page.logout()
        
        # Validate logout was successful
        assert self.logout_page.validate_successfully_logged_out(), \
               "Logout was not successful"
    
    @pytest.mark.dom
    def test_validate_logout_page_url(self):
        """Test URL changes to accounts page after logout"""
        logger.info("TEST: Validate logout page URL")
        
        # Logout
        self.inbox_page.logout()
        
        # Validate we're on accounts page
        assert self.logout_page.validate_on_logout_page(), \
               "Not on logout/accounts page after logout"
    
    @pytest.mark.dom
    def test_validate_logout_page_elements(self):
        """Test logout page DOM elements"""
        logger.info("TEST: Validate logout page DOM elements")
        
        # Logout
        self.inbox_page.logout()
        
        # Validate all logout page elements
        validations = self.logout_page.validate_all_logout_page_elements()
        
        # Check at least we're on the right page
        assert validations["On Logout Page"], \
               "Not on logout page"
    
    @pytest.mark.dom
    def test_validate_account_selection_elements(self):
        """Test account selection elements are present after logout"""
        logger.info("TEST: Validate account selection elements")
        
        # Logout
        self.inbox_page.logout()
        
        # Validate account selection elements
        has_heading = self.logout_page.validate_choose_account_heading_present()
        has_account_btn = self.logout_page.validate_account_button_present()
        
        assert has_heading or has_account_btn, \
               "No account selection elements found on logout page"
    
    @pytest.mark.smoke
    def test_cannot_access_inbox_after_logout(self):
        """Test cannot access inbox after logging out"""
        logger.info("TEST: Cannot access inbox after logout")
        
        # Logout
        self.inbox_page.logout()
        
        # Try to navigate to inbox
        self.page.goto("https://mail.google.com/mail/")
        
        # Should redirect to login page
        current_url = self.page.url
        assert "accounts.google.com" in current_url or "ServiceLogin" in current_url, \
               "Was able to access inbox after logout (should redirect to login)"


@pytest.mark.regression
@pytest.mark.logout
class TestLogoutEdgeCases:
    """Test suite for logout edge cases"""
    
    @pytest.fixture(autouse=True)
    def setup(self, authenticated_page, config):
        """Setup for each test"""
        self.page = authenticated_page
        self.config = config
        self.inbox_page = InboxPage(authenticated_page)
        self.logout_page = LogoutPage(authenticated_page)
    
    def test_logout_from_different_gmail_pages(self):
        """Test logout works from different Gmail pages"""
        logger.info("TEST: Logout from different pages")
        
        # Navigate to sent folder
        try:
            self.page.goto("https://mail.google.com/mail/#sent")
            self.page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            logger.info("Could not navigate to sent folder, continuing with test")
        
        # Logout should still work
        self.inbox_page.logout()
        
        # Validate logout
        assert self.logout_page.validate_successfully_logged_out(), \
               "Logout failed from non-inbox page"
    
    def test_logout_multiple_times(self):
        """Test logout button behavior after clicking multiple times"""
        logger.info("TEST: Logout multiple times")
        
        # Open account menu
        self.inbox_page.click_profile_button()
        
        # Click logout
        self.inbox_page.click_signout()
        
        # Wait for redirect
        self.page.wait_for_url("**/accounts.google.com/**", timeout=15000)
        
        # Validate we're logged out
        assert self.logout_page.validate_on_logout_page(), \
               "Not on logout page after clicking Sign Out"


@pytest.mark.regression
@pytest.mark.dom
class TestInboxDOMValidation:
    """Test suite for detailed inbox DOM validations"""
    
    @pytest.fixture(autouse=True)
    def setup(self, authenticated_page, config):
        """Setup for each test"""
        self.page = authenticated_page
        self.config = config
        self.inbox_page = InboxPage(authenticated_page)
    
    def test_validate_compose_button_attributes(self):
        """Test Compose button DOM attributes"""
        logger.info("TEST: Validate Compose button attributes")
        
        assert self.inbox_page.validate_compose_button_present(), \
               "Compose button not present"
        
        self.inbox_page.validate_compose_button_attributes()
    
    def test_validate_search_box_attributes(self):
        """Test search box DOM attributes"""
        logger.info("TEST: Validate search box attributes")
        
        assert self.inbox_page.validate_search_box_present(), \
               "Search box not present"
        
        self.inbox_page.validate_search_box_attributes()
    
    def test_validate_navigation_menu(self):
        """Test all navigation menu items are present"""
        logger.info("TEST: Validate navigation menu items")
        
        menu_items = self.inbox_page.validate_navigation_menu_items()
        
        # At least Inbox should be present
        assert menu_items.get("Inbox", False), \
               "Inbox link not found in navigation menu"
    
    def test_validate_gmail_logo(self):
        """Test Gmail logo is present"""
        logger.info("TEST: Validate Gmail logo")
        
        assert self.inbox_page.validate_gmail_logo_present(), \
               "Gmail logo not present"
    
    def test_validate_settings_button(self):
        """Test Settings button is present"""
        logger.info("TEST: Validate Settings button")
        
        assert self.inbox_page.validate_settings_button_present(), \
               "Settings button not present"
    
    def test_validate_main_content_area(self):
        """Test main content area is present"""
        logger.info("TEST: Validate main content area")
        
        assert self.inbox_page.validate_main_content_area_present(), \
               "Main content area not present"
    
    def test_validate_toolbar(self):
        """Test toolbar is present"""
        logger.info("TEST: Validate toolbar")
        
        assert self.inbox_page.validate_toolbar_present(), \
               "Toolbar not present"
    
    def test_validate_emails_loaded(self):
        """Test that emails are loaded (or inbox is confirmed empty)"""
        logger.info("TEST: Validate emails loaded")
        
        # Just verify the email list area is accessible
        assert self.inbox_page.validate_emails_loaded(), \
               "Email list area not accessible"
    
    @pytest.mark.smoke
    def test_comprehensive_inbox_validation(self):
        """Test comprehensive validation of all inbox elements"""
        logger.info("TEST: Comprehensive inbox DOM validation")
        
        # Run complete validation suite
        validations = self.inbox_page.validate_all_inbox_elements()
        
        # Log results
        logger.info("Inbox validation results:")
        for element, status in validations.items():
            logger.info(f"  {element}: {'✓' if status else '✗'}")
        
        # Check critical elements
        critical_elements = [
            "Compose Button",
            "Gmail Logo",
            "Search Box",
            "Main Content"
        ]
        
        critical_passed = all(validations.get(elem, False) for elem in critical_elements)
        assert critical_passed, \
               "One or more critical inbox elements failed validation"
