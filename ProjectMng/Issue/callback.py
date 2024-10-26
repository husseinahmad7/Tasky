from asgiref.sync import sync_to_async
from ProjectMng.models import Issue
from telegram.ext import ContextTypes
from telegram import Update

async def issue_detail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Parse the issue ID from the callback data
    issue_id = int(query.data.split('_')[1])

    # Fetch the issue
    try:
        issue = await sync_to_async(Issue.objects.get)(id=issue_id)
    except Issue.DoesNotExist:
        await query.message.reply_text("Issue not found.")
        return

    # Fetch the tasks
    tasks = await sync_to_async(list)(issue.tasks.all())

    # Create the task list
    task_list = "\n".join([f"- {task.title} {'✅' if task.status == 'DONE' else '❌'}" for task in tasks])

    # Send the task details
    await query.message.reply_text(
        f"<b>Issue:</b> {issue.title}\n\n<b>Tasks:</b>\n{task_list}",
        parse_mode="HTML"
    )