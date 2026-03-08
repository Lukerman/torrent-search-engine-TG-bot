from configs.url_shit import pirat_api, movies_api
from configs.blah_blah import welcome
from handlers.letme_handle import listToString
from bs4 import BeautifulSoup
import requests
import telegram
import json
import random
import httpx # Added for async requests
import urllib.parse
import asyncio
import os
import re
import httpx
import html
import html as html_lib
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

def format_size(size_bytes):
    try:
        size_bytes = int(size_bytes)
        if size_bytes == 0: return "0 B"
        suffixes = ["B", "KB", "MB", "GB", "TB", "PB"]
        i = 0
        while size_bytes >= 1024 and i < len(suffixes) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.2f} {suffixes[i]}"
    except Exception:
        return f"{size_bytes} B"

async def start(chatid, context):
    
    await welcome(chatid, context)


async def top_movies(chatid, context):
    URL = f"{pirat_api()}q.php?q=top100:0" # Use global top 100
    update1 = await context.bot.send_message(chat_id=chatid, text="Please wait..Fetching data from APIBay")
    
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True, headers={"User-Agent": USER_AGENT}) as client:
            response = await client.get(URL)
            all_data = response.json()
            
            # Filter for Movie categories: 201 (Movies), 202 (DVDR), 207 (HD), 208 (UltraHD)
            data = [i for i in all_data if i.get('category') in ['201', '202', '207', '208']]

            if not data:
                await context.bot.edit_message_text(chat_id=chatid, message_id=update1.message_id, text="No top movies found currently on APIBay.")
                return

            await context.bot.edit_message_text(chat_id=chatid, message_id=update1.message_id, text="pushing data......")
            
            text_lines = ["🍿 <b>Top 5 Movies:</b>\n"]
            keyboard_row = []
            
            for idx, item in enumerate(data[:5], start=1): # LIMIT TO TOP 5
                title = item.get("name", "Unknown Title")
                info_hash = item.get("info_hash", "")
                size_str = format_size(item.get("size", "0"))
                seeders = item.get("seeders", "N/A")
                
                text_lines.append(f"{idx}. <b>{title}</b>")
                text_lines.append(f"   💾 {size_str} 🟢 Seeders: {seeders}\n")
                
                keyboard_row.append(telegram.InlineKeyboardButton(str(idx), callback_data=f"hash_{idx}_{info_hash}"))
                
            reply_markup = telegram.InlineKeyboardMarkup([keyboard_row])
            final_text = "\n".join(text_lines)
            
            await context.bot.send_message(
                chat_id=chatid, 
                text=final_text, 
                reply_markup=reply_markup,
                parse_mode=telegram.constants.ParseMode.HTML
            )
            
            await context.bot.delete_message(chat_id=chatid, message_id=update1.message_id) 
            
    except Exception as e:
        await context.bot.edit_message_text(chat_id=chatid, message_id=update1.message_id, text=f"Error fetching data: {str(e)[:100]}")


async def popular_apps(chatid, context):
    URL = f"{pirat_api()}q.php?q=top100:0" # Use global top 100
    update1 = await context.bot.send_message(chat_id=chatid, text="Please wait..Fetching data from APIBay")
    
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True, headers={"User-Agent": USER_AGENT}) as client:
            response = await client.get(URL)
            all_data = response.json()
            
            # Filter for Application categories: 301 (Windows), 302 (Mac), 303 (Linux)
            data = [i for i in all_data if i.get('category') in ['301', '302', '303']]

            if not data:
                await context.bot.edit_message_text(chat_id=chatid, message_id=update1.message_id, text="No popular apps found currently on APIBay.")
                return

            text_lines = ["📱 <b>Top 5 Popular Apps:</b>\n"]
            keyboard_row = []
            
            for idx, item in enumerate(data[:5], start=1): # LIMIT TO TOP 5
                title = item.get("name", "Unknown Title")
                info_hash = item.get("info_hash", "")
                size_str = format_size(item.get("size", "0"))
                seeders = item.get("seeders", "N/A")
                
                text_lines.append(f"{idx}. <b>{title}</b>")
                text_lines.append(f"   💾 {size_str} 🟢 Seeders: {seeders}\n")
                
                keyboard_row.append(telegram.InlineKeyboardButton(str(idx), callback_data=f"hash_{idx}_{info_hash}"))
                
            reply_markup = telegram.InlineKeyboardMarkup([keyboard_row])
            final_text = "\n".join(text_lines)
            
            await context.bot.send_message(
                chat_id=chatid, 
                text=final_text, 
                reply_markup=reply_markup,
                parse_mode=telegram.constants.ParseMode.HTML
            )
            
            await context.bot.delete_message(chat_id=chatid, message_id=update1.message_id) 
            
    except Exception as e:
        await context.bot.edit_message_text(chat_id=chatid, message_id=update1.message_id, text=f"Error fetching data: {str(e)[:100]}")


