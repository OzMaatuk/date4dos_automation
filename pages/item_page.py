from constants.settings import Settings
from playwright.sync_api import Page, TimeoutError
from constants.item_constants import ITEM_DETAILS, ITEM_URL_SUFFIX, MESSAGE_INPUT, SEND_MESSAGE_BUTTON
import logging
logger = logging.getLogger(__name__)

class ItemPage:
    def __init__(self, page: Page, id: str):
        logger.debug("Initiliazing ItemPage")
        self.page = page
        self.id = id
        base_url = Settings().BASE_URL
        self.url = f"{base_url}{ITEM_URL_SUFFIX}{id}"
        try:
            page.goto(self.url)
            self.page.wait_for_load_state(state="networkidle")
        except TimeoutError:
            logger.error(f"Failed to load item page for ID: {id}")
            raise Exception(f"Item page for ID {id} could not be loaded.")
        
    def get_info(self) -> str:
        logger.debug("ItemPage.get_info")
        try:
            profile_info = self.page.locator(ITEM_DETAILS).inner_text()
            return profile_info
        except Exception as e:
            logger.error(f"Failed to retrieve item details: {e}")
            raise Exception("Item details could not be retrieved.")
    
    def send_message(self, message: str) -> None:
        logger.debug("ItemPage.send_message")
        try:
            self.page.fill(MESSAGE_INPUT, message, force=True)
            self.page.click(SEND_MESSAGE_BUTTON, force=True)
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            raise Exception("Message could not be sent.")