from typing import Dict

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from .html import html
from .game import Player, Rock, Paper, Scissors, get_outcome


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[WebSocket, Player] = dict()

    async def connect(self, username: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[websocket] = Player(username)

    def disconnect(self, websocket: WebSocket):
        del self.active_connections[websocket]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    def opponent_online(self):
        # Check if there's someone to play against
        if len(self.active_connections.keys()) > 1:
            return True
        return False


manager = ConnectionManager()
app = FastAPI()


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(username, websocket)
    player = manager.active_connections[websocket]
    computer = Player() # Initiate the computer for play too
    try:
        # Start the main loop to talk to frontend
        while True:
            msg = await websocket.receive_text() # TODO: msg typing w FastAPI to distinguish msgs from client
            player.throw = msg # set throw
            # Send some info to player
            await manager.send_personal_message(f"You throw: {msg}", websocket)
            opponent_name = "Computer"
# TODO: msg typing to be able to play against friends, right now can ony play computer but multiple friends can be online
#            if manager.opponent_online():
#                opponent_name = "Friend"
            await manager.send_personal_message(f"Waiting for {opponent_name} to throw... ", websocket)
            if opponent_name == "Computer":
                await manager.send_personal_message(f"Computer throws: {computer.throw.alias}", websocket)
            msg = "It's a DRAW!"
            result = get_outcome(player, computer)
            if result is player:
                msg = "You WIN!"
            if result is computer:
                msg = "You LOST this round... "
            player.on_game_end(result, opponent=computer)
            computer.on_game_end(result) # Reset both computer and player
            await manager.send_personal_message(msg, websocket)

    except WebSocketDisconnect:
            manager.dosconnect(websocket) # Best practices from FastAPI example

