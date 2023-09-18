import enum


class Command(enum.Enum):
    START = '/start'
    CHAT = 'З публічного чату'
    CHANNEL = 'З відкритого каналу'
    CHAT_ALL = 'Усіх'
    # CHAT_RECENT = 'Недавніх учасників'
    CHANNEL_COMMENTS = 'З коментарів'
    INPUT_NUMBER = r'^([0-9]+)$'
    INPUT_LINK = r'^(?:(@[0-9a-z_]+)|(https://t\.me/[@0-9a-zA-Z_\+]+))$'
    BACK = 'Назад'
    TO_START = 'На початок'
