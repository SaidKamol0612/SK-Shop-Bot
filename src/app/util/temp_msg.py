import logging

from aiogram import Bot

from app.core.config import settings

user_msgs = {int: [int]}

BOT = Bot(settings.bot.token)


def add_temp_msg(user_id: int, msg_id: int) -> None:
    """Add a temporary message ID for a user."""
    if not user_msgs.get(user_id):
        user_msgs[user_id] = []
    user_msgs[user_id].append(msg_id)


async def clear_temp_msgs(user_id: int) -> None:
    """Clear all temporary messages for a user."""
    if user_id in user_msgs:
        for msg_id in user_msgs[user_id]:
            try:
                await BOT.delete_message(chat_id=user_id, message_id=msg_id)
            except Exception as e:
                logging.exception(
                    f"Error deleting message {msg_id} for user {user_id}: {e}"
                )
        user_msgs[user_id] = []
    else:
        logging.warning(f"No temporary messages found for user {user_id}.")
