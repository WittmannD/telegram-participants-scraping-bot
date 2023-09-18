from telethon import TelegramClient

from src.common.config import current_config
from src.session.sqlite_custom_session import SQLiteCustomSession

session = SQLiteCustomSession('bot_session')
client = TelegramClient(session, current_config.TELEGRAM_API_ID, current_config.TELEGRAM_API_HASH)
agent_client = TelegramClient('agent_session', current_config.TELEGRAM_API_ID, current_config.TELEGRAM_API_HASH)
bot = client.start(bot_token=current_config.TELEGRAM_BOT_TOKEN)
agent = agent_client.start(phone=current_config.TELEGRAM_PHONE_NUMBER)
