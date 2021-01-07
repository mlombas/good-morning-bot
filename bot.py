from repeated_task import RepeatedTask
from dateutil import parser
import telegram
from telegram.ext import Updater, CommandHandler
import secret

tasks = []

def start(updater, context):
    context.bot.send_message(chat_id=updater.effective_chat.id, text="Bot ready to wish a really good morning to everyone! \u263A")
    context.bot.send_message(chat_id=updater.effective_chat.id, text="You can use the /help command to learn how to configure me!")

def help(updater, context):
    help_text = ""
    try:
        with open("help.txt", "r") as f:
            help_text = f.read()
    except:
        context.bot.send_message(chat_id=updater.effective_chat.id, text="Whoops! There seems to be a problem! contact @Mocoma for help")

    if help_text:
        context.bot.send_message(chat_id=updater.effective_chat.id, text=help_text)

def get_task(task_id):
    id_tasks = [task for task in tasks if task[0] == task_id]
    if id_tasks:
        return id_tasks[0][1]
    else:
        task = RepeatedTask()
        tasks.append((task_id, task))
        return task

def update_task_time(updater, context):
    task = get_task(updater.effective_chat.id)

    time = None
    try:
        time = parser.parse(" ".join(context.args))
    except ParserException:
        context.bot.send_message(chat_id=updater.effective_chat.id, text="It seems the format you introduced is not valid! try again or use /help if you need more info")

    if time:
        task.time_of_repetition = time
        task.restart()

        context.bot.send_message(chat_id=updater.effective_chat.id, text="Done! You will be good morning-ed!")

def update_task_text(updater, context):
    task = get_task(updater.effective_chat.id)

    text = " ".join(context.args)
    if text:
        task.task = lambda: context.bot.send_message(chat_id=updater.effective_chat.id, text=text)
        if not task.is_alive():
            task.restart()

        context.bot.send_message(chat_id=updater.effective_chat.id, text="Done! Your message has been set!")

updater = Updater(token=secret.token, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help))
dispatcher.add_handler(CommandHandler("set_time", update_task_time))
dispatcher.add_handler(CommandHandler("set_message", update_task_text))

updater.start_polling()
