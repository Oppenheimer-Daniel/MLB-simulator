# models/season.py
import os
import random
import pandas as pd
from team import Team
from game import Game

class Season:
    def __init__(self, teams):
        self.teams = teams
        self.records = {team.name: {"W": 0, "L": 0, "R": 0, "RA": 0} for team in teams}

    def _record_game(self, home: Team, away: Team, score_home: int, score_away: int):
        # update runs
        self.records[home.name]["R"] += score_home
        self.records[home.name]["RA"] += score_away
        self.records[away.name]["R"] += score_away
        self.records[away.name]["RA"] += score_home

        # update W/L
        if score_home > score_away:
            self.records[home.name]["W"] += 1
            self.records[away.name]["L"] += 1
            return home.name
        else:
            self.records[away.name]["W"] += 1
            self.records[home.name]["L"] += 1
            return away.name

    def play_game(self, home: Team, away: Team):
        g = Game(home, away)
        # prefer simulate_game if available
        if hasattr(g, "simulate_game"):
            result = g.simulate_game()
            # expect (winner, away_score, home_score)
            if isinstance(result, tuple) and len(result) == 3:
                winner, away_score, home_score = result
            else:
                # fallback: if simulate_game returns just scores dict
                away_score = result[0]
                home_score = result[1]
                winner = home.name if home_score > away_score else away.name
        else:
            # backward-compatible: call play_game() then read g.score
            g.play_game()
            home_score = g.score.get(home.name, 0)
            away_score = g.score.get(away.name, 0)
            winner = home.name if home_score > away_score else away.name

        return self._record_game(home, away, home_score, away_score)

    def simulate_season(self):
        print("\n🏟️ Simulating Full MLB Season...")

        # normalize grouping by league/division
        leagues = {}
        for t in self.teams:
            league = (t.league or "Unknown").strip().upper()
            division = (t.division or "Unknown").strip().title()
            leagues.setdefault(league, {}).setdefault(division, []).append(t)

        league_keys = list(leagues.keys())
        print(f"Detected leagues: {league_keys}")

        # helper
        def games_played(team: Team):
            rec = self.records[team.name]
            return rec["W"] + rec["L"]

        # Divisional games (~13 per opponent)
        for league, divisions in leagues.items():
            for div_name, div_teams in divisions.items():
                for i, t1 in enumerate(div_teams):
                    for j, t2 in enumerate(div_teams):
                        if i >= j:
                            continue
                        for _ in range(13):
                            self.play_game(t1, t2)

        # Intra-league non-division games (~6 per opponent)
        for league, divisions in leagues.items():
            league_teams = [x for d in divisions.values() for x in d]
            for i, t1 in enumerate(league_teams):
                for j, t2 in enumerate(league_teams):
                    if i >= j:
                        continue
                    if t1.division == t2.division:
                        continue
                    for _ in range(6):
                        self.play_game(t1, t2)

        # Interleague games (~3 per opponent, sampled opponents)
        if len(league_keys) >= 2:
            # pick two leagues (if more, pick first two keys)
            key_a, key_b = league_keys[0], league_keys[1]
            a_teams = [t for d in leagues[key_a].values() for t in d]
            b_teams = [t for d in leagues[key_b].values() for t in d]

            for t1 in a_teams:
                opponents = random.sample(b_teams, min(20, len(b_teams)))
                for t2 in opponents:
                    for _ in range(3):
                        self.play_game(t1, t2)

        TARGET = 162
        teams_list = list(self.teams)
        def games_played(t): return self.records[t.name]["W"] + self.records[t.name]["L"]

        # While some teams below target, pair them up fairly
        while True:
            under = [t for t in teams_list if games_played(t) < TARGET]
            over = [t for t in teams_list if games_played(t) > TARGET]
            if not under:
                break

            t1 = random.choice(under)
            # choose opponent not itself & not over-limit if possible
            opp_candidates = [t for t in teams_list if t.name != t1.name and games_played(t) < TARGET]
            if not opp_candidates:
                opp_candidates = [t for t in teams_list if t.name != t1.name]
            t2 = random.choice(opp_candidates)

            # Randomize who is home
            if random.random() < 0.5:
                self.play_game(t1, t2)
            else:
                self.play_game(t2, t1)

            # If both exceed 162, undo the extra one by subtracting last result (rare)
            for t in [t1, t2]:
                gp = games_played(t)
                if gp > TARGET:
                    # remove one random win/loss to balance out
                    if self.records[t.name]["W"] > 0:
                        self.records[t.name]["W"] -= 1
                    else:
                        self.records[t.name]["L"] -= 1



    def print_standings(self):
        print("\n=== FINAL MLB STANDINGS ===")

        # Group teams by league/division
        league_division_map = {}
        for team in self.teams:
            league_division_map.setdefault(team.league, {}).setdefault(team.division, []).append(team)

        # Helper to sort teams in each division by record
        def sort_key(t):
            rec = self.records[t.name]
            return (rec["W"], -rec["RA"])  # wins descending, fewer runs allowed is better

        # Print standings by league/division
        for league, divisions in league_division_map.items():
            print(f"\n🏆 {league} League")
            for division, div_teams in divisions.items():
                print(f"  🔹 {division}")
                sorted_teams = sorted(div_teams, key=sort_key, reverse=True)
                for t in sorted_teams:
                    rec = self.records[t.name]
                    print(f"    {t.name:15} | {rec['W']:3d} - {rec['L']:3d} | Runs: {rec['R']:4d} | RA: {rec['RA']:4d}")




if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    data_dir = os.path.normpath(data_dir)

    teams = []
    teams_metadata = {}

    # load teams.csv metadata (if present) and normalize keys to match filenames like "red_sox"
    teams_csv = os.path.join(data_dir, "teams.csv")
    if os.path.exists(teams_csv):
        df = pd.read_csv(teams_csv, dtype=str).fillna("")
        for _, row in df.iterrows():
            key = row['team'].strip().lower().replace(" ", "_")
            teams_metadata[key] = {
                "league": row.get("league", "").strip().upper(),
                "division": row.get("division", "").strip().title(),
                "ballpark": row.get("ballpark", "").strip()
            }

    # load each team CSV (skip teams.csv)
    for fname in os.listdir(data_dir):
        if not fname.endswith(".csv") or fname == "teams.csv":
            continue
        team_key = os.path.splitext(fname)[0].lower()         
        display_name = team_key.replace("_", " ").title()         
        csv_path = os.path.join(data_dir, fname)

        meta = teams_metadata.get(team_key, {})
        league = meta.get("league", "AL").upper()
        division = meta.get("division", "Unknown").title()
        ballpark = meta.get("ballpark", "Unknown Park")

        team = Team(name=display_name, csv_path=csv_path,league=league, division=division, ballpark=ballpark)
        teams.append(team)


    season = Season(teams)
    season.simulate_season()
    season.print_standings()
