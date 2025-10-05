import csv
from player import Player
import random

class Team:
    def __init__(self, name, csv_path):
        self.name = name
        self.players = []
        self.load_players(csv_path)
        self.lineup_index = 0
        self.stats = {"R": 0, "H": 0, "BB": 0, "SO": 0, "E": 0}

    def load_players(self, csv_path):
        """Load 9 players from the given CSV file."""
        with open(csv_path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Only add players with numeric attributes
                try:
                    player = Player(
                        row["player"],
                        int(row["contact"]),
                        int(row["power"]),
                        int(row["discipline"])
                    )
                    self.players.append(player)
                except (ValueError, KeyError):
                    continue

        # Ensure exactly 9 players
        if len(self.players) > 9:
            self.players = self.players[:9]

    def get_next_batter(self):
        """Return the next player in the lineup (loops back to 1 after 9)."""
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
        for i, p in enumerate(self.players, start=1):
            print(f"{i}. {p.name} (Contact {p.contact}, Power {p.power}, Disc {p.discipline})")

    def team_summary(self):
        """Print current team stats summary."""
        self.record_team_stats()
        print(f"\n{self.name} Summary:")
        print(f"Hits: {self.stats['H']} | Walks: {self.stats['BB']} | Strikeouts: {self.stats['SO']}")

# -------------------------------
# ✅ TEST BLOCK (only runs when executed directly)
# -------------------------------
if __name__ == "__main__":
    astros = Team("Astros", "data/astros.csv")
    astros.print_lineup()

    # Simulate one full lineup cycle
    for _ in range(9):
        batter = astros.get_next_batter()
        print(batter.simulate_at_bat())

    astros.team_summary()