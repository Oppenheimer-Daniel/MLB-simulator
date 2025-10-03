from utils.data_loader import load_teams_and_players
from models.game import Game

if __name__ == "__main__":
    teams = load_teams_and_players("data/teams.csv", "data/players.csv")

    team_with_players = [t for t in teams if len(t.players) > 0]

    team1 = team_with_players[0]
    team2 = team_with_players[1]

    print(f"Simulating: {team1.name} vs {team2.name}")
    game = Game(team1, team2)
    game.play_game()


