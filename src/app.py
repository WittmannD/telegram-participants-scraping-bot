import os.path

from telethon import events, utils, types
from telethon.errors import rpcerrorlist
from telethon.tl.functions.channels import GetParticipantsRequest

from src.common.config import current_config
from src.common.connections import agent_client, bot, client
from src.common.enums import Command
from src.common.helpers import step_filter, tmp_csv_context
from src.services.agent import Agent
from src.services.navigation import Navigation


@events.register(events.NewMessage(pattern=lambda m: m == Command.START.value or m == Command.TO_START.value))
async def start_handler(event: events.NewMessage.Event):
    message = (u'Оберіть тип чату з якого буде здійснений скрапінг учасників. '
               u'Чат має бути загальнодоступним.')
    await Navigation.navigate_to_main(event.message.peer_id.user_id, message)


@events.register(events.NewMessage(pattern=Command.BACK.value))
async def back_handler(event: events.NewMessage.Event):
    user_id = event.message.peer_id.user_id
    await Navigation.back(user_id, Command.BACK.value)


@events.register(events.NewMessage(pattern=Command.CHAT.value))
async def chat_option_handler(event: events.NewMessage.Event):
    user_id = event.message.peer_id.user_id
    message = u'Оберіть критерії збору учасників'
    await Navigation.next(Command.CHAT.name, user_id, message)


@events.register(events.NewMessage(pattern=Command.CHAT_ALL.value))
async def chat_all_option_handler(event: events.NewMessage.Event):
    user_id = event.message.peer_id.user_id
    message = f'Збір можливий лише за умови, що учасники чату не приховані'
    await Navigation.next(Command.CHAT_ALL.name, user_id, message)
    await event.client.send_message(event.message.peer_id, f'Введіть кількість учасників, яку потрібно зібрати')


@events.register(events.NewMessage(pattern=Command.CHANNEL.value))
async def channel_option_handler(event: events.NewMessage.Event):
    user_id = event.message.peer_id.user_id
    message = u'Оберіть критерії збору учасників'
    await Navigation.next(Command.CHANNEL.name, user_id, message)


@events.register(events.NewMessage(pattern=Command.CHANNEL_COMMENTS.value))
async def channel_comments_option_handler(event: events.NewMessage.Event):
    user_id = event.message.peer_id.user_id
    message = f'Збір буде здійснений за першими {current_config.MESSAGES_NUMBER_FOR_SCRAPING} коментарями, за умови що в каналі увімкнені коменатрі'
    await Navigation.next(Command.CHANNEL_COMMENTS.name, user_id, message)
    await event.client.send_message(event.message.peer_id, f'Введіть кількість учасників, яку потрібно зібрати')


@events.register(events.NewMessage(pattern=Command.INPUT_NUMBER.value,
                                   func=step_filter([Command.CHAT_ALL.name, Command.CHANNEL_COMMENTS.name])))
async def number_listener_handler(event: events.NewMessage.Event):
    user_id = event.message.peer_id.user_id
    minimum = current_config.MIN_PARTICIPANTS_TO_SCRAP
    maximum = current_config.MAX_PARTICIPANTS_TO_SCRAP
    number = int(event.pattern_match.group(0))

    if number < minimum or number > maximum:
        await event.reply(f'Мінімальна кількість - {minimum}; максимальна - {maximum} включно')
    else:
        event.client.session.update_settings(user_id, {'number': number})
        message = (u'Надішли посилання на чат. У вигляді гіперпосилання '
                   u'(https://t.me/members_scraping_bot) або тега (@members_scraping_bot)')
        await Navigation.next(Command.INPUT_NUMBER.name, user_id, message)


@events.register(events.NewMessage(pattern=Command.INPUT_LINK.value, func=step_filter([Command.INPUT_NUMBER.name])))
async def chat_link_listener_handler(event: events.NewMessage.Event):
    link = event.pattern_match.group(0)
    user_id = event.message.peer_id.user_id
    number, _ = event.client.session.get_settings(user_id)

    async with agent_client:
        async with Agent.chat_context(agent_client, link) as chat:
            try:
                await event.reply('Починаю збір учасників. Це може зайняти деякий час...')

                if not chat.megagroup:
                    await event.client.send_message(event.message.peer_id,
                                                    'За цим посиланням виявлено канал. Збір учасників буде здійснено в чаті каналу '
                                                    f'за повідомленнями. Максимум {current_config.MESSAGES_NUMBER_FOR_SCRAPING} повідомлень')

                async with tmp_csv_context(prefix=str(chat.id), header=current_config.PICKED_USER_FIELDS) as (
                        file, writer):
                    total, viewed = await Agent.collect_chat_or_channel_participants(client=agent_client, entity=chat,
                        file=writer, amount=number)

                    message = (
                        f'Знайдено {total} учасників' if viewed is None else f'Знайдено {total} учасників. Переглянуто {viewed} повідомлень')

                    file.flush()

                    await bot.send_file(event.message.peer_id, caption=message, file=file.name)

            except ValueError as err:
                await event.reply('Жоден чат за цим посиланням не знайдено')
                print(err)

            except rpcerrorlist.ChannelPrivateError:
                await event.reply('Цей канал має приватний доступ')


handlers = [start_handler, chat_option_handler, chat_all_option_handler, number_listener_handler,
            chat_link_listener_handler, channel_option_handler, channel_comments_option_handler, back_handler]


def register_commands():
    for handler in handlers:
        bot.add_event_handler(handler)


def init_app():
    register_commands()
