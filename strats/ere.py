import os
from main import RuleParameters


class Strategy:
    def __init__(self, rule_parameters: RuleParameters):
        self.name = os.path.splitext(os.path.basename(__file__))[0]
        self.description = "Every Round Even: bid evenly in each round"

        self.bid_per_round = rule_parameters.total_time / rule_parameters.num_rounds

    def bid(self, round_number: int, history: list, time_left: float) -> float:
        return self.bid_per_round