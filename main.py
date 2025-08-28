from controller.controller import Controller
from constants.settings import Settings
from driver import PlaywrightDriver
import logging

from logger import configure_application_logging
logger = logging.getLogger(__name__)



def main():
    logger.info("Starting main application.")
    configure_application_logging(Settings().LOG_LEVEL, Settings().LOG_FILE, Settings().LOG_FORMAT)
    headless: bool = Settings().HEADLESS
    browser_data = Settings().BROWSER_DATA
    browser_type = Settings().BROWSER_TYPE
    timeout = Settings().TIMEOUT

    with PlaywrightDriver(headless, timeout, browser_data) as browser:
        if not browser.page:
            raise Exception("Failed to initialize browser page")

        controller = Controller(browser.page)
        controller.run(Settings().USERNAME, Settings().PASSWORD, Settings().LIMIT)

if __name__ == "__main__":
    main()