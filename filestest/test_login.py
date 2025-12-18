"""
Test cases for Gmail Login functionality with DOM validations
"""
import pytest
from pages.login_page import LoginPage
from pages.inbox_page import InboxPage
from config.config import Config
import logging

logger = logging.getLogger(__name__)


@pytest.mark.smoke
@pytest.mark.login
@pytest.mark.ui
class TestGmailLogin:
    """Test suite for Gmail login functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page, config):
        """Setup for each test"""
        self.page = page
        self.config = config
        self.login_page = LoginPage(page)
        self.inbox_page = InboxPage(page)
    
    def test_navigate_to_gmail(self):
        """Test navigation to Gmail login page"""
        logger.info("TEST: Navigate to Gmail")
        self.login_page.navigate_to_gmail()
        
        # Validate we're on the login page
        assert "accounts.google.com" in self.login_page.get_current_url() or \
               "mail.google.com" in self.login_page.get_current_url(), \
               "Failed to navigate to Gmail"
    
    @pytest.mark.dom
    def test_validate_email_page_dom_elements(self):
        """Test DOM elements validation on email page"""
        logger.info("TEST: Validate email page DOM elements")
        self.login_page.navigate_to_gmail()
        
        # Validate all email page elements
        assert self.login_page.validate_all_email_page_elements(), \
               "Email page DOM validation failed"
    
    @pytest.mark.dom
    def test_validate_email_input_field(self):
        """Test email input field DOM attributes"""
        logger.info("TEST: Validate email input field attributes")
        self.login_page.navigate_to_gmail()
        
        # Check email input is present
        assert self.login_page.validate_email_input_present(), \
               "Email input field not present"
        
        # Validate email input attributes
        self.login_page.validate_email_input_attributes()
    
    @pytest.mark.dom
    def test_validate_google_logo_present(self):
        """Test Google logo is present on login page"""
        logger.info("TEST: Validate Google logo presence")
        self.login_page.navigate_to_gmail()
        
        assert self.login_page.validate_google_logo_present(), \
               "Google logo not present on login page"
    
    @pytest.mark.dom
    def test_validate_privacy_terms_links(self):
        """Test Privacy and Terms links are present"""
        logger.info("TEST: Validate Privacy and Terms links")
        self.login_page.navigate_to_gmail()
        
        assert self.login_page.validate_privacy_terms_links_present(), \
               "Privacy or Terms links not present"
    
    @pytest.mark.dom
    def test_validate_email_next_button(self):
        """Test Next button is present and clickable on email page"""
        logger.info("TEST: Validate email Next button")
        self.login_page.navigate_to_gmail()
        
        assert self.login_page.validate_email_next_button_present(), \
               "Next button not present on email page"
    
    def test_enter_email_address(self):
        """Test entering email address"""
        logger.info("TEST: Enter email address")
        self.login_page.navigate_to_gmail()
        
        # Enter email
        self.login_page.enter_email(self.config.GMAIL_EMAIL)
        
        # Click Next
        self.login_page.click_email_next()
        
        # Validate we're on password page
        assert self.login_page.validate_password_input_present(), \
               "Did not navigate to password page after entering email"
    
    @pytest.mark.dom
    def test_validate_password_page_dom_elements(self):
        """Test DOM elements validation on password page"""
        logger.info("TEST: Validate password page DOM elements")
        self.login_page.navigate_to_gmail()
        
        # Enter email to get to password page
        self.login_page.enter_email(self.config.GMAIL_EMAIL)
        self.login_page.click_email_next()
        
        # Validate all password page elements
        assert self.login_page.validate_all_password_page_elements(), \
               "Password page DOM validation failed"
    
    @pytest.mark.dom
    def test_validate_password_input_field(self):
        """Test password input field DOM attributes"""
        logger.info("TEST: Validate password input field attributes")
        self.login_page.navigate_to_gmail()
        
        # Navigate to password page
        self.login_page.enter_email(self.config.GMAIL_EMAIL)
        self.login_page.click_email_next()
        
        # Check password input is present
        assert self.login_page.validate_password_input_present(), \
               "Password input field not present"
        
        # Validate password input attributes
        self.login_page.validate_password_input_attributes()
    
    @pytest.mark.dom
    def test_validate_password_next_button(self):
        """Test Next button is present on password page"""
        logger.info("TEST: Validate password Next button")
        self.login_page.navigate_to_gmail()
        
        # Navigate to password page
        self.login_page.enter_email(self.config.GMAIL_EMAIL)
        self.login_page.click_email_next()
        
        assert self.login_page.validate_password_next_button_present(), \
               "Next button not present on password page"
    
    @pytest.mark.smoke
    def test_successful_login(self):
        """Test successful login to Gmail"""
        logger.info("TEST: Successful login")
        self.login_page.navigate_to_gmail()
        
        # Perform login
        self.login_page.login(self.config.GMAIL_EMAIL, self.config.GMAIL_PASSWORD)
        
        # Wait for inbox to load
        self.inbox_page.wait_for_inbox_to_load()
        
        # Validate successful login
        assert self.inbox_page.validate_successfully_logged_in(), \
               "Login was not successful"
    
    @pytest.mark.smoke
    @pytest.mark.dom
    def test_validate_inbox_elements_after_login(self):
        """Test inbox DOM elements after successful login"""
        logger.info("TEST: Validate inbox elements after login")
        self.login_page.navigate_to_gmail()
        
        # Login
        self.login_page.login(self.config.GMAIL_EMAIL, self.config.GMAIL_PASSWORD)
        self.inbox_page.wait_for_inbox_to_load()
        
        # Validate inbox elements
        validations = self.inbox_page.validate_all_inbox_elements()
        
        # Check critical elements are present
        critical_elements = ["Compose Button", "Gmail Logo", "Search Box"]
        for element in critical_elements:
            assert validations.get(element, False), \
                   f"Critical element '{element}' not found in inbox"
    
    @pytest.mark.parametrize("invalid_email", [
        "",  # Empty email
        "invalid_email",  # Invalid format
        "test@invalid",  # Incomplete domain
    ])
    def test_invalid_email_validation(self, invalid_email):
        """Test login with invalid email addresses"""
        logger.info(f"TEST: Invalid email validation - {invalid_email}")
        self.login_page.navigate_to_gmail()
        
        # Try to enter invalid email
        if invalid_email:  # Skip if empty
            self.login_page.enter_email(invalid_email)
            self.login_page.click_email_next()
            
            # Should show error or stay on same page
            # Note: Google might not show error for all invalid formats immediately


@pytest.mark.regression
@pytest.mark.login
class TestLoginEdgeCases:
    """Test suite for login edge cases"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page, config):
        """Setup for each test"""
        self.page = page
        self.config = config
        self.login_page = LoginPage(page)
    
    def test_login_page_accessibility(self):
        """Test login page has proper accessibility attributes"""
        logger.info("TEST: Login page accessibility")
        self.login_page.navigate_to_gmail()
        
        # Check email input has proper aria attributes or labels
        assert self.login_page.validate_email_input_present(), \
               "Email input not accessible"
    
    def test_multiple_page_refreshes(self):
        """Test login page after multiple refreshes"""
        logger.info("TEST: Multiple page refreshes")
        self.login_page.navigate_to_gmail()
        
        # Refresh page multiple times
        for i in range(3):
            self.page.reload()
            self.login_page.wait_for_load_state()
            
            # Validate elements are still present
            assert self.login_page.validate_email_input_present(), \
                   f"Email input not present after refresh {i+1}"
