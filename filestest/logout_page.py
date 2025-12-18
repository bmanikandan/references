"""
Gmail Logout Page Object
Handles all logout-related validations
"""
from pages.base_page import BasePage
from config.locators import LogoutPageLocators
from playwright.sync_api import expect
import logging

logger = logging.getLogger(__name__)


class LogoutPage(BasePage):
    """Gmail Logout Page Object"""
    
    def __init__(self, page):
        super().__init__(page)
        self.locators = LogoutPageLocators()
    
    # DOM Element Validation Methods
    
    def validate_on_logout_page(self) -> bool:
        """Validate user is on logout/account selection page"""
        logger.info("Validating logout page")
        
        # Check URL
        current_url = self.get_current_url()
        is_accounts_page = "accounts.google.com" in current_url
        
        logger.info(f"Current URL: {current_url}, Is accounts page: {is_accounts_page}")
        return is_accounts_page
    
    def validate_choose_account_heading_present(self) -> bool:
        """Validate 'Choose an account' heading is present"""
        logger.info("Validating 'Choose an account' heading")
        try:
            return self.is_visible(self.locators.SIGNED_OUT_MESSAGE, timeout=10000)
        except Exception:
            # Try XPath selector
            try:
                return self.is_visible(self.locators.SIGNED_OUT_HEADING, timeout=5000)
            except Exception:
                logger.warning("Could not find 'Choose an account' heading")
                return False
    
    def validate_account_button_present(self) -> bool:
        """Validate account selection button is present"""
        logger.info("Validating account button presence")
        return self.is_visible(self.locators.ACCOUNT_BUTTON, timeout=10000)
    
    def validate_use_another_account_present(self) -> bool:
        """Validate 'Use another account' option is present"""
        logger.info("Validating 'Use another account' option")
        try:
            return self.is_visible(self.locators.USE_ANOTHER_ACCOUNT, timeout=5000)
        except Exception:
            logger.warning("'Use another account' option not found")
            return False
    
    def validate_successfully_logged_out(self) -> bool:
        """Validate user has successfully logged out"""
        logger.info("Validating successful logout")
        
        # Check multiple indicators
        checks = {
            "On Accounts Page": self.validate_on_logout_page(),
            "Choose Account Present": self.validate_choose_account_heading_present() or 
                                     self.validate_account_button_present()
        }
        
        all_passed = all(checks.values())
        if all_passed:
            logger.info("Successfully validated logout")
        else:
            failed = [k for k, v in checks.items() if not v]
            logger.error(f"Logout validation failed for: {', '.join(failed)}")
        
        return all_passed
    
    # Complete DOM Validation Suite
    
    def validate_all_logout_page_elements(self):
        """Validate all DOM elements on logout page"""
        logger.info("Starting comprehensive logout page DOM validation")
        
        validations = {
            "On Logout Page": self.validate_on_logout_page(),
            "Choose Account Heading": self.validate_choose_account_heading_present(),
            "Account Button": self.validate_account_button_present(),
            "Use Another Account": self.validate_use_another_account_present()
        }
        
        logger.info(f"Logout page validation results: {validations}")
        
        # At least the page URL and one other element should be valid
        if not validations["On Logout Page"]:
            raise AssertionError("Not on logout/accounts page")
        
        # At least one account selection element should be present
        account_elements = [
            validations["Choose Account Heading"],
            validations["Account Button"]
        ]
        
        if not any(account_elements):
            raise AssertionError("No account selection elements found on logout page")
        
        logger.info("Logout page DOM validation completed")
        return validations
