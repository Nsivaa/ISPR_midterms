class BayesianNode:
    def __init__(self, name : str, prob: list = [0.5, 0.5]) -> None:
        # probabilities are ordered as [True, False]
        assert sum(prob) == 1
        self.name = name
        self.prob_table = prob

    def __str__(self) -> str:
        return f"Node: {self.name}, Probabilities: {self.prob_table}"