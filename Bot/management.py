from django.apps import apps
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model

class ModelManager:
    def __init__(self, app_label, model_name):
        self.model:Model = apps.get_model(app_label, model_name)

    @sync_to_async
    def create(self, **kwargs):
        instance = self.model.objects.create(**kwargs)
        return instance

    @sync_to_async
    def update(self, pk, **kwargs):
        try:
            instance = self.model.objects.get(pk=pk)
            for key, value in kwargs.items():
                setattr(instance, key, value)
            instance.save()
            return instance
        except ObjectDoesNotExist:
            return None

    @sync_to_async
    def list(self):
        return list(self.model.objects.all())

    @sync_to_async
    def get(self, **kwargs):
        try:
            return self.model.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None
    @sync_to_async
    def filter(self, **kwargs):
        try:
            return self.model.objects.filter(**kwargs)
        except ObjectDoesNotExist:
            return None

    @sync_to_async
    def delete(self, pk):
        try:
            instance = self.model.objects.get(pk=pk)
            instance.delete()
            return True
        except ObjectDoesNotExist:
            return False



from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def create_instance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    model_name = context.args[0]  # Example: 'telegram_bot.TelegramUser'
    data = dict(arg.split('=') for arg in context.args[1:])

    manager = ModelManager(model_name)
    instance = await manager.create(**data)

    await update.message.reply_text(
        f"Created: {instance}",
        parse_mode=ParseMode.HTML
    )

async def update_instance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    model_name = context.args[0]
    pk = context.args[1]
    data = dict(arg.split('=') for arg in context.args[2:])

    manager = ModelManager(model_name)
    instance = await manager.update(pk, **data)

    if instance:
        await update.message.reply_text(
            f"Updated: {instance}",
            parse_mode=ParseMode.HTML
        )
    else:
        await update.message.reply_text("Instance not found.", parse_mode=ParseMode.HTML)

async def list_instances(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    model_name = context.args[0]

    manager = ModelManager(model_name)
    instances = await manager.list()

    response = "\n".join([str(instance) for instance in instances])
    await update.message.reply_text(
        f"List:\n{response}",
        parse_mode=ParseMode.HTML
    )

async def detail_instance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    model_name = context.args[0]
    pk = context.args[1]

    manager = ModelManager(model_name)
    instance = await manager.detail(pk)

    if instance:
        await update.message.reply_text(
            f"Detail:\n{instance}",
            parse_mode=ParseMode.HTML
        )
    else:
        await update.message.reply_text("Instance not found.", parse_mode=ParseMode.HTML)

async def delete_instance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    model_name = context.args[0]
    pk = context.args[1]

    manager = ModelManager(model_name)
    success = await manager.delete(pk)

    if success:
        await update.message.reply_text("Deleted successfully.", parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_text("Instance not found.", parse_mode=ParseMode.HTML)

