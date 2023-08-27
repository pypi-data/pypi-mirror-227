from octopype.account.getInfo import information
from octopype.account.update import update

class OctoAccount:
    def __init__(self, token) -> None:
        self.Token = token
        self.update = update(token)
    def info(self):
        return information(self.Token)

account = OctoAccount