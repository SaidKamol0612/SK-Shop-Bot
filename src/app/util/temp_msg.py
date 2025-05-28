import logging


from app.core.config import settings
from app.core.load import get_bot

user_msgs = {int: [int]}

BOT = get_bot()


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
