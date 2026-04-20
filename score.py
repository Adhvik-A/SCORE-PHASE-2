from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import MatchPayload
from services import get_match_scoreboard

app = FastAPI(title="Khel AI Cricket Engine")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/scoreboard")
def scoreboard(payload: MatchPayload):
    try:
        return get_match_scoreboard(payload.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))