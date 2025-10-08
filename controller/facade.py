from types import FunctionType
from typing import Callable, List
from playwright.sync_api import Page
from constants.feed_constants import ITEM_TITLE_SELECTOR
from pages.feed_page import FeedPage
from pages.item_page import ItemPage
from playwright.sync_api import Locator
import logging
logger = logging.getLogger(__name__)

class Facade:
    def __init__(self, page):
        logger.debug("Initiliazing Facade")
        self.page = page    

    def collect_items(self, filter: FunctionType, extract: FunctionType, limit: int = 0, viewed_my_profile: bool = False) -> List:
        logger.debug("Facade.collect_items")
        feed_page = FeedPage(page=self.page, viewed_my_profile=viewed_my_profile)

        def process_item(page, item):
            try:
                if filter(page, item):
                    return extract(page, item)
            except Exception as e:
                logger.error(f"Error processing item: {e}")
            return None
        
        res = feed_page.iterate_over_items(process_item, limit)
        return [item for item in (res or []) if item is not None]
    
    def apply_filters(self, filters: dict) -> None:
        logger.debug("Facade.apply_filters")
        return
        # TODO
        # implement more filter functions for each filter option in feed_page
        feed_page = FeedPage(self.page)
        try:
            feed_page.filter_min_age(filters['min_age'])
        except Exception as e:
            logger.error(f"Error applying min_age filter: {e}")
        try:
            feed_page.filter_min_age(filters['max_age'])
        except Exception as e:
            logger.error(f"Error applying max_age filter: {e}")
        try:
            feed_page.filter_high(filters['high'])
        except Exception as e:
            logger.error(f"Error applying high filter: {e}")
    
    @staticmethod
    def item_action(page: Page, id: str, create_message: Callable[[str], str]) -> None:
        logger.debug("Facade.operate_on_item")
        try:
            item_page = ItemPage(page, id)
            item_details = item_page.get_info()
            msg = create_message(item_details)
            item_page.send_message(msg)
        except Exception as e:
            logger.error(f"Error performing action on item {id}: {e}")

    @staticmethod
    def filter_item(page: Page, item: ItemPage, filter_description: str = "") -> bool:
        logger.debug("Facade.filter_item")
        if not filter_description:
            filter_description = "just answer yes."
        # TODO: should use llm to filter items
        return True
    
    @staticmethod
    def extract_id(page: Page, item: Locator) -> str:
        logger.debug("Facade.extract_id")
        url = item.locator(ITEM_TITLE_SELECTOR).nth(0).get_attribute("href")
        if url:
            id = url.split('/')[-2]
            if len(id) in range(4, 10):
                return id
        logger.error("Could not extract item id.")
        return ""

    def close(self):
        pass