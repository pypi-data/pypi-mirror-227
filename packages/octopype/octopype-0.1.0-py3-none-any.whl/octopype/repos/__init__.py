from octopype.repos.getrepo import getRepo

def getrepo(token, repository, organization):
    return getRepo(token, repository, organization)

class repo:
    def __init__(self, token) -> None:
        self.Token = token
    def getrepository(self, account, repository):
        if not isinstance(repository, str):
            raise TypeError("repository parameter must be 'str'")
        if not isinstance(account, str):
            raise TypeError("account parameter must be 'str'")
        return getrepo(self.Token, repository, account)
    
repository = repo
