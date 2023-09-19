from telethon import types

from src.common.connections import bot
from src.common.enums import Command


class Navigation:
    menu = {
        Command.START.name: [
            [Command.CHAT.value, Command.CHANNEL.value],
        ],
        Command.CHAT.name: [
            [Command.CHAT_ALL.value],
            [Command.BACK.value]
        ],
        Command.CHAT_ALL.name: [
            [Command.BACK.value]
        ],
        Command.CHANNEL.name: [
            [Command.CHANNEL_COMMENTS.value],
            [Command.BACK.value]
        ],
        Command.CHANNEL_COMMENTS.name: [
            [Command.BACK.value]
        ],
        Command.INPUT_NUMBER.name: [
            [Command.BACK.value, Command.TO_START.value]
        ],
        Command.INPUT_LINK.name: [
            [Command.BACK.value, Command.TO_START.value]
        ]
    }

    @staticmethod
    async def show_menu(menu_name: str, message: str, chat_id: int):
        keyboard = []
        for row in Navigation.menu[menu_name]:
            keyboard_row = types.KeyboardButtonRow([])
            for label in row:
                keyboard_row.buttons.append(types.KeyboardButton(label))
            keyboard.append(keyboard_row)

        markup = types.ReplyKeyboardMarkup(keyboard, resize=True)
        await bot.send_message(chat_id, message, buttons=markup)

    @staticmethod
    async def next(menu_name: str, user_id: int, message: str):
        stack = bot.session.get_navigation_stack(user_id)
        stack.append(menu_name)

        await Navigation.show_menu(menu_name, message, user_id)
        bot.session.set_navigation_stack(user_id, stack)

    @staticmethod
    async def navigate_to_main(user_id: int, message: str):
        menu_name = Command.START.name
        stack = [menu_name]

        await Navigation.show_menu(menu_name, message, user_id)
        bot.session.set_navigation_stack(user_id, stack)

    @staticmethod
    async def back(user_id, message):
        stack = bot.session.get_navigation_stack(user_id)
        stack.pop()

        menu_name = stack[-1]
        await Navigation.show_menu(menu_name, message, user_id)
        bot.session.set_navigation_stack(user_id, stack)
