# models/season.py
import os
import random
import pandas as pd
from team import Team
from game import Game
from schedule import Schedule


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
