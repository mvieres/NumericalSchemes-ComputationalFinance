from Market.EuropeanOptions import EuropeanOptions


class OptionWrapper:

    def __init__(self, exercisetype: str, optiontype: str, strike: float):
        self.exercisetype = exercisetype
        self.optiontype = optiontype
        self.strike = strike

        pass

# TODO: add logic that returns the evaluated option payoff.