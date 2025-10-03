# team.py
from player import Player
import itertools

class Team:
    def __init__(self, name, players):
        """
        name: str (team name)
        players: list[Player] (lineup order)
        """
        self.name = name
        self.players = players
        self.lineup = itertools.cycle(players)  # cycles through batters automatically
        self.stats = {
            "R": 0,
            "H": 0,
            "HR": 0,
            "BB": 0,
            "SO": 0
        }

    def next_batter(self):
        return next(self.lineup)

    def record_event(self, batter):
        """Update team totals after each AB based on batter stats."""
        self.stats["H"] = sum(p.hits for p in self.players)
        self.stats["HR"] = sum(p.hr for p in self.players)
        self.stats["BB"] = sum(p.bb for p in self.players)
        self.stats["SO"] = sum(p.so for p in self.players)

    def print_lineup(self):
        print(f"--- {self.name} Lineup ---")
        for p in self.players:
            print(f"{p.name} | AVG: {p.avg():.3f} | HR: {p.hr} | BB: {p.bb} | SO: {p.so}")
