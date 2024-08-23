import asyncio
from telegram import Bot
from django.conf import settings
#wysylania powiadomien asyncio wymagane
def send_telegram_message(chat_id, message):
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    asyncio.run(bot.send_message(chat_id=chat_id, text=message))