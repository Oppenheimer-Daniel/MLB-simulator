import csv
import random
# Absolute import for running from main.py
from models.player import Player

class Team:
    def __init__(self, name, city="Unknown City", abbreviation="XXX", csv_path=None, league="Unknown League", division="Unknown Division", ballpark="Unknown Park"):
        self.name = name
        self.city = city
        self.abbreviation = abbreviation
        self.csv_path = csv_path
        self.league = league
        self.division = division
        self.ballpark = ballpark

        self.players = []
        self.lineup_index = 0
        
        # Only try to load if a path was actually provided
        if csv_path:
            self.load_players(csv_path)

    def load_players(self, csv_path):
        try:
            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    player = Player(
                        name=row["player"],
                        contact=float(row["contact"]),
                        power=float(row["power"]),
                        speed=float(row["speed"]),
                        fielding=float(row["fielding"]),
                        discipline=float(row["discipline"])
                    )
                    self.players.append(player)
        except FileNotFoundError:
            print(f"⚠️ Warning: Could not find player file at {csv_path}")
        except Exception as e:
            print(f"⚠️ Error loading players for {self.name}: {e}")

    def get_next_batter(self):
        if not self.players:
            raise ValueError(f"No players found for {self.name}")
        batter = self.players[self.lineup_index]
        self.lineup_index = (self.lineup_index + 1) % len(self.players)
        return batter

    def record_team_stats(self):
        """Aggregate stats from players for summary output."""
        self.stats = {"R": 0, "H": 0, "BB": 0, "SO": 0}
        for p in self.players:
            self.stats["H"] += p.stats["H"]
            self.stats["BB"] += p.stats["BB"]
            if "SO" in p.stats:
                self.stats["SO"] += p.stats["SO"]

    def print_lineup(self):
        """Display batting order."""
        print(f"\n{self.name} Lineup:")
        if not self.players:
            print("  (Empty Roster)")
            return
        for i, p in enumerate(self.players, start=1):
            print(f"{i}. {p.name} (Contact {p.contact}, Power {p.power}, Disc {p.discipline})")

    def team_summary(self):
        """Print current team stats summary."""
        self.record_team_stats()
        print(f"\n{self.name} Summary:")
        print(f"Hits: {self.stats['H']} | Walks: {self.stats['BB']} | Strikeouts: {self.stats['SO']}")