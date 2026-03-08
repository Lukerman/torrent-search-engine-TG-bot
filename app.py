import telegram
import re
from telegram.ext import Application, MessageHandler, CallbackQueryHandler, filters
from handlers.bot_handlers import *
from handlers.bot_messages import *
from configs.url_shit import my_bot_token

async def reply(update, context):
    chatid = update.message.chat_id
    user_message = update.message.text
    print(f"DEBUG: Incoming message: '{user_message}' from {chatid}")
    
    if user_message == "/start":
        await start(chatid, context)
    elif user_message == "Top movies":
        await top_movies(chatid, context)
    elif user_message == "Top apps":
        await popular_apps(chatid, context)
    elif user_message == "now playing movies":
        await now_playing(chatid, context)
    elif user_message == "/load_more":
        await load_more(chatid, context)
    elif user_message == "Read me":
        await read_me(chatid, context)
    elif user_message == "Privacy Policy":
        await privacy(chatid, context)
    elif user_message == "Terms":
        await terms(chatid, context)
    elif user_message == "JAV Search":
        await context.bot.send_message(chat_id=chatid, text="Please send the movie code or search term (e.g., Ipzz) for JAV search.")
    elif re.match(r'^/jav($|\s+)', user_message, re.IGNORECASE):
        query = re.sub(r'^/jav\s*', '', user_message, flags=re.IGNORECASE).strip()
        if not query:
            await context.bot.send_message(chat_id=chatid, text="Please provide a search term, e.g., `/jav Ipzz`")
            return
        await jav_search(query, chatid, context)
    elif user_message.startswith("magnet:?xt=urn:btih:"):
        await process_magnet_to_torrent(chatid, context, user_message)
    else:
        await search_engine(user_message, chatid, context)

if __name__ == '__main__':
    token = my_bot_token()
    application = Application.builder().token(token).build()
    hdl = MessageHandler(filters.TEXT, reply)
    application.add_handler(hdl)
    application.add_handler(CallbackQueryHandler(handle_torrent_selection, pattern="^hash_"))
    application.add_handler(CallbackQueryHandler(handle_ijav_download, pattern="^ijavdl_"))
    application.run_polling()
