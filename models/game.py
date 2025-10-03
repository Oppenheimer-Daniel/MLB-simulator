# game.py
from team import Team

class Inning:
    def __init__(self, batting_team):
        self.team = batting_team
        self.outs = 0
        self.bases = [None, None, None]  # 1B, 2B, 3B
        self.runs = 0

    def advance_runners(self, batter, bases_to_advance):
        """
        Move all runners forward by bases_to_advance.
        Count runs if they score.
        """
        # move from 3rd → home first
        for i in reversed(range(3)):
            if self.bases[i] is not None:
                if i + bases_to_advance >= 3:
                    self.runs += 1
                    self.team.stats["R"] += 1
                else:
                    self.bases[i + bases_to_advance] = self.bases[i]
                self.bases[i] = None

        # put batter on base (if not HR)
        if bases_to_advance < 4:
            self.bases[bases_to_advance - 1] = batter

    def play_half_inning(self):
        """
        Simulate until 3 outs.
        Returns runs scored.
        """
        while self.outs < 3:
            batter = self.team.next_batter()
            result = batter.simulate_at_bat()

            if result == "1B":
                self.advance_runners(batter, 1)
            elif result == "2B":
                self.advance_runners(batter, 2)
            elif result == "3B":
                self.advance_runners(batter, 3)
            elif result == "HR":
                self.advance_runners(batter, 4)
                self.runs += 1
                self.team.stats["R"] += 1
            elif result == "BB":
                # walk → force advance if bases loaded
                if self.bases[0] and self.bases[1] and self.bases[2]:
                    self.runs += 1
                    self.team.stats["R"] += 1
                # shift runners if needed
                elif self.bases[0] and self.bases[1]:
                    self.bases[2] = self.bases[1]
                    self.bases[1] = self.bases[0]
                    self.bases[0] = batter
                elif self.bases[0]:
                    self.bases[1] = self.bases[0]
                    self.bases[0] = batter
                else:
                    self.bases[0] = batter
            elif result == "OUT":
                self.outs += 1

            self.team.record_event(batter)

        return self.runs
