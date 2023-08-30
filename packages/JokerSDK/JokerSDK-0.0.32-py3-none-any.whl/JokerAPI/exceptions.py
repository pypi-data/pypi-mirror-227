class REQUIREDAPIKEY(Exception):
    """
    Exception raised when an API key is not provided for a required operation.

    This exception is raised when an API key is expected but not provided, preventing the execution of certain actions.
    """

class INVALIDAPIKEY(Exception):
    """
    Exception raised when an API key is invalid, usually indicating authorization failure.

    This exception is raised when the provided API key is incorrect or unauthorized, leading to inability to perform
    authorized actions such as dialing or controlling call flow.
    """
