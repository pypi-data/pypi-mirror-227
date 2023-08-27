from requests import get
from json import loads

class AccountPlan:
    def __init__(self, given_json: dict) -> None:
        self.name = given_json["plan"]["name"]
        self.space = given_json["plan"]["space"]
        self.collaborators = given_json["plan"]["collaborators"]
        self.private_repositories = given_json["plan"]["private_repos"]

class AccountInfo:
    def __init__(self, token) -> None:
        raw = loads(get(headers={"Accept":"application/vnd.github+json", "Authorization":f"Bearer {token}", "X-GitHub-Api-Version":"2022-11-28"}, url="https://api.github.com/user").text)
        plan = AccountPlan(raw)
        self.plan = plan
        self.name = raw["login"]
        self.id = raw["id"]
        self.node_id = raw["node_id"]
        self.avatar = raw["avatar_url"]
        self.gravatar = raw["gravatar_id"]
        self.api_url = raw["url"]
        self.github_page = raw["html_url"]
        self.followers_api = raw["followers_url"]
        self.following_api = raw["following_url"]
        self.gists_api = raw["gists_url"]
        self.starred_api = raw["starred_url"]
        self.subscriptions_api = raw["subscriptions_url"]
        self.organizations_api = raw["organizations_url"]
        self.repositories_api = raw["repos_url"]
        self.events_api = raw["events_url"]
        self.received_events_api = raw["received_events_url"]
        self.account_type = raw["type"]
        self.is_administrator = raw["site_admin"]
        self.display_name = raw["name"]
        self.company = raw["company"]
        self.blog_url = raw["blog"]
        self.location = raw["location"]
        self.public_email = raw["email"]
        self.hireable = raw["hireable"]
        self.bio = raw["bio"]
        self.twitter_username = raw["twitter_username"]
        self.public_repositories_amount = raw["public_repos"]
        self.public_gists_amount = raw["public_gists"]
        self.followers_amount = raw["followers"]
        self.following_amount = raw["following"]
        self.created_timestamp = raw["created_at"]
        self.updated_timestamp = raw["updated_at"]
        self.private_gists_amount = raw["private_gists"]
        self.total_private_repositories_amount = raw["total_private_repos"]
        self.owned_private_repositories_amount = raw["owned_private_repos"]
        self.used_data = raw["disk_usage"]
        self.collaborators_amount = raw["collaborators"]
        self.two_factor_auth_enabled = raw["two_factor_authentication"]

def information(token):
    return AccountInfo(token)