import csv
from models.team import Team
from models.player import Player

def load_teams_and_players(teams_file, players_file):
    # Step 1: Load teams
    teams = {}
    with open(teams_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            team = Team(
                name=row["team"],
                city=row.get("city"),
                abbreviation=row.get("abbreviation"),
                division=row.get("division"),
                league=row.get("league"),
                ballpark=row.get("ballpark")
            )
            teams[team.name] = team

    # Step 2: Load players and add to correct team
    with open(players_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            player = Player(
                name=row["player"],
                contact=int(row["contact"]),
                power=int(row["power"]),
                speed=int(row["speed"]),
                fielding=int(row["fielding"]),
                pitching=int(row["pitching"])
            )
            team_name = row["team"]
            if team_name in teams:
                teams[team_name].add_player(player)
            else:
                print(f"Warning: team {team_name} not found in teams.csv")

    return list(teams.values())
