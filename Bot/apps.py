from django.apps import AppConfig

class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Bot'
    # def ready(self):
    #     from .telegram_bot import application, Update
    #     application.run_webhook(webhook_url='https://5a74-185-182-193-32.ngrok-free.app',allowed_updates=Update.ALL_TYPES)
        