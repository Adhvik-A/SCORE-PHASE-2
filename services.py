from fastapi import HTTPException


def success_response(data):
    return {
        "meta": {
            "api": "match-scoreboard",
            "version": "2.0",
            "status": "success"
        },
        "data": data,
        "errors": None
    }


def format_overs(balls):
    return f"{balls // 6}.{balls % 6}"


def get_match_scoreboard(payload: dict):

    innings = payload.get("innings", {})
    events = innings.get("events")

    if not events:
        raise HTTPException(status_code=400, detail="Events cannot be empty")

    total_runs = wickets = balls = 0
    fours = sixes = legal = 0

    batter_stats = {}
    bowler_stats = {}

    # ---------------- EXTRAS ----------------
    total_extras = 0
    extras_breakdown = {
        "wide": 0,
        "no_ball": 0,
        "bye": 0,
        "leg_bye": 0,
        "penalty": 0
    }

    recent = []
    current_ball = 0

    for e in events:

        runs_off_bat = e.get("runs_off_bat", 0)
        extras = e.get("extras", 0)
        extra_type = e.get("extra_type")

        if runs_off_bat < 0 or extras < 0:
            raise HTTPException(status_code=400, detail="Runs/extras cannot be negative")

        # ---------------- SCORING ----------------
        total = runs_off_bat + extras
        total_runs += total

        # ---------------- EXTRAS TRACK ----------------
        total_extras += extras

        if extra_type:
            if extra_type not in extras_breakdown:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid extra_type: {extra_type}"
                )
            extras_breakdown[extra_type] += extras

        batter = e.get("batter")
        bowler = e.get("bowler")

        is_legal = e.get("is_legal_delivery", True)
        wicket = e.get("wicket_fell", False)

        if is_legal:
            balls += 1
            legal += 1
            current_ball += 1

        over_number = (current_ball // 6) + 1
        ball_number = (current_ball % 6) or 6

        if wicket:
            wickets += 1

        if runs_off_bat == 4:
            fours += 1
        if runs_off_bat == 6:
            sixes += 1

        # ---------------- BATTER ----------------
        if batter:
            batter_stats[batter] = batter_stats.get(batter, 0) + runs_off_bat

        # ---------------- BOWLER ----------------
        if bowler:
            if bowler not in bowler_stats:
                bowler_stats[bowler] = {"wickets": 0, "runs_conceded": 0}

            bowler_stats[bowler]["runs_conceded"] += total

            if wicket:
                bowler_stats[bowler]["wickets"] += 1

        # ---------------- LABEL ----------------
        if wicket:
            label = "W"
        elif runs_off_bat == 4:
            label = "FOUR"
        elif runs_off_bat == 6:
            label = "SIX"
        elif total == 0:
            label = "DOT"
        else:
            label = str(total)

        # ---------------- RECENT BALL ----------------
        recent.append({
            "over_ball": f"{over_number}.{ball_number}",
            "striker": batter,
            "bowler": bowler,
            "runs": total,
            "wicket": wicket,
            "label": label
        })

    overs = format_overs(balls)
    run_rate = round((total_runs / (balls / 6)), 2) if balls else 0

    # ---------------- TOP PLAYERS ----------------
    top_batter = max(batter_stats, key=batter_stats.get) if batter_stats else "N/A"

    top_bowler = "N/A"
    if bowler_stats:
        top_bowler = max(
            bowler_stats.items(),
            key=lambda x: (x[1]["wickets"], -x[1]["runs_conceded"])
        )[0]

    # ---------------- CHASE ----------------
    target = payload.get("target")
    runs_needed = required_rr = None

    if target is not None:
        runs_needed = target - total_runs
        remaining = max(1, 120 - balls)
        required_rr = round((runs_needed / remaining) * 6, 2)

    result = {
        "match_id": payload.get("match_id"),
        "venue": payload.get("venue"),

        "innings_id": innings.get("innings_id"),
        "innings_number": innings.get("innings_number"),

        "batting_team": payload.get("batting_team"),
        "bowling_team": payload.get("bowling_team"),

        "score": f"{total_runs}/{wickets}",
        "overs": overs,
        "run_rate": run_rate,

        "legal_deliveries": legal,
        "fours": fours,
        "sixes": sixes,

        "extras": {
            "total": total_extras,
            "breakdown": extras_breakdown
        },

        "top_batter": top_batter,
        "top_bowler": top_bowler,

        "recent_balls": recent[-6:],

        "runs_needed": runs_needed,
        "required_run_rate": required_rr
    }

    return success_response(result)