async def now_playing(chatid, context):
    movies_all = {}
    final_data = []
    url = movies_api()
    try:
        async with httpx.AsyncClient(timeout=20.0, follow_redirects=True, headers={"User-Agent": USER_AGENT}) as client:
            response1 = await client.get(url)
            data1 = response1.json()
            movies = data1["results"]
            for movie in movies[:5]: # Send top 5 with posters
                title = movie["title"]
                release = movie.get("release_date", "N/A")
                poster_path = movie.get("poster_path")
                overview = movie.get("overview", "")
                
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
                
                caption = (
                    f"🎬 <b>{html.escape(title)}</b>\n"
                    f"📅 Release: {release}\n\n"
                    f"{html.escape(overview[:150])}..."
                )
                
                # Search button for this movie
                keyboard = [[telegram.InlineKeyboardButton(f"🔍 Search for '{title}'", callback_data=f"search_{title}")]]
                reply_markup = telegram.InlineKeyboardMarkup(keyboard)
                
                if poster_url:
                    await context.bot.send_photo(
                        chat_id=chatid,
                        photo=poster_url,
                        caption=caption,
                        reply_markup=reply_markup,
                        parse_mode=telegram.constants.ParseMode.HTML
                    )
                else:
                    await context.bot.send_message(
                        chat_id=chatid,
                        text=caption,
                        reply_markup=reply_markup,
                        parse_mode=telegram.constants.ParseMode.HTML
                    )
            
            await context.bot.send_message(chat_id=chatid, text="Want more? /load_more")

    except Exception as e:
        import traceback
        print(f"DEBUG Now Playing Error: {traceback.format_exc()}")
        await context.bot.send_message(chat_id=chatid, text=f"Error fetching movies: {str(e)[:100]}")


async def load_more(chatid, context):
    movies_all = {}
    final_data = []
    check = movies_api()
    try:
        async with httpx.AsyncClient(timeout=20.0, follow_redirects=True, headers={"User-Agent": USER_AGENT}) as client:
            response1 = await client.get(check)
            data1 = response1.json()
            page = data1["total_pages"]
            search = random.randint(1, page)
            url = f"https://api.themoviedb.org/3/movie/now_playing?api_key=cc348043650d1146104248ee9c810fa6&language=en-US&page={search}"
            response1 = await client.get(url)
            data1 = response1.json()
            if "results" not in data1:
                await context.bot.send_message(chat_id=chatid, text="Error: TMDB API did not return any results.")
                return

            movies = data1["results"]
            for movie in movies:
                safe_title = html.escape(movie["title"])
                movies_under = safe_title.replace(" ", "_")
                movies_all["title"] = "/"+movies_under
                movies_all["release_date"] = movie.get("release_date", "N/A")
                send_data = json.dumps(movies_all).strip(
                    '{}').replace(',', '\n').replace('"', '')
                final_data.append(send_data+"\n\n")
            final_str = listToString(final_data)
            await context.bot.send_message(chat_id=chatid, text="Click a movie name to get torrent links." +
                                "\n\n"+final_str, parse_mode=telegram.constants.ParseMode.HTML)
            await context.bot.send_message(chat_id=chatid, text='show more movies?\n\n'+"/load_more")
    except Exception as e:
        import traceback
        print(f"DEBUG Load More Error: {traceback.format_exc()}")
        await context.bot.send_message(chat_id=chatid, text=f"Error fetching movies: {str(e)[:100]}")


