from random import randint

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

async def cities(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("cities.txt", mode='r', encoding='utf-8') as f:
        cities = f.read()
    cities = cities.split(',')
    for i in range(len(cities)):
        cities[i] = cities[i].replace('"', ' ').strip()
    print(cities)
    my_cities, last_city = list(cities.copy()), ""
    try:
        with open(str(update.effective_user.id) + ".txt", mode='r', encoding='utf-8') as f:
            for city in f:
                city = city.strip()
                if city not in my_cities:
                    continue
                my_cities.remove(city)
                last_city = city
    except FileNotFoundError:
        with open(str(update.effective_user.id) + ".txt", mode='w', encoding='utf-8') as f:
            pass
    user_city = str(''.join(context.args))
    prt = ""
    print(last_city, len(last_city), user_city, type(user_city))
    if user_city in my_cities and (len(last_city) == 0 or last_city[-1].upper() == user_city[0]):
        prt += "Отлично! Теперь моя очередь. "
        trys, k = [], 0
        while len(trys) == 0:
            k -= 1
            trys = [city for city in my_cities if city[0] == user_city[k].upper()]

        my_city, ran = user_city, 0
        while my_city == user_city:
            ran = randint(0, len(trys))
            if ran == len(trys):
                break
            my_city = trys[ran]
        if ran == len(trys):
            prt += "Поздравляю! Ты победил, я не могу придумать город на такую букву."
            with open(str(update.effective_user.id) + ".txt", mode='w', encoding='utf-8') as f:
                pass
        else:
            trys, k = [], 0
            while len(trys) == 0:
                k -= 1
                trys = [city for city in my_cities if city[0] == my_city[-1].upper()]
            prt += f"Я загадал город {my_city}, теперь твоя очередь на букву {my_city[-1].upper()}"
            with open(str(update.effective_user.id) + ".txt", mode='a', encoding='utf-8') as f:
                f.write(user_city + "\n")
                f.write(my_city + "\n")
    else:
        prt = "Вы ввели неправильный город!"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=prt)

if __name__ == '__main__':
    with open("bot_token", mode='r') as file:
        BOT_TOKEN = file.read()
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters=(filters.TEXT & (~filters.COMMAND)), callback=echo)
    caps_handler = CommandHandler('caps', caps)
    inline_caps_handler = InlineQueryHandler(inline_caps)
    word_count_handler = CommandHandler('wordcount', wordcount)
    cities_handler = CommandHandler('cities', cities)

    application.add_handler(echo_handler)
    application.add_handler(start_handler)
    application.add_handler(caps_handler)
    application.add_handler(inline_caps_handler)
    application.add_handler(word_count_handler)
    application.add_handler(cities_handler)

    application.run_polling()