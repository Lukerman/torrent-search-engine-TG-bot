def my_bot_token():
    return 'YOUR_BOT_TOKEN_HERE'

def pirat_api():
    return 'https://apibay.org/'

def movies_api():
    url = "https://api.themoviedb.org/3/movie/now_playing"
    api_key = "api_key=YOUR_TMDB_API_KEY"
    language = "en-US"
    limit_page = "1"
    movies_api_url = f"{url}?{api_key}&language={language}&page={limit_page}"
    return movies_api_url