async def search_engine(user_message, chatid, context):
    user_message = user_message.replace("_", " ").replace("/", "")
    URL = f"{pirat_api()}q.php?q={urllib.parse.quote(user_message)}"
    update1 = await context.bot.send_message(chat_id=chatid, text=f"Please wait..Searching for '{user_message}' on APIBay")

    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True, headers={"User-Agent": USER_AGENT}) as client:
            response = await client.get(URL)
            data = response.json()

            if not data or (len(data) == 1 and data[0].get('id') == '0'):
                # Deleting the APIBay specific status before switching to JAV search
                await context.bot.delete_message(chat_id=chatid, message_id=update1.message_id)
                await jav_search(user_message, chatid, context)
                return

            text_lines = [f"🔍 <b>Search Results for '{user_message}':</b>\n"]
            keyboard_row = []
            
            for idx, item in enumerate(data[:5], start=1): # LIMIT TO TOP 5 search results
                title = item.get("name", "Unknown Title")
                info_hash = item.get("info_hash", "")
                size_str = format_size(item.get("size", "0"))
                seeders = item.get("seeders", "N/A")
                
                text_lines.append(f"{idx}. <b>{title}</b>")
                text_lines.append(f"   💾 {size_str} 🟢 Seeders: {seeders}\n")
                keyboard_row.append(telegram.InlineKeyboardButton(str(idx), callback_data=f"hash_{idx}_{info_hash}"))
                
            reply_markup = telegram.InlineKeyboardMarkup([keyboard_row])
            final_text = "\n".join(text_lines)
            
            await context.bot.send_message(
                chat_id=chatid,
                text=final_text,
                reply_markup=reply_markup,
                parse_mode=telegram.constants.ParseMode.HTML
            )
            
            await context.bot.delete_message(chat_id=chatid, message_id=update1.message_id) 

    except Exception as e:
        await context.bot.edit_message_text(chat_id=chatid, message_id=update1.message_id, text=f"Error fetching data: {str(e)[:100]}")

async def process_magnet_to_torrent(chatid, context, magnet_link):
    status_msg = await context.bot.send_message(chat_id=chatid, text="Fetching torrent metadata via API Proxy, please wait...")
    
    try:
        # Extract the info_hash using regex
        match = re.search(r'xt=urn:btih:([a-zA-Z0-9]+)', magnet_link, re.IGNORECASE)
        if not match:
            await context.bot.edit_message_text(
                chat_id=chatid, 
                message_id=status_msg.message_id, 
                text="Invalid Magnet Link provided."
            )
            return
            
        info_hash = match.group(1).upper()
        
        # Extract filename (dn parameter)
        title = "download"
        parsed_url = urllib.parse.urlparse(magnet_link)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        if 'dn' in query_params:
            title = urllib.parse.unquote(query_params['dn'][0])
            
        safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c in (' ', '_', '-')]).rstrip()
        if not safe_title: safe_title = "download"
        file_path = f"./{safe_title}.torrent"
        
        # Fetch the .torrent file from itorrents using Codetabs proxy to bypass ISP blocks
        target_url = f"https://itorrents.org/torrent/{info_hash}.torrent"
        proxy_url = f"https://api.codetabs.com/v1/proxy?quest={target_url}"
        
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True, headers={"User-Agent": USER_AGENT}) as client:
            response = await client.get(proxy_url)
            
            # Verify the response is an actual valid Bencoded torrent file, not an HTML error or Cloudflare captcha
            if response.status_code != 200 or not response.content or not response.content.startswith(b'd8:'):
                await context.bot.edit_message_text(
                    chat_id=chatid, 
                    message_id=status_msg.message_id, 
                    text="Unable to fetch torrent metadata. The magnet may be inactive or currently un-cached."
                )
                return
                
            # Save bytes to disk
            with open(file_path, 'wb') as f:
                f.write(response.content)
                
        # Send document back to Telegram user
        with open(file_path, 'rb') as f:
            await context.bot.send_document(chat_id=chatid, document=f)
            
        await context.bot.delete_message(chat_id=chatid, message_id=status_msg.message_id)
        
        # Clean up
        if os.path.exists(file_path):
            os.remove(file_path)
            
    except Exception as e:
        await context.bot.edit_message_text(
            chat_id=chatid, 
            message_id=status_msg.message_id, 
            text=f"Error generating torrent link: {str(e)[:100]}"
        )

