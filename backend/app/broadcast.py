from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.connections: dict[str, WebSocket] = {}

    async def connect(self, user: str, websocket: WebSocket):
        await websocket.accept()
        self.connections[user] = websocket
    
    def disconnect(self, user: str):
        self.connections.pop(user, None)
    
    async def broadcast(self, payload: dict):
        for socket in self.connections.values():
            await socket.send_json(payload)

manager = ConnectionManager()