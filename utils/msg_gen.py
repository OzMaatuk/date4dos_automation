import re
import logging
from typing import Optional, Union
from langchain.chat_models.base import init_chat_model, BaseChatModel
from constants.settings import Settings
logger = logging.getLogger(__name__)

class MessageGenerator:
    def __init__(
        self,
        method: Optional[str] = "default",
        llm_config: dict = {},
        prompt_file_path: str = Settings().PROMPT_FILE,
        profile_file_path: str = Settings().PROFILE_FILE
    ):
        logger.debug("MessageGenerator instance created")
        self.method = method
        self.prompt_file_path = prompt_file_path
        self.profile_file_path = profile_file_path

        if self.method == "llm":
            if llm_config == {}:
                llm_config = {
                    "model": Settings().DEFAULT_MODEL_NAME,
                    "model_provider": Settings().DEFAULT_MODEL_PROVIDER,
                    "base_url": Settings().DEFAULT_MODEL_URL
                }
            self.llm: Union[BaseChatModel, None] = None
            self.llm = init_chat_model(**llm_config)
            logger.info("LLM model initialized successfully")
        elif self.method == "default":
            logger.info("Using default message method")
        else:
            raise ValueError(f"Unsupported method: {self.method}")


    def generate(self, item_description: str) -> str:
        logger.debug("MessageGenerator.generate")
        prompt = self.generate_prompt(item_description)
        if self.method == "llm" and self.llm: response = self.llm.invoke(prompt)
        elif self.method == "default": return Settings().DEFAULT_MESSAGE
        else: raise RuntimeError("message genrator method is not initilized")
        result = str(response.content) if hasattr(response, "content") else str(response)
        logger.debug(f"Result: {result}")
        return result

    def generate_prompt(self, item_description: str) -> str:
        logger.debug("MessageGenerator.generate_prompt")
        prompt = MessageGenerator.load_file_clearly(self.prompt_file_path)
        user_profile = MessageGenerator.load_file_clearly(self.profile_file_path)
        prompt = prompt.replace("<PROFILE_PLACEHOLDER>", user_profile)
        prompt = prompt.replace("<WOMEN_PLACEHOLDER>", item_description)
        logger.debug(f"prompt: {prompt}")
        return prompt

    @staticmethod
    def load_file_clearly(filepath: str, max_length: Optional[int] = None) -> str:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            text = re.sub(r'\s+', ' ', text).strip()
            text = ''.join(char for char in text if ord(char) >= 32)
            if max_length is not None:
                text = text[:max_length]
            return text
        except FileNotFoundError:
            logger.error(f"Error: File not found at {filepath}")
            return ""
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return ""