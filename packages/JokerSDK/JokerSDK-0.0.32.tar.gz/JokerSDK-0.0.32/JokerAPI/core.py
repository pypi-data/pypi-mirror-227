import httpx, asyncio
from .enums import API, ExceptionMsg, Joker
from typing import Any, Awaitable
from .exceptions import *

class SDK:
    def __init__(self, *args, api_key: str = False, **kwargs) -> None:
        self.api_key: str = api_key
    
    """
    Run an asynchronous function using asyncio's event loop.
        This function takes an asynchronous function as an argument and runs it within asyncio's event loop.

        Parameters:
        -----------
        func : Awaitable[None]
            The asynchronous function to be executed.

        Returns:
        --------
        None

        Examples:
        ---------
        JokerINIT.run_async(JokerINIT(api_key="test"))

        --> run_async(async_function())
        ---> Preference Any[asyncio.run, run_async]
    """
    def run_async(func: Awaitable[None], *args, **kwargs) -> None:
        return asyncio.run(func)

    """
    Statically defined `dial` function capable of creating and handling API requests to the
        `voice/v1/dial` endpoint via JokerAPI.co.

        Parameters:
        -----------
        dial_to : str
            The destination number to dial (parent).

        dial_from : str
            The caller ID to display when dialing the destination number (child).

        callback_url : str, required.
            The URL where status change notifications are sent, corresponding to the user's API callback server.

        **kwargs : dict, optional
            Additional optional parameters.

            request_method : str
                The HTTP method for the API request (default is 'GET', supports 'get' or 'post').

            proxy : str or dict
                Proxy configuration for the API request.
                Examples: 'all', 'all://*api.jokerapi.co', 'http://', 'https://', 
                {"http": "USERNAME:PASSWORD@DOMAIN:PORT", "https": "USERNAME:PASSWORD@DOMAIN:PORT"}.

        Returns:
        --------
        int
            The status code of the API response.
        
        Raises:
        -------
        REQUIREDAPIKEY
            If the API key is missing.

        INVALIDAPIKEY
            If the API key is invalid.
    """
    async def dial(self,
             dial_to: str,
             dial_from: str,
             callback_url: str = "https://0.0.0.0/*",
             **kwargs
             ) -> int:
        
        if not self.api_key:
            raise REQUIREDAPIKEY(ExceptionMsg.REQUIRED_KEY)
        
        response = httpx.request(
            "GET" if not kwargs.get("request_method", False) else kwargs['request_method'] if kwargs['request_method'] in ["GET", "POST"] else "GET",
            API.__translator__("DIAL", API.URL, {"key": self.api_key, "to": dial_to, "from": dial_from, "url": callback_url}),
            proxies=None if not kwargs.get("proxy", False) else kwargs['proxy'] if isinstance(kwargs['proxy'], dict) else None
        ).json()

        if response['context'] == Joker.INVALIDAUTH:
            self.api_key = None
            raise INVALIDAPIKEY(ExceptionMsg.INVALID_KEY)

        return 1
    