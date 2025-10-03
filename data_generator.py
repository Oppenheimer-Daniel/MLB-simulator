import csv
from models.player import Player  

players = []

with open("data/astros.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Pull values from CSV
        name = row["player"]
        contact = int(row["contact"])   
        power = int(row["power"])       

        players.append(Player(name, contact, power))

# Simulate 100 at-bats per player
for p in players:
    for _ in range(100):
        p.simulate_at_bat()
    p.print_stats()
