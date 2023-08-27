from octopype.account import account as account_object
from octopype.repos import repository as repository_object

class OctoPype:
    def __init__(self, token) -> None:
        self.Token = token
        if not isinstance(self.Token, str):
            raise TypeError("authentication token must be 'str'")
        self.account = account_object(token)
        self.repository = repository_object(token)