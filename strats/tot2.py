import os
from main import RuleParameters


class Strategy:
    def __init__(self, rule_parameters: RuleParameters):
        self.name = os.path.splitext(os.path.basename(__file__))[0]
        self.description = "team of three (2): bid evenly on every third round starting on round 2"

        self.divisor = 3
        self.remainder = 2
        self.bid_time_per_round = rule_parameters.total_time / (rule_parameters.num_rounds // self.divisor)

    def bid(self, round_number: int, history: list, time_left: float) -> float:
        if round_number % self.divisor == self.remainder:
            return self.bid_time_per_round
        else:
            return 0.0