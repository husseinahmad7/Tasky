
from django.http import JsonResponse
from Bot.bot import application
from telegram import Update

import json

async def telegram_webhook(request):
    if request.method == "POST":
        # data = await 
        update = Update.de_json(json.loads(request.body.decode('utf-8')), application.bot)
    
        await application.process_update(update)
        # application.update_queue.put_nowait(update)
        return JsonResponse({"status": "ok"})
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)