# schedule.py

import itertools

class Schedule:
    def __init__(self, teams):
        self.teams = teams
        self.games = []  # list of (away, home)

    def generate(self):
        """
        Generates a full MLB-style schedule:
        - Division opponents: 14 games each
        - Same-league, non-division: 6 games each
        - Interleague: 3 games each (20 opponents)
        Total: 162 games per team
        """
        self.games = []

        # Group teams by league/division
        leagues = {}
        for team in self.teams:
            leagues.setdefault(team.league, {}).setdefault(team.division, []).append(team)

        # --- 1) Division games (14 per matchup)
        for league in leagues.values():
            for division in league.values():
                for team1, team2 in itertools.combinations(division, 2):
                    self._add_series(team1, team2, 14)

        # --- 2) Same-league, non-division (6 per matchup)
        for league in leagues.values():
            all_teams = [t for div in league.values() for t in div]
            for team1, team2 in itertools.combinations(all_teams, 2):
                if team1.division == team2.division:
                    continue
                self._add_series(team1, team2, 6)

        # --- 3) Interleague (3 games vs 20 teams)
        league_names = list(leagues.keys())
        if len(league_names) == 2:
            l1 = [t for div in leagues[league_names[0]].values() for t in div]
            l2 = [t for div in leagues[league_names[1]].values() for t in div]

            for team1 in l1:
                for team2 in l2:
                    self._add_series(team1, team2, 3)

        return self.games

    def _add_series(self, team1, team2, games):
        """
        Split home/away as evenly as possible.
        """
        for i in range(games):
            if i % 2 == 0:
                self.games.append((team1, team2))  # team1 away
            else:
                self.games.append((team2, team1))  # team2 away
