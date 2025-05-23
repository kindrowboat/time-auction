import os
from main import RuleParameters


class Strategy:
    def __init__(self, rule_parameters: RuleParameters):
        self.name = os.path.splitext(os.path.basename(__file__))[0]
        self.description = "Exponential Decay 15%: bid high at the start and decay 15% each round"

    def bid(self, round_number: int, history: list, time_left: float) -> float:
        return 93.62*0.85**(round_number-1)
 