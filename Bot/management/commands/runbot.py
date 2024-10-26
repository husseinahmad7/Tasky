from django.core.management.base import BaseCommand
# from Bot.telegram_bot import set_webhook
import asyncio
from telegram import Update

class Command(BaseCommand):
    help = "Set the Telegram bot webhook"

    def handle(self, *args, **kwargs):
        from Bot.bot import application
        async def set_webhook():
            # await application.bot.set_webhook('https://82da-212-8-253-138.ngrok-free.app',allowed_updates=Update.ALL_TYPES)
            await application.run_webhook(webhook_url='https://82da-212-8-253-138.ngrok-free.app',allowed_updates=Update.ALL_TYPES)

        asyncio.run(set_webhook())



