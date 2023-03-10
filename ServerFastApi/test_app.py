from fastapi import FastAPI, WebSocket

ws = WebSocket('ws://localhost:8000/ws')

ws.onme