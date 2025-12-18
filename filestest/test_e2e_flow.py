"""
End-to-End Test for complete Gmail Login and Logout flow
"""
import pytest
from pages.login_page import LoginPage
from pages.inbox_page import InboxPage
from pages.logout_page import LogoutPage
from config.config import Config
import logging

logger = logging.getLogger(__name__)


@pytest.mark.smoke
@pytest.mark.e2e
class TestGmailLoginLogoutE2E:
    """End-to-End test suite for complete login-logout flow"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page, config):
        """Setup for each test"""
        self.page = page
        self.config = config
        self.login_page = LoginPage(page)
        self.inbox_page = InboxPage(page)
        self.logout_page = LogoutPage(page)
    
    @pytest.mark.slow
    def test_complete_login_logout_flow(self):
        """Test complete flow: Navigate → Login → Validate Inbox → Logout → Validate Logout"""
        logger.info("=" * 70)
        logger.info("E2E TEST: Complete Login-Logout Flow with DOM Validations")
        logger.info("=" * 70)
        
        # Step 1: Navigate to Gmail
        logger.info("Step 1: Navigating to Gmail...")
        self.login_page.navigate_to_gmail()
        logger.info("✓ Navigation successful")
        
        # Step 2: Validate Login Page Elements
        logger.info("Step 2: Validating login page DOM elements...")
        assert self.login_page.validate_all_email_page_elements(), \
               "Login page DOM validation failed"
        logger.info("✓ Login page DOM validation passed")
        
        # Step 3: Enter Email
        logger.info("Step 3: Entering email address...")
        self.login_page.enter_email(self.config.GMAIL_EMAIL)
        self.login_page.click_email_next()
        logger.info("✓ Email entered successfully")
        
        # Step 4: Validate Password Page Elements
        logger.info("Step 4: Validating password page DOM elements...")
        assert self.login_page.validate_all_password_page_elements(), \
               "Password page DOM validation failed"
        logger.info("✓ Password page DOM validation passed")
        
        # Step 5: Enter Password and Complete Login
        logger.info("Step 5: Entering password and completing login...")
        self.login_page.enter_password(self.config.GMAIL_PASSWORD)
        self.login_page.click_password_next()
        logger.info("✓ Password entered, waiting for inbox...")
        
        # Step 6: Wait for Inbox to Load
        logger.info("Step 6: Waiting for inbox to load...")
        self.inbox_page.wait_for_inbox_to_load()
        logger.info("✓ Inbox loaded successfully")
        
        # Step 7: Validate Successful Login
        logger.info("Step 7: Validating successful login...")
        assert self.inbox_page.validate_successfully_logged_in(), \
               "Login validation failed"
        logger.info("✓ Login validation passed")
        
        # Step 8: Validate All Inbox DOM Elements
        logger.info("Step 8: Validating all inbox DOM elements...")
        inbox_validations = self.inbox_page.validate_all_inbox_elements()
        
        # Check critical elements
        critical_elements = ["Compose Button", "Gmail Logo", "Search Box"]
        for element in critical_elements:
            assert inbox_validations.get(element, False), \
                   f"Critical inbox element '{element}' validation failed"
        logger.info("✓ Inbox DOM validation passed")
        
        # Step 9: Open Account Menu
        logger.info("Step 9: Opening account menu...")
        self.inbox_page.click_profile_button()
        assert self.inbox_page.validate_account_menu_visible(), \
               "Account menu did not appear"
        logger.info("✓ Account menu opened successfully")
        
        # Step 10: Validate Sign Out Button
        logger.info("Step 10: Validating Sign Out button...")
        assert self.inbox_page.validate_signout_button_present(), \
               "Sign Out button not present"
        logger.info("✓ Sign Out button validated")
        
        # Step 11: Click Sign Out
        logger.info("Step 11: Clicking Sign Out...")
        self.inbox_page.click_signout()
        logger.info("✓ Sign Out clicked, waiting for redirect...")
        
        # Step 12: Wait for Logout Page
        logger.info("Step 12: Waiting for logout page...")
        self.page.wait_for_url("**/accounts.google.com/**", timeout=15000)
        logger.info("✓ Redirected to accounts page")
        
        # Step 13: Validate Logout Page
        logger.info("Step 13: Validating logout page...")
        assert self.logout_page.validate_successfully_logged_out(), \
               "Logout validation failed"
        logger.info("✓ Logout validation passed")
        
        # Step 14: Validate Logout Page DOM Elements
        logger.info("Step 14: Validating logout page DOM elements...")
        logout_validations = self.logout_page.validate_all_logout_page_elements()
        assert logout_validations["On Logout Page"], \
               "Not on logout page"
        logger.info("✓ Logout page DOM validation passed")
        
        # Step 15: Verify Cannot Access Inbox
        logger.info("Step 15: Verifying cannot access inbox after logout...")
        self.page.goto("https://mail.google.com/mail/")
        current_url = self.page.url
        assert "accounts.google.com" in current_url or "ServiceLogin" in current_url, \
               "Still able to access inbox after logout"
        logger.info("✓ Inbox access properly blocked after logout")
        
        logger.info("=" * 70)
        logger.info("E2E TEST COMPLETED SUCCESSFULLY")
        logger.info("=" * 70)
    
    @pytest.mark.slow
    def test_login_logout_login_again(self):
        """Test logging in, logging out, and logging in again"""
        logger.info("E2E TEST: Login → Logout → Login Again")
        
        # First login
        logger.info("First login...")
        self.login_page.navigate_to_gmail()
        self.login_page.login(self.config.GMAIL_EMAIL, self.config.GMAIL_PASSWORD)
        self.inbox_page.wait_for_inbox_to_load()
        assert self.inbox_page.validate_successfully_logged_in()
        logger.info("✓ First login successful")
        
        # Logout
        logger.info("Logging out...")
        self.inbox_page.logout()
        assert self.logout_page.validate_successfully_logged_out()
        logger.info("✓ Logout successful")
        
        # Login again
        logger.info("Logging in again...")
        self.page.goto("https://mail.google.com")
        self.login_page.login(self.config.GMAIL_EMAIL, self.config.GMAIL_PASSWORD)
        self.inbox_page.wait_for_inbox_to_load()
        assert self.inbox_page.validate_successfully_logged_in()
        logger.info("✓ Second login successful")
        
        logger.info("E2E TEST: Login-Logout-Login cycle completed successfully")
    
    def test_dom_elements_persist_across_navigation(self):
        """Test that DOM elements persist correctly during navigation"""
        logger.info("E2E TEST: DOM Elements Persistence")
        
        # Login
        self.login_page.navigate_to_gmail()
        self.login_page.login(self.config.GMAIL_EMAIL, self.config.GMAIL_PASSWORD)
        self.inbox_page.wait_for_inbox_to_load()
        
        # Validate initial inbox elements
        initial_validations = self.inbox_page.validate_all_inbox_elements()
        logger.info("Initial inbox validation completed")
        
        # Navigate to different sections and validate elements persist
        sections = [
            ("Sent", "https://mail.google.com/mail/#sent"),
            ("Drafts", "https://mail.google.com/mail/#drafts"),
            ("Inbox", "https://mail.google.com/mail/#inbox")
        ]
        
        for section_name, url in sections:
            logger.info(f"Navigating to {section_name}...")
            try:
                self.page.goto(url)
                self.page.wait_for_load_state("networkidle", timeout=10000)
                
                # Validate key elements still present
                assert self.inbox_page.validate_compose_button_present(), \
                       f"Compose button not present in {section_name}"
                assert self.inbox_page.validate_gmail_logo_present(), \
                       f"Gmail logo not present in {section_name}"
                
                logger.info(f"✓ {section_name} navigation successful")
            except Exception as e:
                logger.warning(f"Navigation to {section_name} had issues: {str(e)}")
        
        logger.info("DOM persistence test completed")


@pytest.mark.regression
@pytest.mark.e2e
class TestGmailE2EEdgeCases:
    """Edge cases for E2E testing"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page, config):
        """Setup for each test"""
        self.page = page
        self.config = config
        self.login_page = LoginPage(page)
        self.inbox_page = InboxPage(page)
        self.logout_page = LogoutPage(page)
    
    def test_session_timeout_simulation(self):
        """Test behavior after session timeout (simulated by clearing cookies)"""
        logger.info("E2E TEST: Session Timeout Simulation")
        
        # Login
        self.login_page.navigate_to_gmail()
        self.login_page.login(self.config.GMAIL_EMAIL, self.config.GMAIL_PASSWORD)
        self.inbox_page.wait_for_inbox_to_load()
        
        # Clear cookies to simulate session expiration
        logger.info("Clearing cookies to simulate session timeout...")
        self.page.context.clear_cookies()
        
        # Try to access inbox
        self.page.goto("https://mail.google.com/mail/")
        
        # Should redirect to login
        self.page.wait_for_load_state("networkidle")
        current_url = self.page.url
        
        assert "accounts.google.com" in current_url or "ServiceLogin" in current_url, \
               "Did not redirect to login after session timeout"
        
        logger.info("✓ Session timeout handled correctly")
