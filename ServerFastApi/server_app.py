from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
import json

app = FastAPI()

connected_clients = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    # await websocket.accept()
    client_name = None
    client_key = None
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    connected_clients.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            # message_json = json.loads(message)
            # await manager.broadcast(f"{client_id}: {message_json}")
            # await manager.send_personal_message(f"You: {data}", websocket)
            message = {"time":current_time,"clientId":client_id,"message":data}
            await manager.broadcast(json.dumps(message))


            # if "name" in data:
            #     client_name = data["name"]
            #     client_key = data["key"]
            #     print(client_key)
            # else:
            #     sender = message_json["sender"]
            #     message = message_json["message"]
            #     p = message_json["p"]
            #     recipient_key = message_json["key"]
            #     await send_message(message, p, recipient_key)
            #     print("TESTE")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        message = {"time":current_time,"clientId":client_id,"message":"Offline"}
        await manager.broadcast(json.dumps(message))
        
        # connected_clients.remove(websocket)
        # await manager.broadcast(f"Client #{client_id} left the chat")


# async def send_message(message: List[int], p: int, recipient_key: str):
#     for client in connected_clients:
#         client_key = json.loads(recipient_key)
#         q_key = client_key[0]
#         h_key = client_key[1]
#         g_key = client_key[2]
#         print(client)

#         if q_key == q and h_key == h and g_key == g:
#             await client.send_text(json.dumps({"sender": sender, "message": message, "p": p}))
#             break
