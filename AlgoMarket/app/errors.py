class UsernameExist(Exception):
    """Raise when same username exists"""
    pass

class EmailExist(Exception):
    """Raise when same email exists"""
    pass

class EmailNotVerified(Exception):
    """Raised when the email is not verified"""
    pass

class IncorrectPassword(Exception):
    """Raised when password is incorrect"""
    pass