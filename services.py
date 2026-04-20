def format_overs(balls: int) -> str:
    """
    Proper cricket format:
    6 balls = 1.0 over
    7 balls = 1.1 overs
    13 balls = 2.1 overs
    """
    return f"{balls // 6}.{balls % 6}"


def get_match_scoreboard(payload: dict):

    events = payload.get("innings", {}).get("events", [])

    if not events:
        return {
            "match_id": payload.get("match_id"),
            "status": "No ball events found"
        }

    # ---------------- STATE ----------------
    runs = 0
    wickets = 0
    balls = 0

    legal_deliveries = 0
    fours = 0
    sixes = 0

    batter_stats = {}
    bowler_stats = {}

    recent_balls = []

    # ---------------- PROCESS EVENTS ----------------
    for event in events:

        runs_scored = event.get("runs_off_bat", 0)
        batter = event.get("batter")
        bowler = event.get("bowler")

        is_legal = event.get("is_legal_delivery", True)
        wicket = event.get("wicket_fell", False)

        # RUNS
        runs += runs_scored

        # BALL COUNT
        if is_legal:
            balls += 1
            legal_deliveries += 1

        # WICKET
        if wicket:
            wickets += 1
            recent_balls.append("W")
        else:
            recent_balls.append(str(runs_scored))

        # FOURS / SIXES
        if runs_scored == 4:
            fours += 1
        if runs_scored == 6:
            sixes += 1

        # BATTER STATS
        if batter:
            batter_stats[batter] = batter_stats.get(batter, 0) + runs_scored

        # BOWLER STATS
        if bowler:
            if bowler not in bowler_stats:
                bowler_stats[bowler] = 0
            if wicket:
                bowler_stats[bowler] += 1

    # ---------------- CALCULATIONS ----------------
    overs = format_overs(balls)
    run_rate = round((runs / (balls / 6)) if balls else 0, 2)

    top_batter = max(batter_stats, key=batter_stats.get) if batter_stats else "N/A"
    top_bowler = max(bowler_stats, key=bowler_stats.get) if bowler_stats else "N/A"

    # ---------------- CHASE LOGIC ----------------
    target = payload.get("target")
    runs_needed = None
    required_rr = None

    if target is not None:
        runs_needed = target - runs
        remaining_balls = max(1, 120 - balls)
        required_rr = round((runs_needed / remaining_balls) * 6, 2)

    # ---------------- RESPONSE ----------------
    return {
        "match_id": payload.get("match_id"),
        "batting_team": payload.get("batting_team"),
        "bowling_team": payload.get("bowling_team"),

        "score": f"{runs}/{wickets}",
        "overs": overs,
        "run_rate": run_rate,

        "legal_deliveries": legal_deliveries,

        "fours": fours,
        "sixes": sixes,

        "top_batter": top_batter,
        "top_bowler": top_bowler,

        "recent_balls": recent_balls[-6:],

        "runs_needed": runs_needed,
        "required_run_rate": required_rr,

        "status": "Live"
    }