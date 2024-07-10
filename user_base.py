import json
import datetime
from typing import Dict, List

class UserBase:
    def __init__(self):
        self.users: Dict[str, Dict] = {}
        self.user_teams: Dict[str, List[str]] = {}
        self.next_user_id = 1

    def create_user(self, request: str) -> str:
        request_data = json.loads(request)
        name = request_data["name"]
        display_name = request_data["display_name"]

        if len(name) > 64:
            return json.dumps({"error": "Name can be max 64 characters"})
        if len(display_name) > 64:
            return json.dumps({"error": "Display name can be max 64 characters"})
        if name in [user["name"] for user in self.users.values()]:
            return json.dumps({"error": "User name must be unique"})

        user_id = str(self.next_user_id)
        self.next_user_id += 1

        self.users[user_id] = {
            "name": name,
            "display_name": display_name,
            "creation_time": datetime.datetime.now().isoformat()
        }
        self.user_teams[user_id] = []

        return json.dumps({"id": user_id})

    def list_users(self) -> str:
        users_list = list(self.users.values())
        return json.dumps(users_list)

    def describe_user(self, request: str) -> str:
        request_data = json.loads(request)
        user_id = request_data["id"]

        if user_id not in self.users:
            return json.dumps({"error": "User not found"})

        return json.dumps(self.users[user_id])

    def update_user(self, request: str) -> str:
        request_data = json.loads(request)
        user_id = request_data["id"]
        user_data = request_data["user"]
        display_name = user_data["display_name"]

        if user_id not in self.users:
            return json.dumps({"error": "User not found"})
        if len(display_name) > 64:
            return json.dumps({"error": "Display name can be max 64 characters"})

        self.users[user_id]["display_name"] = display_name
        return json.dumps({"status": "success"})

    def get_user_teams(self, request: str) -> str:
        request_data = json.loads(request)
        user_id = request_data["id"]

        if user_id not in self.users:
            return json.dumps({"error": "User not found"})

        teams_list = [{"name": team["name"], "description": team["description"], "creation_time": team["creation_time"]}
                      for team_id in self.user_teams[user_id] if team_id in self.teams]
        return json.dumps(teams_list)