"""
Gmail Login Page Object
Handles all login-related actions and DOM validations
"""
from pages.base_page import BasePage
from config.locators import LoginPageLocators
from playwright.sync_api import expect
import logging

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Gmail Login Page Object"""
    
    def __init__(self, page):
        super().__init__(page)
        self.locators = LoginPageLocators()
    
    def navigate_to_gmail(self):
        """Navigate to Gmail login page"""
        logger.info("Navigating to Gmail")
        self.navigate_to("https://mail.google.com")
        self.wait_for_load_state()
    
    # DOM Element Validation Methods
    
    def validate_email_input_present(self) -> bool:
        """Validate email input field is present"""
        logger.info("Validating email input field presence")
        return self.is_visible(self.locators.EMAIL_INPUT_ID, timeout=10000)
    
    def validate_email_input_attributes(self):
        """Validate email input field DOM attributes"""
        logger.info("Validating email input field attributes")
        email_input = self.page.locator(self.locators.EMAIL_INPUT_ID)
        
        # Check input type
        expect(email_input).to_have_attribute("type", "email")
        
        # Check if it's enabled
        expect(email_input).to_be_enabled()
        
        # Check if it's visible
        expect(email_input).to_be_visible()
        
        logger.info("Email input field attributes validated successfully")
    
    def validate_email_next_button_present(self) -> bool:
        """Validate Next button is present on email page"""
        logger.info("Validating Next button presence")
        return self.is_visible(self.locators.EMAIL_NEXT_BUTTON, timeout=10000)
    
    def validate_google_logo_present(self) -> bool:
        """Validate Google logo is present"""
        logger.info("Validating Google logo presence")
        return self.is_visible(self.locators.GOOGLE_LOGO, timeout=10000)
    
    def validate_signin_heading_text(self, expected_text: str = "Sign in"):
        """Validate sign in heading text"""
        logger.info("Validating sign in heading text")
        heading = self.page.locator(self.locators.SIGNIN_HEADING_XPATH)
        expect(heading).to_contain_text(expected_text)
    
    def validate_privacy_terms_links_present(self) -> bool:
        """Validate Privacy and Terms links are present"""
        logger.info("Validating Privacy and Terms links")
        privacy_visible = self.is_visible(self.locators.PRIVACY_LINK, timeout=5000)
        terms_visible = self.is_visible(self.locators.TERMS_LINK, timeout=5000)
        return privacy_visible and terms_visible
    
    def validate_password_input_present(self) -> bool:
        """Validate password input field is present"""
        logger.info("Validating password input field presence")
        return self.is_visible(self.locators.PASSWORD_INPUT, timeout=10000)
    
    def validate_password_input_attributes(self):
        """Validate password input field DOM attributes"""
        logger.info("Validating password input field attributes")
        password_input = self.page.locator(self.locators.PASSWORD_INPUT)
        
        # Check input type
        expect(password_input).to_have_attribute("type", "password")
        
        # Check name attribute
        expect(password_input).to_have_attribute("name", "Passwd")
        
        # Check if it's enabled
        expect(password_input).to_be_enabled()
        
        # Check if it's visible
        expect(password_input).to_be_visible()
        
        logger.info("Password input field attributes validated successfully")
    
    def validate_password_next_button_present(self) -> bool:
        """Validate Next button is present on password page"""
        logger.info("Validating password Next button presence")
        return self.is_visible(self.locators.PASSWORD_NEXT_BUTTON, timeout=10000)
    
    # Action Methods
    
    def enter_email(self, email: str):
        """Enter email address"""
        logger.info(f"Entering email: {email}")
        self.wait_for_selector(self.locators.EMAIL_INPUT_ID)
        self.fill(self.locators.EMAIL_INPUT_ID, email)
    
    def click_email_next(self):
        """Click Next button on email page"""
        logger.info("Clicking Next button on email page")
        self.click(self.locators.EMAIL_NEXT_BUTTON)
        # Wait for password page to load
        self.wait_for_selector(self.locators.PASSWORD_INPUT, timeout=15000)
    
    def enter_password(self, password: str):
        """Enter password"""
        logger.info("Entering password")
        self.wait_for_selector(self.locators.PASSWORD_INPUT)
        self.fill(self.locators.PASSWORD_INPUT, password)
    
    def click_password_next(self):
        """Click Next button on password page"""
        logger.info("Clicking Next button on password page")
        self.click(self.locators.PASSWORD_NEXT_BUTTON)
    
    def login(self, email: str, password: str):
        """Complete login flow"""
        logger.info(f"Starting login flow for {email}")
        
        # Enter email
        self.enter_email(email)
        self.click_email_next()
        
        # Enter password
        self.enter_password(password)
        self.click_password_next()
        
        # Wait for navigation to Gmail
        logger.info("Waiting for Gmail inbox to load")
        try:
            self.page.wait_for_url("**/mail.google.com/**", timeout=30000)
            logger.info("Successfully logged in")
        except Exception as e:
            logger.error(f"Login failed or timeout: {str(e)}")
            raise
    
    # Error Validation Methods
    
    def validate_email_error_displayed(self) -> bool:
        """Check if email error message is displayed"""
        logger.info("Checking for email error message")
        return self.is_visible(self.locators.EMAIL_ERROR, timeout=5000)
    
    def validate_password_error_displayed(self) -> bool:
        """Check if password error message is displayed"""
        logger.info("Checking for password error message")
        return self.is_visible(self.locators.PASSWORD_ERROR, timeout=5000)
    
    def get_email_error_text(self) -> str:
        """Get email error message text"""
        if self.validate_email_error_displayed():
            return self.get_text(self.locators.EMAIL_ERROR)
        return ""
    
    def get_password_error_text(self) -> str:
        """Get password error message text"""
        if self.validate_password_error_displayed():
            return self.get_text(self.locators.PASSWORD_ERROR)
        return ""
    
    # Complete DOM Validation Suite
    
    def validate_all_email_page_elements(self):
        """Validate all DOM elements on email page"""
        logger.info("Starting comprehensive email page DOM validation")
        
        validations = {
            "Google Logo": self.validate_google_logo_present(),
            "Email Input": self.validate_email_input_present(),
            "Next Button": self.validate_email_next_button_present(),
            "Privacy/Terms Links": self.validate_privacy_terms_links_present()
        }
        
        # Validate attributes
        if validations["Email Input"]:
            self.validate_email_input_attributes()
        
        # Check all validations passed
        failed = [k for k, v in validations.items() if not v]
        if failed:
            raise AssertionError(f"Email page validation failed for: {', '.join(failed)}")
        
        logger.info("All email page DOM elements validated successfully")
        return True
    
    def validate_all_password_page_elements(self):
        """Validate all DOM elements on password page"""
        logger.info("Starting comprehensive password page DOM validation")
        
        validations = {
            "Password Input": self.validate_password_input_present(),
            "Next Button": self.validate_password_next_button_present()
        }
        
        # Validate attributes
        if validations["Password Input"]:
            self.validate_password_input_attributes()
        
        # Check all validations passed
        failed = [k for k, v in validations.items() if not v]
        if failed:
            raise AssertionError(f"Password page validation failed for: {', '.join(failed)}")
        
        logger.info("All password page DOM elements validated successfully")
        return True
