from models.team import Team
import random

class Game:
    def __init__(self, home_team: Team, away_team: Team):
        self.home = home_team
        self.away = away_team
        self.score = {"home": 0, "away": 0}
        self.inning = 1
        self.half = "top" 
        for p in self.home.players + self.away.players:
            p.reset_game_stats()

    def play_half_inning(self, batting_team: Team):
        outs = 0
        # bases[0]=1st, [1]=2nd, [2]=3rd
        bases = [False, False, False]
        runs = 0

        while outs < 3:
            batter = batting_team.get_next_batter()
            result = batter.simulate_at_bat()

            batter.game_stats["AB"] += 1
            if "walked" in result:
                batter.game_stats["BB"] += 1
                batter.game_stats["AB"] -= 1
                if bases[0] and bases[1] and bases[2]:
                    runs += 1
                    batter.game_stats["RBI"] += 1
                if bases[0] and bases[1]:
                    bases[2] = True
                if bases[0]:
                    bases[1] = True
                bases[0] = True

            elif "1B" in result:
                batter.game_stats["H"] += 1
                if bases[2]:
                    runs += 1
                    batter.game_stats["RBI"] += 1
                bases[2] = bases[1]
                bases[1] = bases[0]
                bases[0] = True

            elif "2B" in result:
                batter.game_stats["H"] += 1
                if bases[2]: 
                    runs += 1
                    batter.game_stats["RBI"] += 1
                if bases[1]: 
                    runs += 1
                    batter.game_stats["RBI"] += 1
                bases[2] = bases[0]
                bases[1] = True
                bases[0] = False

            elif "3B" in result:
                batter.game_stats["H"] += 1
                runs += sum(bases)
                batter.game_stats["RBI"] += sum(bases)
                bases = [False, False, True]

            elif "HR" in result:
                batter.game_stats["H"] += 1
                runs += 1 + sum(bases)
                batter.game_stats["RBI"] += 1 + sum(bases)
                bases = [False, False, False]

            elif "out" in result:
                outs += 1
            
            # Walk-off check: if it's the bottom of the 9th+ and home team leads
            if self.half == "bottom" and self.inning >= 9:
                if (self.score["home"] + runs) > self.score["away"]:
                    return runs

        return runs

    def simulate_game(self):
        self.inning = 1
        while True:
            # Top of the inning
            self.half = "top"
            self.score["away"] += self.play_half_inning(self.away)

            # Middle of the 9th: Home team leading check
            if self.inning == 9 and self.score["home"] > self.score["away"]:
                break

            # Bottom of the inning
            self.half = "bottom"
            self.score["home"] += self.play_half_inning(self.home)

            # End of inning checks
            if self.inning >= 9 and self.score["home"] != self.score["away"]:
                break
            
            self.inning += 1

        return self.home.name if self.score["home"] > self.score["away"] else self.away.name, self.score["away"], self.score["home"]


    def display_box_score(self):
            print(f"\n{'='*40}")
            print(f"       FINAL SCORE: {self.away.name} {self.score['away']} - {self.home.name} {self.score['home']}")
            print(f"{'='*40}")
            
            for team in [self.away, self.home]:
                print(f"\n{team.name.upper()} BOX SCORE:")
                print(f"{'Player':<20} | {'AB':<3} | {'H':<3} | {'HR':<3} | {'BB':<3} | {'RBI':<3}")
                print("-" * 50)
                for p in team.players:
                    gs = p.game_stats
                    print(f"{p.name:<20} | {gs['AB']:<3} | {gs['H']:<3} | {gs['HR']:<3} | {gs['BB']:<3} | {gs['RBI']:<3}")