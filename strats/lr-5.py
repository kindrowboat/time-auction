import os
from main import RuleParameters


class Strategy:
    def __init__(self, rule_parameters: RuleParameters):
        self.name = os.path.splitext(os.path.basename(__file__))[0]
        self.description = "Bid all remaining time evenly in the last 5 rounds"

        self.last_rounds = 5
        self.start_bidding_round = rule_parameters.num_rounds - self.last_rounds
        self.time_per_round = rule_parameters.total_time / self.last_rounds

    def bid(self, round_number: int, history: list, time_left: float) -> float:
        if round_number <= self.start_bidding_round:
            return 0.0
        else:
            return self.time_per_round