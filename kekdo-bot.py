import telegram
import logging
from functools import wraps
from uuid import uuid4

from telegram.ext import Updater, CommandHandler, InlineQueryHandler
from telegram import ChatAction, InlineQueryResultArticle, InputTextMessageContent, ParseMode
from telegram.utils.helpers import escape_markdown

from secrets import BOT_TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

LIST_OF_CMDS = {
  "start": 'Register yourself!',
  "help": 'List of all available commands',
  "tip": 'Tip kekdos to users for their shitty puns!',
  "wallet": 'Check you current kekdo balance'
}

BOT_VERSION = "0.1.2"

def send_typing_action(func):
  @wraps(func)
  def command_func(*args, **kwargs):
    update, context = args
    context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
    return func(update, context, **kwargs)
  return command_func

def log_updates(func):
  """
  A decorator used only for debugging purposes to see the value of the `update` dict
  """
  @wraps(func)
  def log_wrap_func(*args, **kwargs):
    update, context = args
    print("Update received for {}: {}\n\n".format(func.__name__, vars(update)))
    return func(update, context, **kwargs)
  return log_wrap_func

@send_typing_action
def start(update, context):
  """ 
  Command: /start

  Desc: Register an unregistered user to the bot
  """
  # TODO Setup registration process for users
  update.message.reply_text("Welcome to KekdoBot!")

@send_typing_action
def help(update, context):
  """
  Command: /help

  Desc: List all the available commands
  """
  final_msg = ""
  for k,v in LIST_OF_CMDS.items():
    final_msg += "/{} - {}\n".format(k, v)
  final_msg += "\n\n KekdoBot v{}".format(BOT_VERSION)
  update.message.reply_text(final_msg)

def inlinequery(update, context):
  """ Inline command implementation for /tip """
  query = update.inline_query.query
  if not query:
    return

  user_name, amount = query.split(' ')

  # TODO cross-reference usernames with CSV store, update their wallet value

  results = [
    InlineQueryResultArticle(
      id=uuid4(),
      title="Tip",
      description="Tip some kekdos! Ex: @SsKappa 0.10",
      input_message_content=InputTextMessageContent(
        "_You gifted {} {} kekdos!_".format(escape_markdown(user_name), escape_markdown(amount)), 
        parse_mode=ParseMode.MARKDOWN
      )
    )
  ]
  context.bot.answer_inline_query(update.inline_query.id, results)

def main():
  """ Start the bot """
  updater = Updater(token=BOT_TOKEN, use_context=True)
  dp = updater.dispatcher

  dp.add_handler(CommandHandler('start', start))
  dp.add_handler(CommandHandler('help', help))
  dp.add_handler(InlineQueryHandler(inlinequery))

  logger.info("Spinning up KekdoBot v{}".format(BOT_VERSION))

  updater.start_polling()

  updater.idle()


if __name__ == "__main__":
  main()
