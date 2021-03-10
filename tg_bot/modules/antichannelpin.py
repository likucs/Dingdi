from tg_bot import filters
from tg_bot.types import Message
from tg_bot import (
    COMMAND_HAND_LER,
    A_PIN_MESSAGE_ID
)
from tg_bot.pyrobot import PyroBot


@PyroBot.on_message(
    filters.service
)
async def on_new_pin_message(client: PyroBot, message: Message):
    if message.pinned_message and message.pinned_message.message_id != A_PIN_MESSAGE_ID:
        original_pinned_message = await client.get_messages(
            chat_id=message.chat.id,
            message_ids=A_PIN_MESSAGE_ID
        )
        await original_pinned_message.pin(
            disable_notification=True
        )
