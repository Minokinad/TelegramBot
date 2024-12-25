from telegram import Update,InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, MessageHandler,ApplicationBuilder, ContextTypes, CommandHandler, InlineQueryHandler

from uuid import uuid4

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello there")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Caps",
            input_message_content=InputTextMessageContent(query.upper()),
        )
    )
    print(results)
    await context.bot.answer_inline_query(update.inline_query.id, results)

async def wordcount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    count = len(context.args)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=count)

if __name__ == '__main__':
    with open("bot_token", mode='r') as file:
        BOT_TOKEN = file.read()
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters=(filters.TEXT & (~filters.COMMAND)), callback=echo)
    caps_handler = CommandHandler('caps', caps)
    inline_caps_handler = InlineQueryHandler(inline_caps)
    word_count_handler = CommandHandler('wordcount', wordcount)

    application.add_handler(echo_handler)
    application.add_handler(start_handler)
    application.add_handler(caps_handler)
    application.add_handler(inline_caps_handler)
    application.add_handler(word_count_handler)

    application.run_polling()