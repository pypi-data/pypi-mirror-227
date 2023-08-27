from requests import patch
from octopype.account.status_checker import account_update_check

class UpdateInfo:
    def __init__(self, token) -> None:
        if not isinstance(token, str): raise TypeError("authentication token must be 'str'")
        self.Token = token
    def display_name(self, to: str) -> int:
        if not isinstance(to, str):
            raise TypeError("new display_name must be 'str'")
        request = patch(headers={"Accept":"application/vnd.github+json", "Authorization":f"Bearer {self.Token}","X-GitHub-Api-Version":"2022-11-28"}, json={"name":to}, url="https://api.github.com/user")
        account_update_check(request)
        return request.text
    def public_email(self, to: str) -> int:
        if not isinstance(to, str):
            raise TypeError("new public_email must be 'str'")
        request = patch(headers={"Accept":"application/vnd.github+json", "Authorization":f"Bearer {self.Token}","X-GitHub-Api-Version":"2022-11-28"}, json={"email":to}, url="https://api.github.com/user")
        account_update_check(request)
        return request.status_code
    def blog_url(self, to: str) -> int:
        if not isinstance(to, str):
            raise TypeError("new blog_url must be 'str'")
        request = patch(headers={"Accept":"application/vnd.github+json", "Authorization":f"Bearer {self.Token}","X-GitHub-Api-Version":"2022-11-28"}, json={"blog":to}, url="https://api.github.com/user")
        account_update_check(request)
        return request.status_code
    def twitter_username(self, to: str) -> int:
        if not isinstance(to, str) and to != None:
            raise TypeError("new twitter_username must be 'str' or None")
        request = patch(headers={"Accept":"application/vnd.github+json", "Authorization":f"Bearer {self.Token}","X-GitHub-Api-Version":"2022-11-28"}, json={"twitter_username":to}, url="https://api.github.com/user")
        account_update_check(request)
        return request.status_code
    def company(self, to: str) -> int:
        if not isinstance(to, str):
            raise TypeError("new company must be 'str'")
        request = patch(headers={"Accept":"application/vnd.github+json", "Authorization":f"Bearer {self.Token}","X-GitHub-Api-Version":"2022-11-28"}, json={"company":to}, url="https://api.github.com/user")
        account_update_check(request)
        return request.status_code
    def location(self, to: str) -> int:
        if not isinstance(to, str):
            raise TypeError("new location must be 'str'")
        request = patch(headers={"Accept":"application/vnd.github+json", "Authorization":f"Bearer {self.Token}","X-GitHub-Api-Version":"2022-11-28"}, json={"location":to}, url="https://api.github.com/user")
        account_update_check(request)
        return request.status_code
    def hireable(self, to: bool) -> int:
        if not isinstance(to, bool):
            raise TypeError("new hireable status must be 'bool'")
        request = patch(headers={"Accept":"application/vnd.github+json", "Authorization":f"Bearer {self.Token}","X-GitHub-Api-Version":"2022-11-28"}, json={"hireable":to}, url="https://api.github.com/user")
        account_update_check(request)
        return request.status_code
    def bio(self, to: str) -> int:
        if not isinstance(to, str):
            raise TypeError("new bio must be 'str'")
        request = patch(headers={"Accept":"application/vnd.github+json", "Authorization":f"Bearer {self.Token}","X-GitHub-Api-Version":"2022-11-28"}, json={"bio":to}, url="https://api.github.com/user")
        account_update_check(request)
        return request.status_code
    
update = UpdateInfo