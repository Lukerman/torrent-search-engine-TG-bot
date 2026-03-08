# 🚀 Advanced Torrent Search Telegram Bot

A high-performance, asynchronous Telegram bot built with `python-telegram-bot` v20+ that provides a seamless search experience for movies, apps, and JAV content. Features interactive inline buttons, direct `.torrent` file delivery, and automated search fallbacks.

## ✨ Key Features

- **🔍 Universal Search**: Type any query (movie name, app title, or JAV code) and the bot will automatically route it to the correct engine.
- **🔞 Integrated JAV Engine**: Native support for JAV searches with direct `.torrent` file delivery via high-speed proxy.
- **⚡ Interactive UI**: Uses modern `InlineKeyboardMarkup` buttons for one-tap downloads.
- **📂 Direct File Delivery**: Automatically converts magnet links (or site download IDs) into downloadable `.torrent` files directly in the chat.
- **🔄 Smart Fallback**: If the primary torrent database (APIBay) has no results, the bot automatically checks the JAV engine seamlessly.
- **🛡️ Secure & Clean**: Protected configuration system (`.gitignore`) to prevent secret leakage.

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Lukerman/torrent-search-engine-TG-bot.git
cd torrent-search-engine-TG-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
1. Copy the example configuration file:
   ```bash
   cp configs/url_shit_example.py configs/url_shit.py
   ```
2. Open `configs/url_shit.py` and replace the placeholders with your actual:
   - **Telegram Bot Token** (from @BotFather)
   - **TMDB API Key** (from [TheMovieDB](https://www.themoviedb.org/documentation/api))

### 4. Run the Bot
```bash
python app.py
```

## 📖 Usage

- **Start**: Send `/start` to initialize the bot.
- **Search**: Simply type what you are looking for (e.g., `Inception` or `IPZZ-198`).
- **JAV Specific**: Use `/jav <query>` for direct JAV-only searches.
- **Download**: Tap the numbered buttons `[ 1 ]`, `[ 2 ]`, etc., to receive your `.torrent` file instantly.

## 📦 Tech Stack

- **Language**: Python 3.10+
- **Library**: `python-telegram-bot` (Async version)
- **Networking**: `httpx` (Asynchronous HTTP requests)
- **Parsing**: `BeautifulSoup4`

---
Made with ❤️ by [Lukerman](https://github.com/Lukerman)
