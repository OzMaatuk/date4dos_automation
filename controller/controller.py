from playwright.sync_api import Page
from controller.facade import Facade
from utils.msg_gen import MessageGenerator
import logging
logger = logging.getLogger(__name__)

class Controller:
    def __init__(self, page: Page, api_key: str = ""):
        logger.debug("Initiliazing Controller")
        self.page = page
        self.facade = Facade(page)
        self.msggen = MessageGenerator(api_key)

    def run(self, username: str, password: str, limit: int = 0):
        logger.debug("Controller.run")
        self.filter_and_send_message_to_new_ones(limit)
        # self.send_message_to_ones_who_viewed_my_profile()
        self.facade.close()
    
    def filter_and_send_message_to_new_ones(self, limit: int = 0):
        logger.debug("Controller.filter_and_send_message_to_new_ones")
        try:
            self.facade.apply_filters({})
            items = self.facade.collect_items(filter=Facade.filter_item,
                                              extract=Facade.extract_id,
                                              limit=limit,
                                              viewed_my_profile=False)
            items.reverse()
            for item_id in items:
                try:
                    Facade.item_action(self.page, item_id, self.msggen.generate)
                except Exception as e:
                    logger.error(f"Error sending message to item {item_id}: {e}")
        except Exception as e:
            logger.error(f"Error in filter_and_send_message_to_new_ones: {e}")

    def send_message_to_ones_who_viewed_my_profile(self):
        logger.debug("Controller.send_message_to_ones_who_viewed_my_profile")
        return
        try:
            # num_of_views = self.facade.get_num_of_views()
            num_of_views = 250
            items = self.facade.collect_items(filter=Facade.filter_item,
                                              extract=Facade.extract_id,
                                              limit=num_of_views,
                                              viewed_my_profile=True)
            items.reverse()
            for item_id in items:
                try:
                    Facade.item_action(self.page, item_id, self.msggen.generate)
                except Exception as e:
                    logger.error(f"Error sending message to item {item_id}: {e}")
        except Exception as e:
            logger.error(f"Error in send_message_to_ones_who_viewed_my_profile: {e}")
