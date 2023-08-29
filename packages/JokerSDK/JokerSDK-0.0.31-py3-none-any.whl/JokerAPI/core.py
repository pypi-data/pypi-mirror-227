import httpx
from .enums import API, ExceptionMsg, Joker
from typing import Any
from .exceptions import *

class SDK:
    def __init__(self, api_key: str = False, **kwargs) -> None:
        self.api_key: str = api_key
        return
    
    def DIAL(self,
             dial_to: str,
             dial_from: str,
             callback_url: str,
             proxy: str = {},
             request_method: str = "GET"
             ) -> dict:
        
        if not self.api_key:
            raise REQUIREDAPIKEY(ExceptionMsg.REQUIRED_KEY)
        
        response: dict = httpx.request(request_method.upper() if request_method.upper() in ["GET", "POST"] else "GET", API.__translator__("DIAL", API.URL), proxies=proxy if proxy != {} else None).json()

        if response['status'] == Joker.INVALIDAUTH:
            self.api_key = None
            raise INVALIDAPIKEY(ExceptionMsg.INVALID_KEY)
        