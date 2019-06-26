class UserNotFoundInLDAP(Exception):
    """Raised when a user is not found in AD. This sometimes happens even if the user is in AD, but the server is misbehaving."""
