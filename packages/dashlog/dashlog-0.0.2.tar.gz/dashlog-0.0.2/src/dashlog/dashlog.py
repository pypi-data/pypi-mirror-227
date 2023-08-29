import requests


class Dashlog:
    def __init__(self, token_user: str):
        self.base_url = "https://api.dashlog.app/v1"
        self.header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token_user,
        }

    def log(
        self,
        project: str,
        channel: str,
        title: str,
        description: str | None = None,
        data: dict[str, str | int | bool | float] = {},
        notify: bool | None = None,
    ):
        event = {
            "project": project,
            "channel": channel,
            "title": title,
            "description": description,
            "data": data,
            "notify": notify,
        }
        return requests.post(self.base_url + "/log", json=event, headers=self.header)
