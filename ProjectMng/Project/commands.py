from asgiref.sync import sync_to_async
from ProjectMng.models import Project
from telegram.ext import ContextTypes


@sync_to_async
def list_projects_message():
    projects = Project.objects.all()
    if projects:
        project_list = "Projects:\n"
        for project in projects:
            project_list += f"{project.id}. {project.name}\n"
        return project_list
    else:
        return "No projects found."

async def list_projects(update, context: ContextTypes.DEFAULT_TYPE):
    message = await list_projects_message()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


    