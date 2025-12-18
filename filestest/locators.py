"""
Gmail DOM Element Locators
Contains all CSS selectors, XPath expressions, and data-testid for Gmail pages
"""


class LoginPageLocators:
    """Locators for Gmail/Google login page"""
    
    # Email Step
    EMAIL_INPUT = 'input[type="email"]'
    EMAIL_INPUT_ID = '#identifierId'
    EMAIL_NEXT_BUTTON = '#identifierNext button'
    EMAIL_NEXT_BUTTON_XPATH = '//button[.//span[text()="Next"]]'
    
    # Password Step
    PASSWORD_INPUT = 'input[type="password"][name="Passwd"]'
    PASSWORD_INPUT_XPATH = '//input[@type="password" and @name="Passwd"]'
    PASSWORD_NEXT_BUTTON = '#passwordNext button'
    PASSWORD_NEXT_BUTTON_XPATH = '//button[.//span[text()="Next"]]'
    
    # Error Messages
    EMAIL_ERROR = '#identifierId-error'
    EMAIL_ERROR_XPATH = '//*[@id="identifierId"]/following-sibling::div[@class="Ekjuhf Jj6Lae"]'
    PASSWORD_ERROR = 'div[jsname="B34EJ"]'
    PASSWORD_ERROR_XPATH = '//div[@jsname="B34EJ"]'
    
    # Page Elements
    GOOGLE_LOGO = 'img[alt="Google"]'
    SIGNIN_HEADING = 'h1[data-a11y-title-piece]'
    SIGNIN_HEADING_XPATH = '//h1[@data-a11y-title-piece]'
    
    # Privacy & Terms Links
    PRIVACY_LINK = 'a[href*="policies.google.com/privacy"]'
    TERMS_LINK = 'a[href*="policies.google.com/terms"]'
    
    # Language Selector
    LANGUAGE_SELECTOR = 'select[aria-label*="language"]'
    
    # Help Link
    HELP_LINK = 'a[aria-label*="Help"]'


class GmailInboxLocators:
    """Locators for Gmail inbox page"""
    
    # Main Navigation
    COMPOSE_BUTTON = 'div[role="button"][gh="cm"]'
    COMPOSE_BUTTON_XPATH = '//div[@role="button" and @gh="cm"]'
    COMPOSE_BUTTON_TEXT = 'div.T-I-KE'
    
    # Gmail Logo
    GMAIL_LOGO = 'a[aria-label*="Gmail"]'
    GMAIL_LOGO_XPATH = '//a[@aria-label and contains(@aria-label, "Gmail")]'
    
    # Search Box
    SEARCH_BOX = 'input[aria-label="Search mail"]'
    SEARCH_BOX_XPATH = '//input[@aria-label="Search mail"]'
    
    # Navigation Menu
    INBOX_LINK = 'a[title="Inbox"]'
    INBOX_LINK_XPATH = '//a[@title="Inbox"]'
    STARRED_LINK = 'a[href*="#starred"]'
    SENT_LINK = 'a[href*="#sent"]'
    DRAFTS_LINK = 'a[href*="#drafts"]'
    
    # User Profile/Account Menu
    PROFILE_BUTTON = 'a[aria-label*="Google Account"]'
    PROFILE_BUTTON_XPATH = '//a[contains(@aria-label, "Google Account")]'
    PROFILE_IMAGE = 'img[data-iml][alt*="Profile"]'
    
    # Account Menu Items (appears after clicking profile)
    ACCOUNT_MENU = 'div[role="menu"]'
    SIGN_OUT_BUTTON = 'a[href*="Logout"]'
    SIGN_OUT_BUTTON_XPATH = '//a[contains(@href, "Logout")]'
    SIGN_OUT_ALL_ACCOUNTS = '//div[@role="link" and contains(text(), "Sign out of all accounts")]'
    
    # Settings Icon
    SETTINGS_BUTTON = 'button[aria-label*="Settings"]'
    SETTINGS_BUTTON_XPATH = '//button[contains(@aria-label, "Settings")]'
    
    # Email List
    EMAIL_ROW = 'tr[role="row"]'
    EMAIL_ROW_XPATH = '//tr[@role="row"]'
    UNREAD_EMAILS = 'tr.zE'
    
    # Main Content Area
    MAIN_CONTENT = 'div[role="main"]'
    
    # Loading Indicators
    LOADING_INDICATOR = 'div[aria-label="Loading"]'
    
    # Toolbar
    TOOLBAR = 'div[role="toolbar"]'
    SELECT_ALL_CHECKBOX = 'div[role="checkbox"][aria-label*="Select"]'
    
    # Side Panel
    SIDE_PANEL = 'div[role="complementary"]'
    
    # Categories/Labels
    LABEL_LIST = 'div[data-tooltip*="label"]'


class LogoutPageLocators:
    """Locators for logout confirmation page"""
    
    # Signed Out Message
    SIGNED_OUT_MESSAGE = 'h1:has-text("Choose an account")'
    SIGNED_OUT_HEADING = '//h1[contains(text(), "Choose an account")]'
    
    # Account Selection
    ACCOUNT_BUTTON = 'div[data-identifier]'
    ADD_ACCOUNT_BUTTON = 'div[data-identifier]:has-text("Use another account")'
    
    # Sign in to another account
    USE_ANOTHER_ACCOUNT = '//div[contains(text(), "Use another account")]'
    
    # Remove account option
    REMOVE_ACCOUNT = 'div[aria-label*="Remove"]'


class CommonLocators:
    """Common locators used across pages"""
    
    # Loading states
    SPINNER = 'div[role="progressbar"]'
    LOADING = '*[aria-busy="true"]'
    
    # Buttons
    BUTTON_GENERIC = 'button'
    LINK_GENERIC = 'a'
    
    # Forms
    INPUT_GENERIC = 'input'
    TEXTAREA_GENERIC = 'textarea'
    
    # Alerts/Notifications
    ALERT = 'div[role="alert"]'
    NOTIFICATION = 'div[role="status"]'
    
    # Modal/Dialog
    DIALOG = 'div[role="dialog"]'
    MODAL_CLOSE = 'button[aria-label*="Close"]'
