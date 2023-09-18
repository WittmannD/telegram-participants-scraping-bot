import csv
from contextlib import contextmanager, asynccontextmanager
from tempfile import NamedTemporaryFile

from telethon.errors import rpcerrorlist
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.utils import parse_username
from telethon import events, types

from src.common.config import current_config


def step_filter(steps: list[str]):
    def func(event: events.NewMessage.Event):
        user_id = event.message.peer_id.user_id
        stack = event.client.session.get_navigation_stack(user_id)
        current_step = stack[-1]

        return current_step in steps

    return func


def pick_user_fields(user, fields: list[str]):
    user_dict = user.to_dict()
    pick = []

    for field in fields:
        pick.append(user_dict[field])

    return pick


@asynccontextmanager
async def tmp_csv_context(prefix, header=None):
    temp_file = None

    try:
        temp_file = NamedTemporaryFile(mode='r+', prefix=prefix, suffix='.csv', encoding='utf-8')
        writer = csv.writer(temp_file, quoting=csv.QUOTE_NONNUMERIC)

        if header:
            writer.writerow(header)

        yield temp_file, writer

    finally:
        if temp_file:
            temp_file.close()


@contextmanager
def csv_context(filename):
    file = None
    try:
        file = open(filename, 'w', encoding='utf-8')
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)

        yield writer

    finally:
        if file:
            file.close()

