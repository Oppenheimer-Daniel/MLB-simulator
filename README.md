# ⚾ MLB Simulation Engine: Franchise Edition

A deep-logic Python simulation engine that models Major League Baseball through an interactive command-line interface. 

![Python](https://img.shields.io/badge/python-3.11-blue)
![Status](https://img.shields.io/badge/status-Alpha--Playable-green)

## 🎯 Project Overview
This isn't just a statistical calculator; it's a playable Franchise Mode. The engine simulates plate appearances using linear weights for contact, power, and discipline, while a custom scheduler manages the complex 162-game MLB matrix (Divisional, League, and Interleague play).

## 🕹️ Current Features
- **Interactive Manager Menu:** Choose your team and lead them through a full season.
- **Dynamic 162-Game Scheduler:** Generates a realistic MLB schedule including home/away splits.
- **Advanced Simulation Logic:** - Real-time base-running state (1st, 2nd, 3rd base tracking).
  - Walk-off logic for bottom-of-the-9th scenarios.
  - Performance-based hit distribution (Power attribute scales HR/2B probability).
- **Relational Data Loading:** Automatically maps team metadata to individual player rosters via CSV.

## 🗺️ Roadmap
- [x] Core Engine: Plate appearances, walks, and HR logic.
- [x] Franchise Infrastructure: Interactive menus and 162-game scheduling.
- [ ] Box Scores: Post-game summaries showing individual player performance.
- [ ] Lineup Management: Active UI to swap players in the batting order.
- [ ] Pitching 2.0: Integrating pitcher-specific attributes (Velocity/Control) into the hit probability.
- [ ] Save System: Exporting season progress to JSON/SQLite.