from dotenv import load_dotenv
import os

load_dotenv()


class BaseConfig(object):
    TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
    TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_PHONE_NUMBER = os.getenv('TELEGRAM_PHONE_NUMBER')

    MESSAGES_NUMBER_FOR_SCRAPING = 10_000

    MIN_PARTICIPANTS_TO_SCRAP = 10
    MAX_PARTICIPANTS_TO_SCRAP = 5_000

    PICKED_USER_FIELDS = ['id', 'first_name', 'last_name', 'username', 'phone']

    def __init__(self):
        if self.TELEGRAM_API_ID is None or self.TELEGRAM_API_HASH is None or self.TELEGRAM_BOT_TOKEN is None:
            raise RuntimeError('env file is malformed, check .env file and try again')


class ProductionConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    pass


configs = {'development': DevelopmentConfig, 'production': ProductionConfig}
current_config = configs[os.getenv('ENV', 'development')]()
