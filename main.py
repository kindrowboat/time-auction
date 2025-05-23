#!/usr/bin/env python3

import argparse
import importlib
from pathlib import Path

class RuleParameters:
    def __init__(self, total_time: int, num_rounds: int):
        self._total_time = total_time
        self._num_rounds = num_rounds

    @property
    def total_time(self):
        return self._total_time

    @property
    def num_rounds(self):
        return self._num_rounds

RULE_PARAMETERS = RuleParameters(600, 19)

class PlayerWrapper:
    def __init__(self, module_name: str, rule_parameters: RuleParameters = RULE_PARAMETERS):
        module = importlib.import_module(f"strats.{module_name}")
        self.strategy = module.Strategy(rule_parameters)
        self.name = module_name
        self.time_left = rule_parameters.total_time;
        self.wins = 0

    def bid(self, round_number, history):
        if self.time_left <= 0:
            return 0.0
        bid = min(self.strategy.bid(round_number, history, self.time_left), self.time_left)
        return max(0.0, bid)

def run_game(player_modules):
    players = [PlayerWrapper(name) for name in player_modules]
    history = []

    for round_num in range(1, RULE_PARAMETERS.num_rounds + 1):
        bids = []
        for p in players:
            bid = p.bid(round_num, history)
            bids.append((p, bid))

        bids.sort(key=lambda x: (-x[1], -x[0].time_left))
        winner = None
        if len(bids) > 1 and bids[0][1] == bids[1][1]:
            print(f"Round {round_num}: Tie — No winner")
        else:
            winner = bids[0][0]
            winner.wins += 1
            print(f"Round {round_num} winner: {winner.name} with bid {bids[0][1]:.1f}s")

        for p, bid in bids:
            p.time_left -= bid
            print(f"  {p.name:6} {bid:6.1f} bid {p.wins:2} wins {p.time_left:7.1f}s left")

        history.append([(p.name, bid) for p, bid in bids])

    players.sort(key=lambda p: (-p.wins, -p.time_left))

    print("\nRESULTS")
    for p in players:
        print(f"  {p.name:6} {p.wins:2} wins {p.time_left:6.1f}s left")

def list_strategies():
    strats_dir = Path(__file__).parent / "strats"
    strategies = []

    for strat_file in strats_dir.glob("*.py"):
        if strat_file.name == "__init__.py":
            continue
        module_name = strat_file.stem
        module = importlib.import_module(f"strats.{module_name}")
        if hasattr(module, "Strategy"):
            strategy = module.Strategy(RULE_PARAMETERS)
            strategies.append((strategy.name, strategy.description))

    # Sort strategies alphabetically by name
    strategies.sort(key=lambda x: x[0])

    # Calculate dynamic padding based on the longest strategy name
    max_name_length = max(len(name) for name, _ in strategies)
    padding = max_name_length

    print("\nAvailable Strategies:")
    for name, description in strategies:
        print(f"  {name:{padding}} | {description}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", "--list", action="store_true", help="List available strategies and their descriptions"
    )
    parser.add_argument(
        "strategies", nargs="*", help="List of strategy module names from ./strats"
    )
    args = parser.parse_args()

    if args.list:
        list_strategies()
        return

    if not args.strategies:
        print("Error: No strategies specified. Use -l to list available strategies.")
        return

    run_game(args.strategies)


if __name__ == "__main__":
    main()
