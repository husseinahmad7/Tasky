from django.urls import re_path, include
from django.conf import settings

# from .views import start, BotMenuElemViewSet, UserViewSet, some_debug_func
from Bot.webhook import telegram_webhook
from .telegram_bot import start

urlpatterns = [
    # re_path('start', start, name='start'),
    # re_path('main_menu', start, name='start'),

    # re_path('sb/', BotMenuElemViewSet, name='BotMenuElemViewSet'),
    # re_path('us/', UserViewSet, name='UserViewSet'),
    # re_path('',telegram_webhook)
]
