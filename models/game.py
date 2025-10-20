from team import Team
import random

class Game:
    def __init__(self, home_team: Team, away_team: Team):
        self.home = home_team
        self.away = away_team
        self.score = {"home": 0, "away": 0}
        self.inning = 1
        self.half = "top" 

    def play_half_inning(self, batting_team: Team):
        outs = 0
        bases = [False, False, False]
        runs = 0

        while outs < 3:
            batter = batting_team.get_next_batter()
            result = batter.simulate_at_bat()

            if "1B" in result:
                # Advance all runners one base
                if bases[2]:  # runner on 3rd scores
                    runs += 1
                    bases[2] = False
                if bases[1]:  # runner on 2nd moves to 3rd
                    bases[2] = True
                    bases[1] = False
                if bases[0]:  # runner on 1st moves to 2nd
                    bases[1] = True
                bases[0] = True  # batter on 1st

            elif "2B" in result:
                # Runners on 2nd or 3rd score
                if bases[2]:
                    runs += 1
                    bases[2] = False
                if bases[1]:
                    runs += 1
                    bases[1] = False
                if bases[0]:
                    bases[2] = True  # runner on 1st moves to 3rd
                    bases[0] = False
                bases[1] = True  # batter on 2nd

            elif "3B" in result:
                # Everyone scores
                runs += sum(bases)
                bases = [False, False, True]

            elif "HR" in result:
                # All runners + batter score
                runs += 1 + sum(bases)
                bases = [False, False, False]

            elif "walked" in result:
                # Force walk logic
                if all(bases):  # bases loaded
                    runs += 1  # runner on 3rd scores
                # Move runners one base if forced
                if bases[1] and bases[0]:
                    bases[2] = True
                if bases[0]:
                    bases[1] = True
                bases[0] = True

            elif "out" in result or "struck out" in result:
                outs += 1

        return runs


    def simulate_game(self):

        for inning in range(1, 10):
            self.inning = inning
            self.half = "top"
            away_runs = self.play_half_inning(self.away)
            self.score["away"] += away_runs
        
            if inning == 9 and self.score["home"] > self.score["away"]:
                break

            self.half = "bottom"
            home_runs = self.play_half_inning(self.home)
            self.score["home"] += home_runs

            # If bottom of the 9th (or later) ends with home team leading, end game.
            if inning == 9 and self.score["home"] > self.score["away"]:
                break


        print("\n✅ Final Score:")
        print(f"{self.away.name}: {self.score['away']} | {self.home.name}: {self.score['home']}")

        if self.score["away"] > self.score["home"]:
            winner = self.away.name
        elif self.score["home"] > self.score["away"]:
            winner = self.home.name
        else:
            winner = random.choice([self.away.name, self.home.name])

        return winner, self.score["away"], self.score["home"]



if __name__ == "__main__":
    home = Team("Astros", "data/astros.csv")
    away = Team("Yankees", "data/yankees.csv")

    game = Game(home, away)
    winner, away_score, home_score = game.simulate_game()

