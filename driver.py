import logging
from typing import Optional
from contextlib import contextmanager
from playwright.sync_api import sync_playwright, Page, BrowserContext, Playwright
from constants.settings import Settings

logger = logging.getLogger(__name__)

# TODO: channel also can be configurable.
class PlaywrightDriver:
    """Basic Playwright driver operations with context manager support."""
    
    def __init__(self, headless: bool = Settings().HEADLESS, 
                 timeout: int = Settings().TIMEOUT, 
                 user_data_dir: str = ""):
        self.headless = headless
        self.timeout = timeout
        self.user_data_dir = user_data_dir
        self._playwright: Optional[Playwright] = None
        self._browser_context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
    def __enter__(self):
        self.initialize()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
            
    def initialize(self):
        """Initializes Playwright, browser context, and page."""
        logger.info("Initializing Playwright driver...")
        try:
            self._playwright = sync_playwright().start()
            
            browser_args = [
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--no-sandbox',
            ]
            
            # Launch browser
            self._browser_context = self._playwright.chromium.launch_persistent_context(
                user_data_dir=self.user_data_dir,
                headless=self.headless,
                ignore_https_errors=True,
                timeout=self.timeout,
                channel="msedge",
                args=browser_args,
            )
            
            # Initialize page with proper null check
            if self._browser_context and self._browser_context.pages:
                self.page = self._browser_context.pages[0]
            elif self._browser_context:
                self.page = self._browser_context.new_page()
            else:
                raise Exception("Failed to create browser context")
                
            self.page.set_default_timeout(self.timeout)
            logger.info("Playwright browser and page successfully initialized.")
            
        except Exception as e:
            logger.error(f"Failed to initialize Playwright driver: {e}", exc_info=True)
            self.close()
            raise
        
    def close(self) -> None:
        """Closes the browser context and stops Playwright."""
        logger.info("Closing Playwright resources...")
        try:
            if self._browser_context:
                self._browser_context.close()
                self._browser_context = None
                self.page = None
            if self._playwright:
                self._playwright.stop()
                self._playwright = None
            logger.debug("Playwright resources closed.")
        except Exception as e:
            logger.error(f"Error while closing Playwright resources: {e}", exc_info=True)

@contextmanager
def create_driver(headless: bool = Settings().HEADLESS, 
                  timeout: int = Settings().TIMEOUT,
                  user_data_dir: str = Settings().BROWSER_DATA):
    """Context manager for creating and managing PlaywrightDriver."""
    driver = PlaywrightDriver(headless=headless, timeout=timeout, user_data_dir=user_data_dir)
    driver.initialize()
    try:
        yield driver
    finally:
        driver.close()