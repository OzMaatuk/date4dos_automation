import re
import logging
from constants.settings import Settings
from copilot import Copilot
logger = logging.getLogger(__name__)

class MessageGenerator:
    def __init__(self, api_key: str = "",
                    prompt_file_path: str = Settings().PROMPT_FILE,
                    profile_file_path: str = Settings().PROFILE_FILE):
        logger.debug("MessageGenerator instance created")

        # Initialize Copilot
        self.llm = Copilot()

        self.prompt_file_path = prompt_file_path
        self.profile_file_path = profile_file_path

    def generate(self, item_description: str) -> str:
        logger.debug("MessageGenerator.generate")
        prompt = self.generate_prompt(item_description)
        
        # Basic chat example
        messages = [
            # {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ]

        # Stream responses
        for response in self.llm.create_completion(
            model="Copilot",
            messages=messages,
            stream=True):
            if isinstance(response, str):
                logger.debug(f"Result: {response}")
                return response
        return ""
    
    def generate_prompt(self, item_description: str) -> str:
        logger.debug("MessageGenerator.generate_prompt")
        with open(self.prompt_file_path, "r") as f: prompt = f.read()
        with open(self.profile_file_path, "r") as f: user_profile = f.read()
        
        prompt = prompt.replace("<PROFILE_PLACEHOLDER>", user_profile)
        prompt = prompt.replace("<WOMEN_PLACEHOLDER>", item_description)
        logger.debug(f"prompt: {prompt}")
        return prompt