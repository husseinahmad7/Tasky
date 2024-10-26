from django.conf import settings
from Bot.telegram_bot import *
from ProjectMng.Project.commands import *
from ProjectMng.Issue.callback import *
from telegram import Bot

bot = Bot(settings.TELEGRAM_BOT_TOKEN)

from telegram.ext import Updater, CommandHandler, ApplicationBuilder, CallbackQueryHandler

application = ApplicationBuilder().bot(bot).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CallbackQueryHandler(issue_detail, pattern=r'^issue_\d+$'))




application.add_handler(CommandHandler("projects", list_projects))
# application.add_handler(CommandHandler("issues", list_issues))
# application.add_handler(CommandHandler("tasks", list_tasks))
# application.add_handler(CommandHandler("add_task", add_task))
# application.add_handler(CommandHandler("daily_report", daily_report))

def add_handler(type, func, command:str=None):
    if type=='command':
        application.add_handler(CommandHandler(command, func)) #globals()

