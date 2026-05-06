from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        if username not in self.active_connections:
            self.active_connections[username] = []
        self.active_connections[username].append(websocket)

    def disconnect(self, websocket: WebSocket, username: str):
        if username in self.active_connections:
            self.active_connections[username].remove(websocket)
            if not self.active_connections[username]:
                del self.active_connections[username]

    # async def send_personal_message(self, username: str, message: dict):
    #     if username in self.active_connections:
    #         for connection in self.active_connections[username]:
    #             await connection.send_json(message)

    async def send_personal_message(self, username: str, message: dict):
        if username not in self.active_connections:
            return  # user is offline — notification already saved in DB, WS is non-fatal

        dead_connections = []
        for connection in self.active_connections[username]:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"⚠️ WebSocket send failed for '{username}': {e}")
                dead_connections.append(connection)

        # Clean up stale connections
        for conn in dead_connections:
            self.active_connections[username].remove(conn)
        if not self.active_connections.get(username):
            self.active_connections.pop(username, None)

    async def broadcast(self, message: dict):
        for user_conns in self.active_connections.values():
            for conn in user_conns:
                await conn.send_json(message)


manager = ConnectionManager()