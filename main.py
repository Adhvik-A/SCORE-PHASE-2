from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import MatchPayload
from services import get_match_scoreboard

app = FastAPI(
    title="Khel AI Match Scoreboard API",
    description="""
Event-driven cricket scoreboard engine.

Processes ball-by-ball data and returns:
- Score, overs, run rate
- Extras breakdown
- Top batter & bowler
- Recent balls (structured)
- Chase metrics
""",
    version="2.0.0"
)

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- ROOT ----------------
@app.get("/", tags=["Root"])
def root():
    return {
        "meta": {
            "api": "match-scoreboard",
            "version": "2.0.0",
            "status": "running"
        },
        "message": "Welcome to Khel AI Match Scoreboard API 🚀",
        "endpoints": {
            "health": "/health",
            "scoreboard": "/scoreboard",
            "docs": "/docs"
        }
    }

# ---------------- HEALTH ----------------
@app.get("/health", tags=["Health"])
def health():
    return {
        "meta": {
            "api": "match-scoreboard",
            "version": "2.0.0",
            "status": "ok"
        }
    }

# ---------------- SCOREBOARD ----------------
@app.post("/scoreboard", tags=["Scoreboard"])
def scoreboard(payload: MatchPayload):
    return get_match_scoreboard(payload.dict())