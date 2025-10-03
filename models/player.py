import random
import math as Math

class Player:
    def __init__(self, name, contact, power, discipline):
        self.name = name
        self.contact = contact 
        self.power = power 
        self.discipline = discipline
        self.stats = {"AB": 0, "H": 0, "1B": 0, "2B": 0, "3B": 0, "HR": 0, "BB": 0, "SO": 0}

    def get_hit_probability(self):
        """
        Map contact to chance of getting a hit.
        50 contact = 24% hit rate
        100 contact = 32% hit rate
        Linear scale between those.
        """
        base = 0.24
        slope = (0.32 - base) / 50 
        if self.contact < 50:
            return max(0.10, base - (50 - self.contact) * slope)
        else:
            return base + (self.contact - 50) * slope
        
    def get_strike_out_probability(self):
        """
        Strikeout probability based on both Contact and Discipline.
        Average of contact and discipline determines strikeout rate:
        - Avg = 50  → 21% strikeout rate
        - Avg = 100 → 15% strikeout rate
        - Avg = 25  → 27% strikeout rate
        """
        avg_skill = (self.contact + self.discipline) / 2
        base = 0.21  # 21% at average skill (50)
        slope = (0.15 - base) / 50  # decreases 0.06 from 50→100

        if avg_skill < 50:
            # below-average skill → *more* strikeouts
            return base + (50 - avg_skill) * (-slope)  # reverse slope direction
        else:
            # above-average skill → fewer strikeouts
            return base + (avg_skill - 50) * slope

        
    def get_walk_probability(self):
        """
        Map contact to chance of getting a walk.
        50 discpline = 9% walk rate
        100 disciple = 22% walk rate
        Linear scale between those.
        """
        base = 0.09
        slope = (0.22 - base) / 50 
        if self.discipline < 50:
            return max(0.10, base - (50 - self.discipline) * slope)
        else:
            return base + (self.discipline - 50) * slope

    def get_hit_distribution(self):
        """
        Based on power, distribute hit types.
        """
        # Home run %
        hr_prob = 0.16 + (self.power / 100) * (0.30 - 0.16)

        # Doubles %
        double_prob = 0.20 + (self.power / 100) * (0.25 - 0.20)

        # Triples % (constant for now, change to scale with speed later)
        triple_prob = 0.02

        # Singles = leftover
        single_prob = 1 - (hr_prob + double_prob + triple_prob)

        return {
            "1B": single_prob,
            "2B": double_prob,
            "3B": triple_prob,
            "HR": hr_prob
        }

    def simulate_at_bat(self):
        self.stats["AB"] += 1
        if random.random() < self.get_hit_probability():
            # Decide hit type
            self.stats["H"] += 1
            distribution = self.get_hit_distribution()
            outcome = random.choices(
                population=list(distribution.keys()),
                weights=list(distribution.values())
            )[0]
            self.stats[outcome] += 1
            return f"{self.name} got a {outcome}"
        elif random.random() < self.get_walk_probability():
            self.stats["BB"] += 1
            self.stats["AB"] -= 1  # Walks don't count as at-bats
            return f"{self.name} walked"
        else:
            if random.random() < self.get_strike_out_probability():
                self.stats["SO"] += 1
                return f"{self.name} struck out"
            return f"{self.name} made an out"

    def print_stats(self):
        avg = self.stats["H"] / self.stats["AB"] if self.stats["AB"] > 0 else 0
        obp = (self.stats["H"] + self.stats["BB"]) / (self.stats["AB"] + self.stats["BB"]) if (self.stats["AB"] + self.stats["BB"]) > 0 else 0
        slg = (self.stats["1B"] + 2 * self.stats["2B"] + 3 * self.stats["3B"] + 4 * self.stats["HR"]) / self.stats["AB"] if self.stats["AB"] > 0 else 0
        ops = obp + slg
        print(f"{self.name} Stats:")
        print(f"AB: {self.stats['AB']}, H: {self.stats['H']}, AVG: {avg:.3f}, OBP: {obp:.3f}, SLG: {slg:.3f}, OPS: {ops:.3f}")
        print(f"1B: {self.stats['1B']}, 2B: {self.stats['2B']}, 3B: {self.stats['3B']}, HR: {self.stats['HR']}, BB: {self.stats['BB']}, SO: {self.stats['SO']}")
