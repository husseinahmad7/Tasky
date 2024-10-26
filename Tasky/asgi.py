"""
ASGI config for Tasky project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tasky.settings')

django_application = get_asgi_application()


from Bot.bot import application
from telegram import Update

from contextlib import asynccontextmanager
# import json
# from django.http import JsonResponse
from starlette.responses import PlainTextResponse, Response

async def telegram_webhook(request):
    if request.method == "POST":
        # data = await 
        # update = Update.de_json(json.loads(request.body.decode('utf-8')), application.bot)
        update = Update.de_json(data=await request.json(), bot=application.bot)

    
        await application.process_update(update)
        # application.update_queue.put_nowait(update)
        return Response()
    else:
        return Response(status=400)

# Starlette serving
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles


@asynccontextmanager
async def ptb_lifespan(app):
    # async with application:
        # await application.run_webhook(webhook_url='https://1647-185-107-56-124.ngrok-free.app/telegram',allowed_updates=Update.ALL_TYPES)
        await application.bot.set_webhook('https://681e-89-38-99-82.ngrok-free.app/telegram/',allowed_updates=Update.ALL_TYPES)
        async with application:
            await application.start()
            yield
            await application.stop()


# async def custom_app(scope, receive, send):
#     if scope["type"] == "lifespan":
#         async with ptb_lifespan(app):
#             yield
#     elif scope["path"].startswith("/static/"):
#         await StaticFiles(directory="static")(scope, receive, send)
#     elif scope["path"].startswith("/telegram"):
#         await Route("/telegram", telegram_webhook, methods=["POST"])(scope, receive, send)
#     else:
#         await django_application(scope, receive, send)

# app = Starlette(
#     debug=True,
#     routes=[
#         Mount("/", custom_app),
#     ],
# )
app = Starlette(
    routes=[
        Route("/telegram/", telegram_webhook, methods=['POST']),
        Mount("/static/", StaticFiles(directory="static"), name="static"),
        Mount("/django/", django_application),  # redirect all requests to Django
    ],
    lifespan=ptb_lifespan,
)
