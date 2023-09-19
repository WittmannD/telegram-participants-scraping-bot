import enum


class Command(enum.Enum):
    START = '/start'
    CHAT = u'🗯 З публічного чату'
    CHANNEL = u'📢 З відкритого каналу'
    CHAT_ALL = u'🔵 Усіх'
    # CHAT_RECENT = 'Недавніх учасників'
    CHANNEL_COMMENTS = u'💬 З коментарів'
    INPUT_NUMBER = r'^([0-9]+)$'
    INPUT_LINK = r'^(?:(@[0-9a-zA-Z_]+)|(https://t\.me/[@/0-9a-zA-Z_\+]+))$'
    BACK = u'⬅️ Назад'
    TO_START = u'⏮ На початок'
