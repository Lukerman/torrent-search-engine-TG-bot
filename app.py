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
    elif user_message == "/help":
        await help_command(update, context)
    elif user_message == "/movies" or user_message == "popular_movies":
        await now_playing(chatid, context)
    elif user_message == "/apps" or user_message == "popular_apps":
        await popular_apps(chatid, context)
    elif user_message == "/load_more":
        await load_more(chatid, context)
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

async def post_init(application: Application):
    await application.bot.set_my_commands([
        ("start", "Start the bot"),
        ("movies", "Get currently playing movies"),
        ("apps", "Get popular applications"),
        ("help", "Show help and tips"),
    ])

if __name__ == '__main__':
    token = my_bot_token()
    application = Application.builder().token(token).post_init(post_init).build()
    hdl = MessageHandler(filters.TEXT & (~filters.COMMAND), reply)
    # Command handlers
    from telegram.ext import CommandHandler
    application.add_handler(CommandHandler("start", lambda u, c: start(u.effective_chat.id, c)))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("movies", lambda u, c: now_playing(u.effective_chat.id, c)))
    application.add_handler(CommandHandler("apps", lambda u, c: popular_apps(u.effective_chat.id, c)))
    application.add_handler(CommandHandler("jav", lambda u, c: reply(u, c))) # Reuse reply logic for /jav
    
    application.add_handler(hdl)
    application.add_handler(CallbackQueryHandler(handle_torrent_selection, pattern="^hash_"))
    application.add_handler(CallbackQueryHandler(handle_ijav_download, pattern="^ijavdl_"))
    application.run_polling()
