from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

app = FastAPI()

# Простая база
players = {}

class ActionRequest(BaseModel):
    user_id: str

@app.post("/mine")
def mine(req: ActionRequest):
    player = players.setdefault(req.user_id, {"xp": 0, "tokens": 0, "inventory": {}})
    player["xp"] += 3
    player["tokens"] += 5
    player["inventory"].setdefault("руда", 0)
    player["inventory"]["руда"] += 1
    return player

@app.get("/player/{user_id}")
def get_player(user_id: str):
    if user_id not in players:
        raise HTTPException(status_code=404, detail="Игрок не найден")
    return players[user_id]

# Абсолютный путь к static
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../static"))
index_html = os.path.join(static_dir, "index.html")

@app.get("/", response_class=HTMLResponse)
def get_index():
    return FileResponse(index_html)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
