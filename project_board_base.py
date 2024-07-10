import json
import datetime
from typing import Dict, List

class ProjectBoardBase:
    def __init__(self):
        self.boards: Dict[str, Dict] = {}
        self.tasks: Dict[str, Dict] = {}
        self.next_board_id = 1
        self.next_task_id = 1

    def create_board(self, request: str) -> str:
        request_data = json.loads(request)
        name = request_data["name"]
        description = request_data["description"]
        team_id = request_data["team_id"]

        if len(name) > 64:
            return json.dumps({"error": "Board name can be max 64 characters"})
        if len(description) > 128:
            return json.dumps({"error": "Description can be max 128 characters"})
        if any(board["name"] == name and board["team_id"] == team_id for board in self.boards.values()):
            return json.dumps({"error": "Board name must be unique for a team"})

        board_id = str(self.next_board_id)
        self.next_board_id += 1

        self.boards[board_id] = {
            "name": name,
            "description": description,
            "team_id": team_id,
            "creation_time": datetime.datetime.now().isoformat(),
            "status": "OPEN",
            "tasks": []
        }

        return json.dumps({"id": board_id})

    def close_board(self, request: str) -> str:
        request_data = json.loads(request)
        board_id = request_data["id"]

        if board_id not in self.boards:
            return json.dumps({"error": "Board not found"})
        if any(task["status"] != "COMPLETE" for task in self.boards[board_id]["tasks"]):
            return json.dumps({"error": "All tasks must be COMPLETE to close the board"})

        self.boards[board_id]["status"] = "CLOSED"
        self.boards[board_id]["end_time"] = datetime.datetime.now().isoformat()

        return json.dumps({"status": "success"})

    def add_task(self, request: str) -> str:
        request_data = json.loads(request)
        title = request_data["title"]
        description = request_data["description"]
        user_id = request_data["user_id"]
        board_id = request_data["board_id"]

        if board_id not in self.boards:
            return json.dumps({"error": "Board not found"})
        if self.boards[board_id]["status"] != "OPEN":
            return json.dumps({"error": "Can only add task to an OPEN board"})
        if len(title) > 64:
            return json.dumps({"error": "Task title can be max 64 characters"})
        if len(description) > 128:
            return json.dumps({"error": "Description can be max 128 characters"})
        if any(task["title"] == title for task in self.boards[board_id]["tasks"]):
            return json.dumps({"error": "Task title must be unique for a board"})

        task_id = str(self.next_task_id)
        self.next_task_id += 1

        task = {
            "id": task_id,
            "title": title,
            "description": description,
            "user_id": user_id,
            "creation_time": datetime.datetime.now().isoformat(),
            "status": "OPEN"
        }

        self.boards[board_id]["tasks"].append(task)
        self.tasks[task_id] = task

        return json.dumps({"id": task_id})

    def update_task_status(self, request: str) -> str:
        request_data = json.loads(request)
        task_id = request_data["id"]
        status = request_data["status"]

        if task_id not in self.tasks:
            return json.dumps({"error": "Task not found"})

        self.tasks[task_id]["status"] = status

        return json.dumps({"status": "success"})

    def list_boards(self, request: str) -> str:
        request_data = json.loads(request)
        team_id = request_data["id"]

        open_boards = [
            {"id": board_id, "name": board["name"]}
            for board_id, board in self.boards.items()
            if board["team_id"] == team_id and board["status"] == "OPEN"
        ]

        return json.dumps(open_boards)

    def export_board(self, request: str) -> str:
        request_data = json.loads(request)
        board_id = request_data["id"]

        if board_id not in self.boards:
            return json.dumps({"error": "Board not found"})

        board = self.boards[board_id]
        output = f"Board: {board['name']}\nDescription: {board['description']}\nCreation Time: {board['creation_time']}\n\nTasks:\n"
        
        for task in board["tasks"]:
            output += f"\nTask ID: {task['id']}\nTitle: {task['title']}\nDescription: {task['description']}\nUser ID: {task['user_id']}\nCreation Time: {task['creation_time']}\nStatus: {task['status']}\n"

        filename = f"board_{board_id}.txt"
        with open(filename, "w") as file:
            file.write(output)

        return json.dumps({"out_file": filename})