from pydantic import BaseModel
from typing import List, Optional


class BallEvent(BaseModel):
    runs_off_bat: int = 0
    batter: Optional[str] = None
    bowler: Optional[str] = None
    is_legal_delivery: bool = True
    wicket_fell: bool = False


class Innings(BaseModel):
    events: List[BallEvent]


class MatchPayload(BaseModel):
    match_id: str
    batting_team: str
    bowling_team: str
    innings: Innings
    target: Optional[int] = None