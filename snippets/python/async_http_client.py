"""Reusable High-Performance Async HTTP Client with Retries & Exponential Backoff."""
import asyncio
import logging
from typing import Any, Dict, Optional

try:
    import httpx
except ImportError:
    httpx = None

class AsyncHttpClient:
    def __init__(self, base_url: str = "", timeout: float = 10.0, max_retries: int = 3):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        
    async def get_json(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not httpx:
            raise ImportError("httpx package is required for AsyncHttpClient.")
            
        url = f"{self.base_url}{endpoint}" if self.base_url else endpoint
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for attempt in range(1, self.max_retries + 1):
                try:
                    response = await client.get(url, params=params)
                    response.raise_for_status()
                    return response.json()
                except Exception as err:
                    if attempt == self.max_retries:
                        raise err
                    await asyncio.sleep(0.5 * (2 ** (attempt - 1)))
        return {}
