from types import FunctionType
from typing import List
from playwright.sync_api import Page
from constants.feed_constants import ADVANCED_SEARCH_SELECTOR, FEED_ITEMS_SELECTOR, SEARCH_URL_SUFFIX, VIEWS_URL_SUFFIX, NUM_OF_VIEWS_SELECTOR
from constants.settings import Settings
import logging
logger = logging.getLogger(__name__)

class FeedPage:
    def __init__(self, page: Page, reload : bool = False, viewed_my_profile: bool = False):
        logger.debug("Initiliazing FeedPage")
        self.page = page
        url = Settings().BASE_URL
        if viewed_my_profile: url += VIEWS_URL_SUFFIX
        else: url += SEARCH_URL_SUFFIX
        if url not in self.page.url or reload:
            self.page.goto(url)
            self.page.wait_for_load_state(state="networkidle")
            try:
                self.page.click(ADVANCED_SEARCH_SELECTOR)
            except Exception as e:
                logger.error(f"Could not open advanded search: {e}")

    def scroll_to_bottom(self) -> None:
        logger.debug("FeedPage.scroll_to_bottom")
        self.page.locator(FEED_ITEMS_SELECTOR).evaluate("node => node.scrollTop = node.scrollHeight")
        self.page.wait_for_timeout(500)

    def iterate_over_items(self, process_item: FunctionType, limit: int = 0) -> List:
        logger.debug("FeedPage.iterate_over_items")
        res = []

        num_of_scroll_downs = limit
        for i in range(num_of_scroll_downs):
            self.scroll_to_bottom()

        # Locate the search results container
        search_results = self.page.locator(FEED_ITEMS_SELECTOR)
        if not search_results.is_visible():
            raise Exception("Search results container not found or not visible.")

        # Find all item elements within the search results
        items = search_results.locator('div.member_div').all()
        logger.info(f"Found {len(items)} items in search results.")

        # Iterate over each item
        for index, item in enumerate(items):
            try:
                res.append(process_item(self.page, item))
                if index >= limit:
                    break
            except Exception as e:
                logger.error(f"Error processing item {index}: {e}")
        
        return res

    def get_num_of_views(self) -> int:
        logger.debug("FeedPage.get_num_of_views")
        res = 0
        try:
            res = 0 # int(self.page.locator(NUM_OF_VIEWS).inner_text(timeout=1000))
        except Exception:
            logger.error("Could not parse number of views.")
        return res