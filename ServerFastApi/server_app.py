from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
import json


app = FastAPI()


connected_clients = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client_name = None
    client_key = None
    connected_clients.append(websocket)

    try:
        while True:
            message = await websocket.receive_text()
            message_json = json.loads(message)
            if "name" in message_json:
                client_name = message_json["name"]
                client_key = message_json["key"]
                print(client_key)
            else:
                sender = message_json["sender"]
                message = message_json["message"]
                p = message_json["p"]
                recipient_key = message_json["key"]
                await send_message(message, p, recipient_key)
                print("TESTE")

    except WebSocketDisconnect:
        connected_clients.remove(websocket)


async def send_message(message: List[int], p: int, recipient_key: str):
    for client in connected_clients:
        client_key = json.loads(recipient_key)
        q_key = client_key[0]
        h_key = client_key[1]
        g_key = client_key[2]
        print(client)

        if q_key == q and h_key == h and g_key == g:
            await client.send_text(json.dumps({"sender": sender, "message": message, "p": p}))
            break
