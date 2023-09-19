from contextlib import asynccontextmanager

from telethon import types
from telethon.errors import rpcerrorlist
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.utils import parse_username

from src.common.config import current_config
from src.common.helpers import pick_user_fields


class Agent:
    @classmethod
    @asynccontextmanager
    async def chat_context(cls, client, username_or_link: str):
        username_or_hash, is_join = parse_username(username_or_link)

        chat_entity = None

        try:
            try:
                if is_join:
                    await client(ImportChatInviteRequest(hash=username_or_hash))
                else:
                    await client(JoinChannelRequest(channel=username_or_link))

            except rpcerrorlist.UserAlreadyParticipantError:
                pass

            chat_entity = await client.get_entity(username_or_link)

            yield chat_entity

        finally:
            if chat_entity:
                await client(LeaveChannelRequest(chat_entity))

    @classmethod
    async def collect_group_participants(cls, client, chat, fields: list[str], file, amount: int):
        total_write = 0

        async for participant in client.iter_participants(chat):
            if total_write >= amount:
                break

            file.writerow(pick_user_fields(participant, fields))
            total_write += 1

        return total_write, None

    @classmethod
    async def get_channel_chat(cls, client, channel):
        chat = None
        posts = 200
        async for post in client.iter_messages(channel):
            if not (posts := posts - 1):
                break

            try:
                print(post)
                async for message in client.iter_messages(channel, reply_to=post.id):
                    if message.peer_id is None:
                        continue

                    chat = await client.get_entity(message.peer_id)
                    break

            except rpcerrorlist.MsgIdInvalidError:
                continue

            if chat is not None:
                break

        return chat

    @classmethod
    async def collect_channel_participants(cls, client, channel, fields: list[str], file, amount: int):
        me = await client.get_me()

        chat = await cls.get_channel_chat(client, channel)
        if chat is None:
            raise ValueError()

        viewed_users = {me.id}
        total_write = 0
        messages_viewed = 0

        async for message in client.iter_messages(chat):
            if (messages_viewed >= current_config.MESSAGES_NUMBER_FOR_SCRAPING or
                    total_write >= amount):
                break

            messages_viewed += 1

            if (
                    message.from_id is None or
                    type(message.from_id) != types.PeerUser or
                    message.from_id.user_id in viewed_users
            ):
                continue

            user = await client.get_entity(message.from_id)
            viewed_users.add(user.id)

            file.writerow(pick_user_fields(user, fields))
            total_write += 1

        return total_write, messages_viewed

    @classmethod
    async def collect_chat_or_channel_participants(cls, client, entity, file, amount):
        try:
            result = await cls.collect_group_participants(
                client=client,
                chat=entity,
                fields=current_config.PICKED_USER_FIELDS,
                file=file,
                amount=amount
            )
            return result

        except rpcerrorlist.ChatAdminRequiredError:
            result = await cls.collect_channel_participants(
                client=client,
                channel=entity,
                fields=current_config.PICKED_USER_FIELDS,
                file=file,
                amount=amount
            )
            return result
