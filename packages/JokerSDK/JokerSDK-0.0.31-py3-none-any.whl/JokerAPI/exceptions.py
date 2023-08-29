class REQUIREDAPIKEY(Exception):
    "Raised whenever a API key is not present"

class INVALIDAPIKEY(Exception):
    "Raised whenever an API key is invalid > Joker.INVALIDAUTH"