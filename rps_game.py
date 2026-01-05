from dataclasses import dataclass
from typing import Optional, Dict
import random

# Holds all mutable game state
@dataclass
class GameState:
    round_num: int = 1
    user_score: int = 0
    bot_score: int = 0
    user_used_bomb: bool = False
    bot_used_bomb: bool = False
    is_active: bool = True

class GameLogic:
    allowed_moves = {"rock", "paper", "scissors", "bomb"}

    beats_map = {
        "rock": "scissors",
        "paper": "rock",
        "scissors": "paper",
    }

    @staticmethod
    def clean_move(raw_input: str) -> Optional[str]:
        if not raw_input:
            return None

        text = raw_input.strip().lower()
        shortcuts = {
            "r": "rock",
            "p": "paper",
            "s": "scissors",
            "b": "bomb",
            "stone": "rock",
        }

        move = shortcuts.get(text, text)
        return move if move in GameLogic.allowed_moves else None

    @staticmethod
    def pick_winner(user_move: str, bot_move: str) -> str:
        if user_move == bot_move:
            return "draw"
        if user_move == "bomb":
            return "draw" if bot_move == "bomb" else "user"
        if bot_move == "bomb":
            return "bot"
        return "user" if GameLogic.beats_map[user_move] == bot_move else "bot"
# Tool-style helpers for validation and state updates
class GameTools:

    @staticmethod
    def check_move(state: GameState, user_input: str) -> Dict:
        move = GameLogic.clean_move(user_input)

        if move is None:
            return {"ok": False, "error": "Invalid move"}
        if move == "bomb" and state.user_used_bomb:
            return {"ok": False, "error": "You already used your bomb"}

        return {"ok": True, "move": move}

    @staticmethod
    def apply_round(state: GameState, user_move: str, bot_move: str) -> Dict:
        winner = GameLogic.pick_winner(user_move, bot_move)

        if winner == "user":
            state.user_score += 1
        elif winner == "bot":
            state.bot_score += 1

        if user_move == "bomb":
            state.user_used_bomb = True
        if bot_move == "bomb":
            state.bot_used_bomb = True

        state.round_num += 1
        if state.round_num > 3:
            state.is_active = False

        return {
            "winner": winner,
            "user_move": user_move,
            "bot_move": bot_move,
            "scores": (state.user_score, state.bot_score),
            "game_over": not state.is_active,
        }
class BotStrategy:
    # Simple probabilistic bot behavior
    @staticmethod
    def decide(state: GameState) -> str:
        if state.round_num == 3 and not state.bot_used_bomb:
            if state.bot_score < state.user_score:
                return "bomb"

        options = ["rock", "paper", "scissors"]
        if not state.bot_used_bomb and random.random() < 0.2:
            options.append("bomb")

        return random.choice(options)
class GameReferee:
    # Main controller coordinating the game flow
    RULES_TEXT = (
        "Rock–Paper–Scissors–Plus\n"
        "• Best of 3 rounds\n"
        "• Moves: rock, paper, scissors, bomb\n"
        "• Bomb beats everything (once per game)\n"
        "• Invalid input wastes the round\n"
    )
    def __init__(self):
        self.state = GameState()

    def start_game(self) -> str:
        return f"{self.RULES_TEXT}\nRound 1 — your move?"

    def handle_input(self, user_input: str) -> str:
        if not self.state.is_active:
            return "Game already finished."

        check = GameTools.check_move(self.state, user_input)
        if not check["ok"]:
            self.state.round_num += 1
            if self.state.round_num > 3:
                self.state.is_active = False
                return self._final_summary()
            return f"{check['error']}. Round wasted.\nNext move?"

        user_move = check["move"]
        bot_move = BotStrategy.decide(self.state)

        result = GameTools.apply_round(self.state, user_move, bot_move)
        return self._render_round(result)

    def _render_round(self, result: Dict) -> str:
        text = (
            f"Round {self.state.round_num - 1} Result:\n"
            f"You played: {result['user_move']}\n"
            f"Bot played: {result['bot_move']}\n"
            f"Winner: {result['winner']}\n"
            f"Score: You {result['scores'][0]} - {result['scores'][1]} Bot"
        )

        return text + ("\n" + self._final_summary() if result["game_over"] else "\nNext move?")
    def _final_summary(self) -> str:
        if self.state.user_score > self.state.bot_score:
            outcome = "You win the game."
        elif self.state.bot_score > self.state.user_score:
            outcome = "Bot wins the game."
        else:
            outcome = "Game ends in a draw."

        return (
            "\n--- GAME OVER ---\n"
            f"Final Score: You {self.state.user_score} - {self.state.bot_score} Bot\n"
            f"{outcome}"
        )
def main():
    referee = GameReferee()
    print(referee.start_game())

    while referee.state.is_active:
        user_input = input("> ").strip()

        if user_input.lower() in {"quit", "exit"}:
            print("Game exited.")
            break

        print(referee.handle_input(user_input))


if __name__ == "__main__":
    main()
