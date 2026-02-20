from utils.data_loader import load_teams_and_players
from models.game import Game
from models.season import Season

def manage_lineup(team):
    print(f"\n--- Manage Lineup: {team.name} ---")
    # Placeholder for the swap logic
    print("Feature coming soon: Implement later.")

def show_standings(season):
    season.print_standings()

def play_franchise():
    teams = load_teams_and_players("data/teams.csv")
    user_team = teams[0] # Simplified selection
    
    season = Season(teams)
    # 2. User selects their team
    print("Welcome to Franchise Mode!")
    from models.schedule import Schedule
    scheduler = Schedule(teams)
    full_schedule = scheduler.generate() # Returns a list of (away, home) tuples
    
    # 3. Track where we are in the season
    current_game_index = 0

    # 4. Interactive Game Loop
    while True:
        print(f"\n{'='*30}")
        print(f"   {user_team.name} MANAGER MENU")
        print(f"{'='*30}")
        print("1. Play Next Game")
        print("2. Manage Lineup (Implement later)")
        print("3. View League Standings")
        print("4. Exit Game")
        
        choice = input("\nWhat would you like to do? ")

        if choice == "1":
            # 1. Find the next game in the schedule that involves the user_team
            next_game = None
            for i in range(current_game_index, len(full_schedule)):
                away, home = full_schedule[i]
                if away == user_team or home == user_team:
                    next_game = (away, home)
                    # Update index to the next game AFTER this one
                    current_game_index = i + 1
                    break
            
            if next_game:
                away, home = next_game
                print(f"\nNext Matchup: {away.name} @ {home.name}")
                
                # 2. Use your existing Season logic to play the single game
                game = season.play_game(home, away)
                game.display_box_score()
            else:
                print("\n🏁 The season is over! No more games in the schedule.")
            
        elif choice == "2":
            manage_lineup(user_team)
            
        elif choice == "3":
            show_standings(season)
            
        elif choice == "4":
            print("Saving (Implement later) and Exiting...")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    play_franchise()