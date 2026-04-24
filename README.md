# 🏏 Khel AI Match Scoreboard API (Phase 2)
# 🚀 API Objective

To build an event-driven cricket scoreboard engine using FastAPI that processes ball-by-ball match data and generates real-time match analytics including:

Score (runs/wickets)
Overs (cricket format)
Run rate
Extras (total + breakdown)
Top batter & bowler
Recent ball-by-ball feed
Required run rate (for chase)

# Endpoint
🔹 Base URL
https://score-phase-2.onrender.com
🔹 API Route
POST /scoreboard
🔹 Health Check
GET /health
🔹 Root
GET /

# Input Schema
{
  "match_id": "string",
  "venue": "string | null",

  "batting_team": "string",
  "bowling_team": "string",

  "innings": {
    "innings_id": "string",
    "innings_number": 1,

    "events": [
      {
        "player_id": "string",
        "bowler_id": "string",

        "batter": "string",
        "bowler": "string",

        "runs_off_bat": 0,
        "extras": 0,
        "extra_type": "wide | no_ball | bye | leg_bye | penalty | null",

        "is_legal_delivery": true,
        "wicket_fell": false
      }
    ]
  },

  "target": 0
}

# Output Schema
{
  "meta": {
    "api": "match-scoreboard",
    "version": "2.0",
    "status": "success"
  },
  "data": {
    "match_id": "string",
    "venue": "string",

    "innings_id": "string",
    "innings_number": 1,

    "batting_team": "string",
    "bowling_team": "string",

    "score": "runs/wickets",
    "overs": "x.y",
    "run_rate": 0.0,

    "legal_deliveries": 0,
    "fours": 0,
    "sixes": 0,

    "extras": {
      "total": 0,
      "breakdown": {
        "wide": 0,
        "no_ball": 0,
        "bye": 0,
        "leg_bye": 0,
        "penalty": 0
      }
    },

    "top_batter": "string",
    "top_bowler": "string",

    "recent_balls": [
      {
        "over_ball": "x.y",
        "striker": "string",
        "bowler": "string",
        "runs": 0,
        "wicket": false,
        "label": "FOUR | SIX | W | DOT | number"
      }
    ],

    "runs_needed": 0,
    "required_run_rate": 0.0
  },
  "errors": null
}

# Example Request
{
  "match_id": "IND_AUS_001",
  "venue": "Wankhede Stadium",

  "batting_team": "India",
  "bowling_team": "Australia",

  "innings": {
    "innings_id": "INN_1",
    "innings_number": 1,

    "events": [
      {
        "player_id": "P1",
        "bowler_id": "B1",
        "batter": "Rohit",
        "bowler": "Starc",
        "runs_off_bat": 4,
        "extras": 0,
        "extra_type": null,
        "is_legal_delivery": true,
        "wicket_fell": false
      },
      {
        "player_id": "P2",
        "bowler_id": "B1",
        "batter": "Gill",
        "bowler": "Starc",
        "runs_off_bat": 0,
        "extras": 1,
        "extra_type": "wide",
        "is_legal_delivery": false,
        "wicket_fell": false
      },
      {
        "player_id": "P3",
        "bowler_id": "B2",
        "batter": "Kohli",
        "bowler": "Cummins",
        "runs_off_bat": 6,
        "extras": 0,
        "extra_type": null,
        "is_legal_delivery": true,
        "wicket_fell": false
      }
    ]
  }
}

#  Example Response
{
  "meta": {
    "api": "match-scoreboard",
    "version": "2.0",
    "status": "success"
  },
  "data": {
    "match_id": "IND_AUS_001",
    "venue": "Wankhede Stadium",

    "innings_id": "INN_1",
    "innings_number": 1,

    "batting_team": "India",
    "bowling_team": "Australia",

    "score": "11/0",
    "overs": "0.2",
    "run_rate": 33.0,

    "legal_deliveries": 2,
    "fours": 1,
    "sixes": 1,

    "extras": {
      "total": 1,
      "breakdown": {
        "wide": 1,
        "no_ball": 0,
        "bye": 0,
        "leg_bye": 0,
        "penalty": 0
      }
    },

    "top_batter": "Kohli",
    "top_bowler": "Cummins",

    "recent_balls": [
      {
        "over_ball": "1.1",
        "striker": "Rohit",
        "bowler": "Starc",
        "runs": 4,
        "wicket": false,
        "label": "FOUR"
      },
      {
        "over_ball": "1.2",
        "striker": "Kohli",
        "bowler": "Cummins",
        "runs": 6,
        "wicket": false,
        "label": "SIX"
      }
    ],

    "runs_needed": null,
    "required_run_rate": null
  },
  "errors": null
}
# Validation Errors
 400 Bad Request
Runs or extras negative
Invalid extra_type
Empty events list
Wicket with runs > 0
Same batting & bowling team

Example:

{
  "detail": "Runs/extras cannot be negative"
}
 422 Validation Error
Missing required fields
Invalid data types

 500 Internal Error
Unexpected server failure

#  Integration Usage
Using Fetch (Frontend)
fetch("https://score-phase-2.onrender.com/scoreboard", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(payload)
})
.then(res => res.json())
.then(data => console.log(data));

#  Live Update Logic
Maintain events array in frontend
Append new ball after each delivery
Send full payload again
Update UI dynamically
#  Recommended UI Fields
Score → score
Overs → overs
Run Rate → run_rate
Extras → extras.total
Top Players
Recent Balls (live feed)
🏁 FINAL NOTE

# This API is a production-ready, event-driven cricket analytics backend with:

✔ Real-time scoring logic
✔ Proper validation & error handling
✔ Standard response format
✔ Deployment-ready architecture
✔ Frontend integration support