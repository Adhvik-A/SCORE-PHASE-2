from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional


class BallEvent(BaseModel):
    player_id: Optional[str] = None
    bowler_id: Optional[str] = None

    batter: Optional[str] = None
    bowler: Optional[str] = None

    runs_off_bat: int = Field(0, ge=0, le=6)
    extras: int = Field(0, ge=0)
    extra_type: Optional[str] = None

    is_legal_delivery: bool = True
    wicket_fell: bool = False

    @field_validator("batter", "bowler")
    @classmethod
    def validate_names(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Player name cannot be empty")
        return v


class Innings(BaseModel):
    innings_id: str
    innings_number: int = Field(..., ge=1)

    events: List[BallEvent]

    @field_validator("events")
    @classmethod
    def validate_events(cls, v):
        if not v:
            raise ValueError("Events cannot be empty")
        return v


class MatchPayload(BaseModel):
    match_id: str
    venue: Optional[str] = None

    batting_team: str
    bowling_team: str

    innings: Innings
    target: Optional[int] = Field(None, ge=0)

    @model_validator(mode="after")
    def validate_logic(self):
        if self.batting_team == self.bowling_team:
            raise ValueError("Teams cannot be same")
        return self