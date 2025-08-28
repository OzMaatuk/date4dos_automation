import configparser
import os
from dotenv import load_dotenv


class Settings:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        load_dotenv()

    @property
    def BASE_URL(self):
        return self.config.get('Settings', 'base_url')

    @property
    def BROWSER_TYPE(self):
        return self.config.get('Settings', 'browser_type')

    @property
    def BROWSER_DATA(self):
        return self.config.get('Settings', 'browser_data_dir')

    @property
    def HEADLESS(self):
        return self.config.getboolean('Settings', 'headless', fallback=True)

    @property
    def TIMEOUT(self):
        return self.config.getint('Settings', 'timeout', fallback=1000)

    @property
    def LIMIT(self):
        return self.config.getint('Settings', 'limit', fallback=3)

    @property
    def LOG_LEVEL(self):
        return self.config.get('Settings', 'log_level', fallback='INFO')
    
    @property
    def LOG_FILE(self):
        return self.config.get('Settings', 'log_file', fallback='logs/main.log')

    @property
    def LOG_FORMAT(self):
        return self.config.get('Settings', 'log_format', fallback="%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    @property
    def OUTPUT_DIR(self):
        return self.config.get('Settings', 'output_dir', fallback='results/')
    
    @property
    def PROFILE_FILE(self):
        return self.config.get('Settings', 'profile_file')
    
    @property
    def PROMPT_FILE(self):
        return self.config.get('Settings', 'prompt_file')    

    @property
    def USERNAME(self):
        return os.getenv('USERNAME') or self.config.get('Settings', 'username')

    @property
    def PASSWORD(self):
        return os.getenv('PASSWORD') or self.config.get('Settings', 'password')

    @property
    def API_KEY(self):
        return os.getenv('GOOGLE_API_KEY') or self.config.get('Settings', 'api_key')