import httpx
from .enums import API
from typing import Any

class JokerAPI:
    def __init__(self, *args, **kwargs) -> None:
        return
    
    def DIAL(self,
             api_key: str,
             dial_to: str,
             dial_from: str,
             callback_url: str,
             proxy: str = {},
             request_method: str = "GET"
             ) -> dict:
        response: dict = httpx.request(request_method.upper() if request_method.upper() in ["GET", "POST"] else "GET", API.__translator__("DIAL", API.URL), proxies=proxy if proxy != {} else None).json()
        return response
        