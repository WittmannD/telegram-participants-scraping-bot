import unittest

from telethon import TelegramClient, functions
from telethon.utils import parse_username

from src.common.config import current_config

client = TelegramClient('bot_test', current_config.TELEGRAM_API_ID, current_config.TELEGRAM_API_HASH)
# agent = client.start(phone='+380686990793')


class BotTest(unittest.TestCase):
    def test_bot(self):
        print('start')

        async def test():

            channel_hash, _ = parse_username('https://t.me/+6ICy2JfwaZ4zYjcy')
            print(channel_hash)
            # await client(functions.channels.JoinChannelRequest('https://t.me/misanthropic_raccoon'))
            # result = await client(functions.messages.CheckChatInviteRequest(
            #     hash=channel_hash
            # ))
            #
            # print(result.stringify())
            async with client:
                result=None
                try:
                    result = await client(functions.channels.JoinChannelRequest(
                        channel='https://t.me/+6ICy2JfwaZ4zYjcy'
                    ))
                except Exception:
                    result = await client(functions.messages.ImportChatInviteRequest(
                        hash=channel_hash
                    ))
                print(result)
                entity = await client.get_entity('https://t.me/+6ICy2JfwaZ4zYjcy')
                print(entity.stringify())

            # async for part in agent.iter_participants(entity):
            #     print(part)

        self.assertEqual(1, 1)

        client.loop.run_until_complete(test())


if __name__ == '__main__':
    unittest.main()
