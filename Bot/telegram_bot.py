from telegram.ext import CommandHandler, ContextTypes
from ProjectMng.models import Project, Issue, Task, Note, Resource, DailyReport
from django.utils import timezone
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from asgiref.sync import sync_to_async
from Bot.management import ModelManager
ProjectM = ModelManager('ProjectMng', 'Project')
IssueMng = ModelManager('ProjectMng', 'Issue')


async def start(update: Update, context:ContextTypes.DEFAULT_TYPE):
# Parse the project name from the command
    if not context.args:
        await update.message.reply_text("Please specify a project name: /start {project_name}")
        return
    
    project_name = context.args[0]

    # Fetch the project
    try:
        project = await ProjectM.get(name=project_name)
    except Project.DoesNotExist:
        await update.message.reply_text("Project not found.")
        return

    # Fetch the latest issues
    issues = await sync_to_async(list)(project.issues.order_by('-created_at')[:5])

    # Create buttons for issues
    keyboard = [
        [InlineKeyboardButton(f"Issue: {issue.title} ({await sync_to_async(issue.tasks.count)()} tasks)", callback_data=f"issue_{issue.id}")]
        for issue in issues
    ]

    # Build the reply markup
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the response
    await update.message.reply_text(
        f"<b>Project:</b> {project.name}\n\n<b>Latest Issues:</b>",
        reply_markup=reply_markup,
        parse_mode="HTML"
    )


async def help_command(update, context):
    help_text = """
    Available commands:
    /start - Start the bot
    /help - Show this help message
    /projects - List all projects
    /issues <project_id> - List issues for a project
    /tasks <issue_id> - List tasks for an issue
    /add_task <issue_id> <title> <description> - Add a new task
    /daily_report <content> - Submit a daily report
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)


# @sync_to_async
# def list_projects(update, context):
#     projects = Project.objects.all()
#     if projects:
#         project_list = "Projects:\n"
#         for project in projects:
#             project_list += f"{project.id}. {project.name}\n"
#         context.bot.send_message(chat_id=update.effective_chat.id, text=project_list)
#     else:
#         context.bot.send_message(chat_id=update.effective_chat.id, text="No projects found.")

# async def list_issues(update, context):
#     if len(context.args) != 1:
#         context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a project ID.")
#         return
    
#     try:
#         project_id = int(context.args[0])
#         project = Project.objects.get(id=project_id)
#         issues = Issue.objects.filter(project=project)
        
#         if issues:
#             issue_list = f"Issues for {project.name}:\n"
#             for issue in issues:
#                 issue_list += f"{issue.id}. {issue.title} ({issue.get_issue_type_display()})\n"
#             context.bot.send_message(chat_id=update.effective_chat.id, text=issue_list)
#         else:
#             context.bot.send_message(chat_id=update.effective_chat.id, text=f"No issues found for {project.name}.")
#     except Project.DoesNotExist:
#         context.bot.send_message(chat_id=update.effective_chat.id, text="Project not found.")
#     except ValueError:
#         context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid project ID.")

# async def list_tasks(update, context):
#     if len(context.args) != 1:
#         context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide an issue ID.")
#         return
    
#     try:
#         issue_id = int(context.args[0])
#         issue = Issue.objects.get(id=issue_id)
#         tasks = Task.objects.filter(issue=issue)
        
#         if tasks:
#             task_list = f"Tasks for {issue.title}:\n"
#             for task in tasks:
#                 task_list += f"{task.id}. {task.title} - {task.get_status_display()}\n"
#             context.bot.send_message(chat_id=update.effective_chat.id, text=task_list)
#         else:
#             context.bot.send_message(chat_id=update.effective_chat.id, text=f"No tasks found for {issue.title}.")
#     except Issue.DoesNotExist:
#         context.bot.send_message(chat_id=update.effective_chat.id, text="Issue not found.")
#     except ValueError:
#         context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid issue ID.")

# async def add_task(update, context):
#     if len(context.args) < 3:
#         context.bot.send_message(chat_id=update.effective_chat.id, 
#                                  text="Please provide issue ID, task title, and description.")
#         return
    
#     try:
#         issue_id = int(context.args[0])
#         title = context.args[1]
#         description = " ".join(context.args[2:])
        
#         issue = Issue.objects.get(id=issue_id)
#         user = User.objects.get(username=update.effective_user.username)
        
#         task = Task.objects.create(
#             issue=issue,
#             assigned_to=user,
#             title=title,
#             description=description,
#             deadline=None  # You may want to add a way to set the deadline
#         )
        
#         context.bot.send_message(chat_id=update.effective_chat.id, 
#                                  text=f"Task '{title}' added successfully to issue '{issue.title}'.")
#     except Issue.DoesNotExist:
#         context.bot.send_message(chat_id=update.effective_chat.id, text="Issue not found.")
#     except User.DoesNotExist:
#         context.bot.send_message(chat_id=update.effective_chat.id, text="User not found. Please register first.")
#     except ValueError:
#         context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid issue ID.")

# async def daily_report(update, context):
#     if not context.args:
#         context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide the daily report content.")
#         return
    
#     content = " ".join(context.args)
#     user = User.objects.get(username=update.effective_user.username)
    
#     DailyReport.objects.create(
#         user=user,
#         content=content,
#         date=timezone.now().date()
#     )
    
#     context.bot.send_message(chat_id=update.effective_chat.id, text="Daily report submitted successfully.")


