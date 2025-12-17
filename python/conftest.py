"""
Pytest configuration and fixtures
"""
import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from config.config import Config
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler('reports/test_execution.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def config():
    """Fixture to provide configuration"""
    Config.create_directories()
    return Config


@pytest.fixture(scope="session")
def browser_type_launch_args(config):
    """Browser launch arguments"""
    return {
        "headless": config.HEADLESS,
        "slow_mo": config.SLOW_MO,
        "args": [
            "--start-maximized",
            "--disable-blink-features=AutomationControlled"
        ]
    }


@pytest.fixture(scope="session")
def browser_context_args(config):
    """Browser context arguments"""
    return {
        "viewport": None,  # Use full window size
        "locale": "en-US",
        "timezone_id": "America/New_York",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "record_video_dir": str(config.VIDEO_DIR) if config.VIDEO_RECORDING else None,
        "record_video_size": {"width": 1280, "height": 720} if config.VIDEO_RECORDING else None
    }


@pytest.fixture(scope="function")
def page(browser: Browser, browser_context_args, config) -> Page:
    """Create a new page for each test"""
    logger.info("Creating new browser context and page")
    context = browser.new_context(**browser_context_args)
    page = context.new_page()
    
    # Set default timeout
    page.set_default_timeout(config.DEFAULT_TIMEOUT)
    page.set_default_navigation_timeout(config.NAVIGATION_TIMEOUT)
    
    yield page
    
    # Cleanup
    logger.info("Closing page and context")
    page.close()
    context.close()


@pytest.fixture(scope="function")
def authenticated_page(page, config):
    """Fixture that provides an authenticated Gmail session"""
    from pages.login_page import LoginPage
    from pages.inbox_page import InboxPage
    
    logger.info("Setting up authenticated session")
    
    # Navigate and login
    login_page = LoginPage(page)
    login_page.navigate_to_gmail()
    
    try:
        login_page.login(config.GMAIL_EMAIL, config.GMAIL_PASSWORD)
        
        # Wait for inbox to load
        inbox_page = InboxPage(page)
        inbox_page.wait_for_inbox_to_load()
        
        logger.info("Authenticated session ready")
        yield page
        
    except Exception as e:
        logger.error(f"Failed to create authenticated session: {str(e)}")
        # Take screenshot on failure
        screenshot_path = config.SCREENSHOT_DIR / f"auth_failure_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        page.screenshot(path=str(screenshot_path))
        raise


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results and take screenshots on failure"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        # Get the page fixture if it exists
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            config = item.funcargs.get("config", Config)
            
            if config.SCREENSHOT_ON_FAILURE:
                # Create screenshot filename
                test_name = item.nodeid.replace("::", "_").replace("/", "_")
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = config.SCREENSHOT_DIR / f"failure_{test_name}_{timestamp}.png"
                
                try:
                    page.screenshot(path=str(screenshot_path), full_page=True)
                    logger.info(f"Screenshot saved: {screenshot_path}")
                except Exception as e:
                    logger.error(f"Failed to take screenshot: {str(e)}")


def pytest_configure(config):
    """Configure pytest"""
    # Create reports directory
    Path("reports").mkdir(exist_ok=True)
    Path("reports/screenshots").mkdir(exist_ok=True)
    Path("reports/videos").mkdir(exist_ok=True)
    
    # Register custom markers
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "login: mark test as login related")
    config.addinivalue_line("markers", "logout: mark test as logout related")
    config.addinivalue_line("markers", "ui: mark test as UI validation")
    config.addinivalue_line("markers", "dom: mark test as DOM validation")


def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    for item in items:
        # Add markers based on test name
        if "login" in item.nodeid.lower():
            item.add_marker(pytest.mark.login)
        if "logout" in item.nodeid.lower():
            item.add_marker(pytest.mark.logout)
        if "dom" in item.nodeid.lower() or "validate" in item.nodeid.lower():
            item.add_marker(pytest.mark.dom)


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment(config):
    """Setup test environment before all tests"""
    logger.info("=" * 60)
    logger.info("Setting up test environment")
    logger.info("=" * 60)
    
    # Validate configuration
    try:
        config.validate()
    except ValueError as e:
        logger.error(f"Configuration validation failed: {str(e)}")
        logger.info("Please update the .env file with valid Gmail test credentials")
        pytest.exit("Configuration validation failed")
    
    logger.info(f"Browser: {config.BROWSER}")
    logger.info(f"Headless: {config.HEADLESS}")
    logger.info(f"Gmail URL: {config.GMAIL_URL}")
    
    yield
    
    logger.info("=" * 60)
    logger.info("Test execution completed")
    logger.info("=" * 60)
