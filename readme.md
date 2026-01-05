# Rock–Paper–Scissors–Plus – AI Game Referee

## Overview
This project implements a stateful AI game referee for the Rock–Paper–Scissors–Plus game.
The referee manages the full game flow, validates user input, enforces rules, tracks
state across turns, and determines round outcomes in a deterministic manner.

The game runs in a simple conversational loop using a command-line interface (CLI),
with no external dependencies or services.

---

## State Model
All mutable game state is encapsulated in a dedicated `GameState` dataclass.
It stores:
- Current round number
- User and bot scores
- Bomb usage flags for both players
- A flag indicating whether the game is still active

The state is kept explicit and flat to avoid hidden dependencies and to make the
agent’s behavior easy to reason about, test, and debug across turns.

---

## Agent and Tool Design
The `GameReferee` class acts as the central agent orchestrator. It controls the
conversation flow, prompts the user, and renders round-by-round feedback.

Validation and state mutation are handled through explicit tool-style helper
functions:
- `check_move` validates and interprets user input
- `apply_round` resolves the round outcome and updates game state

These tools return structured outputs (Python dictionaries), which aligns with
Google ADK principles of separating agent orchestration from tool-based validation
and state mutation.

Core game rules are isolated in the `GameLogic` class, while bot decision-making is
handled independently in `BotStrategy`, ensuring clear separation of responsibilities.

---

## Tradeoffs
The game logic is fully deterministic and rule-based, so no LLM-based reasoning or
external APIs are used. This avoids unnecessary complexity and ensures predictable,
correct behavior for a well-defined problem space.

While an LLM could be used to generate richer natural-language explanations, it would
not improve correctness for this use case. The current design prioritizes clarity,
testability, and correctness over generative behavior.

---

## Improvements with More Time
With additional time, the following enhancements could be explored:
- Adding an optional LLM layer purely for natural-language explanations
- Making the number of rounds configurable
- Adding logging of state transitions for easier debugging and analysis
- Supporting alternative game variants without changing core logic

---

## How to Run
### Prerequisites
- Python 3.8 or higher

### Run the game
```bash
python rps_game.py
