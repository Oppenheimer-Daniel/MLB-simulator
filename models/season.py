import os
from team import Team
from game import Game
import random
import pandas as pd

class Season:
    def __init__(self, teams, games_per_matchup=3):
        self.teams = teams
        self.games_per_matchup = games_per_matchup
        self.records = {team.name: {"W": 0, "L": 0, "R": 0, "RA": 0} for team in teams}

    def play_game(self, team1, team2):
        game = Game(team1, team2)
        winner, score_away, score_home = game.simulate_game()

        # Update runs for/against
        self.records[team1.name]["R"] += score_away
        self.records[team1.name]["RA"] += score_home
        self.records[team2.name]["R"] += score_home
        self.records[team2.name]["RA"] += score_away

        # Update W/L
        if winner == team1.name:
            self.records[team1.name]["W"] += 1
            self.records[team2.name]["L"] += 1
        else:
            self.records[team2.name]["W"] += 1
            self.records[team1.name]["L"] += 1

    def simulate_season(self):
        for i, team1 in enumerate(self.teams):
            for j, team2 in enumerate(self.teams):
                if i >= j:  # avoid duplicates
                    continue
                print(f"\n🏟️  {team1.name} vs {team2.name}")
                for g in range(self.games_per_matchup):
                    print(f"Game {g+1}:")
                    self.play_game(team1, team2)

    def print_standings(self):
        print("\n=== FINAL STANDINGS ===")
        sorted_teams = sorted(
            self.records.items(),
            key=lambda t: (t[1]["W"], -t[1]["RA"]),
            reverse=True
        )
        for name, rec in sorted_teams:
            print(f"{name:15} | {rec['W']:3d}-{rec['L']:3d} | Runs: {rec['R']:4d} | RA: {rec['RA']:4d}")


# ---------------------------
# 🧩 MAIN EXECUTION
# ---------------------------
if __name__ == "__main__":
    data_dir = "data"
    teams = []

    # Load team metadata (league, division, ballpark)
    teams_metadata_path = os.path.join(data_dir, "teams.csv")
    teams_metadata = {}
    if os.path.exists(teams_metadata_path):
        df = pd.read_csv(teams_metadata_path)
        for _, row in df.iterrows():
            teams_metadata[row['team_name'].lower()] = {
                'ballpark': row['ballpark'],
                'league': row['league'],
                'division': row['division']
            }

    # Load all player CSVs (skip teams.csv)
    for file in os.listdir(data_dir):
        if not file.endswith(".csv") or file == "teams.csv":
            continue

        team_name = file.replace(".csv", "").capitalize()
        csv_path = os.path.join(data_dir, file)

        # Add metadata if available
        meta = teams_metadata.get(team_name.lower(), {})
        team = Team(
            name=team_name,
            csv_path=csv_path,
            ballpark=meta.get('ballpark', 'Unknown Park'),
            league=meta.get('league', 'Unknown League'),
            division=meta.get('division', 'Unknown Division')
        )

        teams.append(team)

    print(f"✅ Loaded {len(teams)} teams into the season.")

    # Simulate a full season
    season = Season(teams, games_per_matchup=3)
    season.simulate_season()
    season.print_standings()

