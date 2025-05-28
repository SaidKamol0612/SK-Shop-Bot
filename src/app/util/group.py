from aiogram import Bot

from app.core.config import settings
from app.core.load import get_bot

BOT = get_bot()


async def send_order_to_group(user_name: str, user_phone: str, products: list[dict]):
    group_id = int(settings.group.chat_id)

    msg = (
        "📦 <b>Buyurtma.</b>\n"
        f"  🪪 <b>Buyurtmachi ismi / Имя заказчика:</b> {user_name}\n"
        f"  ☎️ <b>Buyurtmachi telefon raqami / Номер телефона заказчика:</b> {user_phone}\n\n"
        "🛒 <b>Buyurtma qiling mahsulotlar:</b>\n"
    )

    total = 0
    for product in products:
        msg += f"   <b>Mahsulot ID:</b> {product['id']}\n"
        msg += f"   <b>Mahsulot nomi:</b> {product['name']}\n"
        msg += f"   <b>Mahsulot narxi:</b> {product['price']}\n"
        msg += f"   <b>Mahsulot SKU:</b> {product['sku']}\n"
        msg += f"   <b>Mahsulotlar soni:</b> {product['count']}\n"
        t = int(product["count"]) * int(product["price"])
        msg += f"   <b>Jami narxi:</b> {t}\n\n"

        total += t
    msg += f"<b>Ummumiy narx / Общая сумма:</b> {total}"

    await BOT.send_message(chat_id=group_id, text=msg)
