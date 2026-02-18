import csv
import os
from models.team import Team
from models.player import Player

def load_teams_and_players(teams_file, data_dir="data"):
    teams_list = []
    
    if not os.path.exists(teams_file):
        print(f"Error: Could not find {teams_file}")
        return []

    with open(teams_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            team_name = row.get("team")
            
            # Convert "White Sox" -> "white_sox.csv"
            # Convert "Astros" -> "astros.csv"
            file_name = team_name.lower().replace(" ", "_") + ".csv"
            player_file_path = os.path.join(data_dir, file_name)
            
            # Create the Team object
            # We pass player_file_path to csv_path so the Team class 
            # can load its own players via self.load_players()
            team = Team(
                name=team_name,
                city=row.get("city", "Unknown"),
                abbreviation=row.get("abbreviation", "XXX"),
                csv_path=player_file_path,
                league=row.get("league"),
                division=row.get("division"),
                ballpark=row.get("ballpark")
            )
            
            teams_list.append(team)
            
    return teams_list