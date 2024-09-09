from fastapi import FastAPI
import socketio
from fastapi.middleware.cors import CORSMiddleware

SOCKETIO_PATH = "bids"
CLIENT_URLS = ["ws://localhost:3000", '*']

sio = socketio.AsyncServer(async_mode="", cors_allowed_origins=CLIENT_URLS)
sio_app = socketio.ASGIApp(socketio_server=sio, socketio_path=SOCKETIO_PATH)
app = FastAPI()

app.mount("/socket", sio_app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CLIENT_URLS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@sio.event
async def connect(sid, environ):
    print(f"Client {sid} connected")

@sio.event
async def disconnect(sid):
    print(f"Client {sid} disconnected")

@sio.event
async def chat_message(sid, data):
    room = data.get("room")
    bid = data.get("bid")
    print(f"Received message from {sid}: {bid} in room {room}")
    await sio.emit("my_room_event", {"success": True, "data": {"price": bid}}, room=room)

@sio.event
async def join_room(sid, data):
    room = data.get("room")
    await sio.enter_room(sid, room)
    print(f"User {sid} joined room {room}")
    await sio.emit("my_room_event", {"success": True, "data": {"price": "1000"}}, room=room)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)