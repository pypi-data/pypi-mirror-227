__context__: tuple = (
    "API.INVALID",
    "API.VALID"
)


from typing import Any
from enum import StrEnum


class API(StrEnum):
    URL = "https://api.jokerapi.co/voice/v1/{}"
    def __translator__(val: str, url) -> str:
        return {
            "DIAL": url.format("dial"),
            "PLAY": url.format("play"),
            "PLAYTEXT": url.format("playtext"),
            "gAUDIO": url.format("gather"),
            "gText": url.format("gathertext"),
            "TRANSFER": url.format("transfer"),
            "HANGUP": url.format("hangup")
            }['val']

class Joker(StrEnum):
    """
    An enumeration of responses registered and heard from JokerAPI.
        Used in library to handle differed responses to be read.
    """
    __unknown__ = []

    INVALIDAUTH =  "invalid api key"
    INVALIDPARAM = "you are missing parameters"
    SERVERFAILURE = "Connection failed"
    NO_BALANCE = "you have no balance"
    INVALIDCOUNTRY = "this country is not whitelisted"
    
    GATHER_AUDIO = "playing audio while gathering"
    GATHER_TEXT = "playing text while gathering"

    CALL_ENDED = "call ended"

    PLAY_AUDIO = "playing audio"
    
    PLAY_TEXT = "playing text"
    
    TRANSFERING = "transfering call"

    def __INVALID__(value: str) -> list[Any, int]:
        return (_ := Joker.__unknown__.append([value])), len(Joker.__unknown__)[-1]