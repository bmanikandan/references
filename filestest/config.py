"""
Configuration module for test settings
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for test settings"""
    
    # Gmail Credentials
    GMAIL_EMAIL = os.getenv('GMAIL_EMAIL', '')
    GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD', '')
    
    # URLs
    GMAIL_URL = os.getenv('GMAIL_URL', 'https://mail.google.com')
    GOOGLE_ACCOUNTS_URL = os.getenv('GOOGLE_ACCOUNTS_URL', 'https://accounts.google.com')
    
    # Browser Settings
    BROWSER = os.getenv('BROWSER', 'chromium')
    HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'
    SLOW_MO = int(os.getenv('SLOW_MO', '500'))
    
    # Timeouts (in milliseconds)
    DEFAULT_TIMEOUT = int(os.getenv('DEFAULT_TIMEOUT', '30000'))
    NAVIGATION_TIMEOUT = int(os.getenv('NAVIGATION_TIMEOUT', '60000'))
    
    # Screenshot Configuration
    SCREENSHOT_ON_FAILURE = os.getenv('SCREENSHOT_ON_FAILURE', 'True').lower() == 'true'
    SCREENSHOT_DIR = Path(os.getenv('SCREENSHOT_DIR', 'reports/screenshots'))
    
    # Video Recording
    VIDEO_RECORDING = os.getenv('VIDEO_RECORDING', 'True').lower() == 'true'
    VIDEO_DIR = Path(os.getenv('VIDEO_DIR', 'reports/videos'))
    
    # Test Environment
    TEST_ENV = os.getenv('TEST_ENV', 'staging')
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.GMAIL_EMAIL or cls.GMAIL_EMAIL == 'your_test_email@gmail.com':
            raise ValueError("GMAIL_EMAIL must be set in .env file")
        if not cls.GMAIL_PASSWORD or cls.GMAIL_PASSWORD == 'your_test_password':
            raise ValueError("GMAIL_PASSWORD must be set in .env file")
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories for reports"""
        cls.SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        cls.VIDEO_DIR.mkdir(parents=True, exist_ok=True)
