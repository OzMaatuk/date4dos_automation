import logging
from configparser import ConfigParser
import pytest
from playwright.sync_api import sync_playwright, BrowserContext, Page
from typing import Generator, cast, Any
from logger import configure_application_logging
from pages import ItemPage
from pages import FeedPage
from utils.msg_gen import MessageGenerator
from dotenv import load_dotenv

module_logger = logging.getLogger(__name__)
load_dotenv()


@pytest.fixture(scope="session")
def config() -> ConfigParser:
    config = ConfigParser()
    config.read('pytest.ini')
    return config

@pytest.fixture(scope="session", autouse=True)
def configure_logger(config: ConfigParser):
    # Prefer pytest.ini [pytest] log_file if present
    try:
        pytest_log_file = config.get('pytest', 'log_file')
    except Exception:
        pytest_log_file = None

    log_file = pytest_log_file or config.get('Settings', 'log_file', fallback='logs/tests.log')
    log_level_name = config.get('Settings', 'log_level', fallback='DEBUG')
    logging_format = '%(asctime)s %(levelname)s %(name)s: %(message)s'
    try:
        # Convert level name like 'DEBUG' to numeric level; fall back to DEBUG
        level_num = logging.getLevelName(log_level_name)
        if isinstance(level_num, str):
            level_num = logging.DEBUG
    except Exception:
        level_num = logging.DEBUG

    try:
        configure_application_logging(level_num, log_file, logging_format)
        module_logger.info("Configured application logging: level=%s file=%s", log_level_name, log_file)
    except Exception as e:
        module_logger.error(f"Failed to configure application logging: {e}")
    return None

@pytest.fixture(scope="session")
def playwright_instance() -> Generator:
    module_logger.info("Starting Playwright instance...")
    instance = sync_playwright().start()
    yield instance
    module_logger.info("Stopping Playwright instance...")
    instance.stop()
    module_logger.info("Playwright instance stopped.")

@pytest.fixture(scope="session")
def playwright_browser(config: ConfigParser, playwright_instance) -> Generator[BrowserContext, None, None]:
    try:
        module_logger.info("Launching persistent Playwright browser context...")
        HEADLESS = config.getboolean("Settings", "headless")
        browser_context = playwright_instance.chromium.launch_persistent_context(
            user_data_dir=config.get("Settings", "browser_data_dir"),
            headless=HEADLESS
        )
        # Verify the context is usable by creating a temporary page
        temp_page = browser_context.new_page()
        temp_page.goto("about:blank")
        temp_page.close()
        module_logger.info("Persistent browser context launched and verified successfully.")
        yield browser_context
        module_logger.info("Closing persistent browser context...")
        browser_context.close()
        module_logger.info("Persistent browser context closed.")
    except Exception as e:
        module_logger.error(f"Failed to launch persistent browser context: {e}")
        raise

@pytest.fixture(scope="session")
def playwright_browser_no_data(playwright_instance, config: ConfigParser) -> Generator[BrowserContext, None, None]:
    try:
        module_logger.info("Launching non-persistent Playwright browser...")
        HEADLESS = config.getboolean("Settings", "headless")
        browser = playwright_instance.chromium.launch(headless=HEADLESS)
        context = browser.new_context()
        module_logger.info("Non-persistent browser context launched successfully.")
        yield context
        module_logger.info("Closing non-persistent browser context...")
        context.close()
        browser.close()
        module_logger.info("Non-persistent browser closed.")
    except Exception as e:
        module_logger.error(f"Failed to launch non-persistent browser: {e}")
        raise

@pytest.fixture(scope="function")
def playwright_page(playwright_browser: BrowserContext) -> Generator[Page, None, None]:
    page: Page | None = None
    try:
        page = playwright_browser.new_page()
        module_logger.info("New page created successfully.")
        page.goto("about:blank")
        module_logger.info("Test page loaded successfully.")
        yield page
        module_logger.info("Closing test page...")
        page.close()
        module_logger.info("Test page closed.")
    except Exception as e:
        module_logger.error(f"Failed to create or manage page: {e}")
        if page is not None:
            try:
                page.close()
            except:
                pass
        raise

@pytest.fixture(scope="function")
def playwright_page_no_data(playwright_browser_no_data: BrowserContext) -> Generator[Page, None, None]:
    try:
        page = playwright_browser_no_data.new_page()
        module_logger.info("New page created successfully.")
        page.goto("about:blank")
        module_logger.info("Test page loaded successfully.")
        yield page
        module_logger.info("Closing test page...")
        page.close()
        module_logger.info("Test page closed.")
    except Exception as e:
        module_logger.error(f"Failed to create or manage page: {e}")
        raise
    
@pytest.fixture(scope="function")
def feed_page(playwright_page):
    return FeedPage(playwright_page)

@pytest.fixture(scope="function")
def item_page(playwright_page, config):
    TEST_ID = config.get("Settings", "test_id")
    return ItemPage(playwright_page, TEST_ID)

from langchain.chat_models.base import BaseChatModel

@pytest.fixture
def mock_msg_gen(mocker):
    msggen = MessageGenerator(method="llm")
    mock_llm = mocker.Mock(spec=BaseChatModel)
    msggen.llm = mock_llm
    mock_response = mocker.Mock()
    mock_response.content = "Generated text"
    mock_invoke = cast(Any, msggen.llm).invoke
    mock_invoke.return_value = mock_response
    return msggen

@pytest.fixture
def message_generator():
    return MessageGenerator()