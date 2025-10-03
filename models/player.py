import random

class Player:
    def __init__(self, name, contact, power):
        self.name = name
        self.contact = contact 
        self.power = power 
        self.stats = {"AB": 0, "H": 0, "1B": 0, "2B": 0, "3B": 0, "HR": 0}

    def get_hit_probability(self):
        """
        Map contact to chance of getting a hit.
        50 contact = 24% hit rate
        100 contact = 32% hit rate
        Linear scale between those.
        """
        base = 0.24
        slope = (0.32 - 0.24) / 50 
        if self.contact < 50:
            return max(0.10, base - (50 - self.contact) * slope)
        else:
            return base + (self.contact - 50) * slope

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
        hit_chance = self.get_hit_probability()
        if random.random() < hit_chance:
            # Decide hit type
            self.stats["H"] += 1
            distribution = self.get_hit_distribution()
            outcome = random.choices(
                population=list(distribution.keys()),
                weights=list(distribution.values())
            )[0]
            self.stats[outcome] += 1
            return f"{self.name} got a {outcome}"
        else:
            return f"{self.name} made an out"

    def print_stats(self):
        avg = self.stats["H"] / self.stats["AB"] if self.stats["AB"] > 0 else 0
        print(f"{self.name} Stats:")
        print(f"AB: {self.stats['AB']}, H: {self.stats['H']}, AVG: {avg:.3f}")
        print(f"1B: {self.stats['1B']}, 2B: {self.stats['2B']}, 3B: {self.stats['3B']}, HR: {self.stats['HR']}")
