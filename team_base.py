
import json
import datetime
from typing import Dict, List

class TeamBase:
    def __init__(self):
        self.teams: Dict[str, Dict] = {}
        self.team_users: Dict[str, List[str]] = {}
        self.next_team_id = 1

    def create_team(self, request: str) -> str:
        request_data = json.loads(request)
        name = request_data["name"]
        description = request_data["description"]
        admin = request_data["admin"]

        if len(name) > 64:
            return json.dumps({"error": "Name can be max 64 characters"})
        if len(description) > 128:
            return json.dumps({"error": "Description can be max 128 characters"})
        if name in [team["name"] for team in self.teams.values()]:
            return json.dumps({"error": "Team name must be unique"})

        team_id = str(self.next_team_id)
        self.next_team_id += 1

        self.teams[team_id] = {
            "name": name,
            "description": description,
            "creation_time": datetime.datetime.now().isoformat(),
            "admin": admin
        }
        self.team_users[team_id] = []

        return json.dumps({"id": team_id})

    def list_teams(self) -> str:
        teams_list = list(self.teams.values())
        return json.dumps(teams_list)

    def describe_team(self, request: str) -> str:
        request_data = json.loads(request)
        team_id = request_data["id"]

        if team_id not in self.teams:
            return json.dumps({"error": "Team not found"})

        return json.dumps(self.teams[team_id])

    def update_team(self, request: str) -> str:
        request_data = json.loads(request)
        team_id = request_data["id"]
        team_data = request_data["team"]
        name = team_data["name"]
        description = team_data["description"]
        admin = team_data["admin"]

        if team_id not in self.teams:
            return json.dumps({"error": "Team not found"})
        if len(name) > 64:
            return json.dumps({"error": "Name can be max 64 characters"})
        if len(description) > 128:
            return json.dumps({"error": "Description can be max 128 characters"})
        if name in [team["name"] for tid, team in self.teams.items() if tid != team_id]:
            return json.dumps({"error": "Team name must be unique"})

        self.teams[team_id] = {
            "name": name,
            "description": description,
            "creation_time": self.teams[team_id]["creation_time"],
            "admin": admin
        }
        return json.dumps({"status": "success"})

    def add_users_to_team(self, request: str):
        request_data = json.loads(request)
        team_id = request_data["id"]
        users = request_data["users"]

        if team_id not in self.team_users:
            return json.dumps({"error": "Team not found"})
        if len(self.team_users[team_id]) + len(users) > 50:
            return json.dumps({"error": "Max users cap reached"})

        self.team_users[team_id].extend(users)
        self.team_users[team_id] = list(set(self.team_users[team_id]))
        return json.dumps({"status": "success"})

    def remove_users_from_team(self, request: str):
        request_data = json.loads(request)
        team_id = request_data["id"]
        users = request_data["users"]

        if team_id not in self.team_users:
            return json.dumps({"error": "Team not found"})

        self.team_users[team_id] = [user for user in self.team_users[team_id] if user not in users]
        return json.dumps({"status": "success"})

    def list_team_users(self, request: str):
        request_data = json.loads(request)
        team_id = request_data["id"]

        if team_id not in self.team_users:
            return json.dumps({"error": "Team not found"})

        users_list = [{"id": user_id, "name": user_id, "display_name": user_id} for user_id in self.team_users[team_id]]
        return json.dumps(users_list)