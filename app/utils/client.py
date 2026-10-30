import httpx
import asyncio
import logging

MAX_CONCURRENT_CALLS = asyncio.Semaphore(5)

logging.basicConfig(
    level=10,
    filename="client.log",
    format="%(asctime)s - %(levelname)s - %(message)s"
    )

async def retry_with_calls(url:str, payload: dict) -> dict:
    async with MAX_CONCURRENT_CALLS:
        async with httpx.AsyncClient() as client:
            for attempt in range(1,4):
                try:
                    response = client.post(url,json=payload)
                    response.raise_for_status()
                    return response.json()
                except Exception as e:
                    logging.warning("Attempt Failed")
                    if (attempt < 3):
                        await asyncio.sleep(2 ** attempt)
            
            return RuntimeError("Attemp Made But Runtime Error")
        