async def handle_torrent_selection(update, context):
    query = update.callback_query
    await query.answer()
    
    # Handle search triggers from rich previews
    if query.data.startswith("search_"):
        search_query = query.data.replace("search_", "")
        await search_engine(search_query, query.message.chat_id, context)
        return

    # Expected format: hash_{idx}_{info_hash}
    data_parts = query.data.split("_")
    if len(data_parts) < 3:
        return
        
    idx = data_parts[1]
    info_hash = data_parts[2]
    
    title = "download"
    try:
        # Extract title from the message text block
        if query.message and query.message.text:
            text = query.message.text
            part = text.split(f"{idx}. ")[1]
            title = part.split("\n")[0].strip()
    except Exception:
        pass
    
    chatid = query.message.chat_id
    magnet_link = f"magnet:?xt=urn:btih:{info_hash}&dn={urllib.parse.quote(title)}"
    
    # We leverage our existing robust magnet processor 
    await process_magnet_to_torrent(chatid, context, magnet_link)

async def jav_search(query, chatid, context):
    query = query.replace(" ", "+")
    URL = f"https://ijavtorrent.com/?searchTerm={query}"
    status_msg = await context.bot.send_message(chat_id=chatid, text=f"Searching for '{query}' on iJavTorrent...")

    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True, headers={"User-Agent": USER_AGENT}, verify=False) as client:
            response = await client.get(URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            video_items = soup.find_all('div', class_='video-item')
            if not video_items:
                await context.bot.edit_message_text(chat_id=chatid, message_id=status_msg.message_id, text=f"No JAV results found for '{query}'.")
                return

            text_lines = [f"🔞 <b>JAV Search Results for '{query}':</b>\n"]
            keyboard_row = []
            cover_url = None
            
            # Extract cover for the first result to "WOW" the user
            first_vid = video_items[0]
            img_tag = first_vid.find('img')
            if img_tag:
                cover_url = img_tag.get('src')
                if cover_url and not cover_url.startswith('http'):
                    cover_url = "https://ijavtorrent.com" + cover_url

            count = 0

            for vid in video_items:
                if count >= 5: break
                
                # Fallback title from the movie name div
                movie_name_div = vid.find('div', class_='name')
                fallback_title = movie_name_div.get_text(strip=True) if movie_name_div else "Unknown JAV"
                
                # Each video-item has a table of torrents.
                torrent_table = vid.find('table', class_='table-sm')
                if not torrent_table: continue
                
                torrent_row = torrent_table.find('tr')
                if not torrent_row: continue
                
                dl_tag = torrent_row.find('a', class_='download-click-track')
                magnet_tag = torrent_row.find('a', class_='magnet-click-track')
                
                if not dl_tag: continue
                
                dl_href = dl_tag.get('href', '')
                dl_id = dl_href.split('/')[-1] if '/' in dl_href else ""
                if not dl_id: continue
                
                # We still extract info_hash if magnet is available for fallback, 
                # but we prioritize dl_id for direct download.
                info_hash = ""
                if magnet_tag:
                    magnet = magnet_tag.get('href', '').replace('&amp;', '&')
                    hash_match = re.search(r'xt=urn:btih:([a-zA-Z0-9]+)', magnet, re.IGNORECASE)
                    if hash_match:
                        info_hash = hash_match.group(1).upper()

                
                # Extract title from 'dn' param in magnet or fallback
                title = fallback_title
                if magnet_tag:
                    magnet = magnet_tag.get('href', '').replace('&amp;', '&')
                    query_str = magnet.split('?', 1)[1] if '?' in magnet else ""
                    query_params = urllib.parse.parse_qs(query_str)
                    if 'dn' in query_params:
                        title = urllib.parse.unquote(query_params['dn'][0])

                
                # Extract metadata from table cells
                metadata = ""
                tds = torrent_row.find_all('td')
                if len(tds) >= 3:
                    size = tds[1].get_text(strip=True)
                    seeds = tds[2].get_text(strip=True).replace('S:', '').strip()
                    metadata = f"   💾 {size} 🟢 Seeders: {seeds}"
                
                count += 1
                text_lines.append(f"{count}. <b>{html.escape(title)}</b>")
                if metadata:
                    text_lines.append(f"{metadata}\n")
                else:
                    text_lines.append("\n")
                
                # Truncate title to keep callback_data under 64 bytes
                short_title = (title[:20] + "..") if len(title) > 20 else title
                
                # We offer both direct download and magnet fallback
                keyboard_row.append(telegram.InlineKeyboardButton(f"DL {count}", callback_data=f"ijavdl_{count}_{dl_id}_{short_title}"))
                if info_hash:
                    # Use existing hash_ prefix but we need to pass enough info for handle_torrent_selection
                    keyboard_row.append(telegram.InlineKeyboardButton(f"🧲 {count}", callback_data=f"hash_{count}_{info_hash}"))



            if count == 0:
                await context.bot.edit_message_text(chat_id=chatid, message_id=status_msg.message_id, text=f"No valid magnet links found for '{query}'.")
                return

            reply_markup = telegram.InlineKeyboardMarkup([keyboard_row])
            final_text = "\n".join(text_lines)
            
            if cover_url:
                await context.bot.send_photo(
                    chat_id=chatid,
                    photo=cover_url,
                    caption=final_text,
                    reply_markup=reply_markup,
                    parse_mode=telegram.constants.ParseMode.HTML
                )
            else:
                await context.bot.send_message(
                    chat_id=chatid,
                    text=final_text,
                    reply_markup=reply_markup,
                    parse_mode=telegram.constants.ParseMode.HTML
                )

            await context.bot.delete_message(chat_id=chatid, message_id=status_msg.message_id)

    except Exception as e:
        import traceback
        print(f"JAV Search Error: {traceback.format_exc()}")
        await context.bot.edit_message_text(chat_id=chatid, message_id=status_msg.message_id, text=f"Error searching JAV: {str(e)[:100]}")

async def handle_ijav_download(update, context):
    query = update.callback_query
    await query.answer()
    
    # Expected format: ijavdl_{idx}_{id}_{title}
    data_parts = query.data.split("_")
    if len(data_parts) < 4:
        return
        
    dl_id = data_parts[2]
    title = data_parts[3]
    chatid = query.message.chat_id
    
    status_msg = await context.bot.send_message(chat_id=chatid, text=f"Downloading '{title}' directly from iJavTorrent, please wait...")
    
    try:
        safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c in (' ', '_', '-')]).rstrip()
        if not safe_title: safe_title = "download"
        file_path = f"./{safe_title}.torrent"
        
        target_url = f"https://ijavtorrent.com/download/{dl_id}"
        proxy_url = f"https://api.codetabs.com/v1/proxy?quest={target_url}"
        
        async with httpx.AsyncClient(timeout=40.0, follow_redirects=True, headers={"User-Agent": USER_AGENT}) as client:
            response = await client.get(proxy_url)
            
            if response.status_code != 200 or not response.content or not response.content.startswith(b'd8:'):
                await context.bot.edit_message_text(
                    chat_id=chatid, 
                    message_id=status_msg.message_id, 
                    text="Unable to download the torrent file directly. It might be currently unavailable."
                )
                return
                
            with open(file_path, 'wb') as f:
                f.write(response.content)
                
        with open(file_path, 'rb') as f:
            await context.bot.send_document(chat_id=chatid, document=f)
            
        await context.bot.delete_message(chat_id=chatid, message_id=status_msg.message_id)
        if os.path.exists(file_path): os.remove(file_path)
            
    except Exception as e:
        await context.bot.edit_message_text(
            chat_id=chatid, 
            message_id=status_msg.message_id, 
            text=f"Error downloading torrent: {str(e)[:100]}"
        )


async def help_command(update, context):
    chatid = update.effective_chat.id
    help_text = (
        "🔍 <b>Universal Search Bot Help</b>\n\n"
        "Simply type a movie, app, or JAV code (e.g., <code>Ipzz-198</code>) to search!\n\n"
        "<b>Available Commands:</b>\n"
        "• /start - Start the bot\n"
        "• /movies - Get currently playing movies\n"
        "• /apps - Get popular applications\n"
        "• /jav &lt;query&gt; - Direct JAV search\n"
        "• /help - Show this guide\n\n"
        "<b>Tips:</b>\n"
        "• If normal search fails, it automatically checks the JAV database.\n"
        "• Use the <b>🧲</b> button for magnet links if the direct file fails.\n"
        "• You can also paste a magnet link to convert it to a .torrent file."
    )
    await context.bot.send_message(chat_id=chatid, text=help_text, parse_mode=telegram.constants.ParseMode.HTML)
