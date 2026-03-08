import telegram
from telegram import ReplyKeyboardRemove

async def welcome(chatid, context):
    welcome_text = "Hi! What data do you want? type in for a search (e.g., 'Batman' or a JAV code like 'Ipzz-198')."
    await context.bot.send_message(chat_id=chatid, text=welcome_text,
                        reply_markup=ReplyKeyboardRemove())

async def read_me(chatid, context):
    readme_text = '''Welcome to Torrent Bot. Here are some clarifications\n\n
            <b>Do i need a vpn to use this bot?</b>\n
            No. You do not require a vpn to use this bot\n\n
            <b>Why some of the toorent files are showing
            page not found?</b>\n
            Some of the ISP might block the links. 
            If you cant download the .torrent file please
            use a vpn.
            '''
    await context.bot.send_message(chat_id=chatid, text=readme_text,
                        parse_mode=telegram.constants.ParseMode.HTML)

async def privacy(chatid, context):
    privacy_text = '''Welcome to Torrent Bot. Our privacy policy\n\n
            We dont care what you search using
            our bot. We don't store your data and 
            Queries.
            '''
    await context.bot.send_message(chat_id=chatid, text=privacy_text,
                        parse_mode=telegram.constants.ParseMode.HTML)

async def terms(chatid, context):
    terms_text = '''Welcome to Torrent Bot. Terms of use\n\n
            We are not responsible for the contents
            you see/download using our bot.
            '''
    await context.bot.send_message(chat_id=chatid, text=terms_text,
                        parse_mode=telegram.constants.ParseMode.HTML)
