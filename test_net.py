import httpx
import asyncio
import sys

async def test():
    urls = [
        "https://api.themoviedb.org/3/movie/now_playing?api_key=cc348043650d1146104248ee9c810fa6",
        "https://apibay.org/q.php?q=top100:201",
        "https://api.telegram.org/bot7541257434:AAHpUWVbHfygfeXUaUdhYYOR6an8Dktk_7s/getMe"
    ]
    
    async with httpx.AsyncClient(verify=False, timeout=10.0) as client:
        for url in urls:
            print(f"Testing {url}...")
            try:
                r = await client.get(url)
                print(f"  SUCCESS: {r.status_code}")
            except Exception as e:
                print(f"  FAILURE: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(test())
