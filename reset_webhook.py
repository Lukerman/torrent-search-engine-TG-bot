import httpx
import asyncio
from configs.url_shit import my_bot_token

async def fix():
    token = my_bot_token()
    print(f"Attempting to clear webhook for token ending in ...{token[-5:]}")
    async with httpx.AsyncClient(verify=False) as client:
        try:
            r = await client.post(
                f'https://api.telegram.org/bot{token}/deleteWebhook', 
                data={'drop_pending_updates': True},
                timeout=30.0
            )
            print(f"Response: {r.json()}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(fix())
