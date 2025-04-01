from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import database
import os
import uvicorn

app = FastAPI()
database.init_db()

class ActionRequest(BaseModel):
    user_id: str
    name: str = "Игрок"

@app.post("/mine")
def mine(req: ActionRequest):
    player = database.get_or_create_player(req.user_id, req.name)
    inventory = player["inventory"]
    inventory["руда"] = inventory.get("руда", 0) + 1
    database.update_player_field(req.user_id, "inventory", inventory)

    return {
        "message": "+5 токенов!",
        "inventory": inventory
    }

@app.get("/player/{user_id}")
def get_player(user_id: str):
    try:
        player = database.get_or_create_player(user_id)
        return player
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=FileResponse)
def index():
    return FileResponse(os.path.join(os.path.dirname(__file__), "../static/index.html"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)