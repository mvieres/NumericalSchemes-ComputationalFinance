from enum import Enum
from analysis.supported_payoffs import supported_payoffs  # TODO: This is temporary


class Payoff:

    def __init__(self, name: str, params):
        """

        @param name: string as input that describes the payoff -> has to be mapped
        @param exercise_type:
        @param params:
        """
        self.name = name

        try:
            self.name = PayoffName(name)
        except KeyError as e:
            raise ValueError(f"error occurred {e}")
        # Get the exercise type from classification Enum
        self.exercise_type = ExerciseType.PATH_INDEPENDENT if self.name.value in PayoffClassification.PATH_INDEPENDENT.value else ExerciseType.PATH_DEPENDENT
        self.params = params  # This is uncategorized at the moment
        pass

    def get_exercise_type(self):
        return self.exercise_type

    def eval(self, underlying_history) -> float:
        underlying = self.__process_underlying_history(underlying_history)  # Cutting of history if needed
        # Then we need to distinguish between the different payoffs as many have a different number of input parameters.
        if self.name.value in PayoffClassification.STRIKE_SPOT.value:
            strike = self.params.get("strike")
            self.__validate(strike)
            return supported_payoffs[self.name.value](underlying, strike)
        elif self.name.value in PayoffClassification.STRIKE_SPOT_BARRIER.value:
            strike = self.params.get("strike")
            barrier = self.params.get("barrier")
            self.__validate(strike)
            self.__validate(barrier)
            # Validate for correct underlying history (should be a series)
            assert not isinstance(underlying, float) and not isinstance(underlying, int), "Underlying history should be a series"
            return supported_payoffs[self.name.value](underlying, strike, barrier)
        else:
            raise ValueError("Payoff not implemented yet")

    def __process_underlying_history(self, underlying_history):
        if isinstance(underlying_history, float) or isinstance(underlying_history, int) or self.exercise_type == ExerciseType.PATH_DEPENDENT:
            return underlying_history
        elif self.exercise_type == ExerciseType.PATH_INDEPENDENT:
            return underlying_history[-1]
        else:
            raise ValueError("Process error during Payoff evaluation")

    @staticmethod
    def __validate(param):
        if param is None:
            raise KeyError('Option-parameter not found in dict!')


class PayoffName(Enum):

    CALL = "call"
    PUT = "put"
    LOOKBACK_MIN_CALL = "lookback_min_call"
    LOOKBACK_MAX_CALL = "lookback_max_call"
    LOOKBACK_MIN_PUT = "lookback_min_put"
    LOOKBACK_MAX_PUT = "lookback_max_put"
    BARRIER_CALL = "barrier_call"
    BARRIER_PUT = "barrier_put"
    ASIAN_CALL = "asian_call"
    ASIAN_PUT = "asian_put"


class ExerciseType(Enum):

    PATH_INDEPENDENT = "path_independent"
    PATH_DEPENDENT = "path_dependent"


class PayoffClassification(Enum):

    VANILLA = ["call", "put"]
    EXOTIC = ["lookback_min_call", "lookback_max_call",
                     "lookback_min_put", "lookback_max_put",
                "barrier_call", "barrier_put", "asian_call", "asian_put"]
    STRIKE_SPOT = ["call", "put", "lookback_min_call", "lookback_max_call",
                     "lookback_min_put", "lookback_max_put", "asian_call", "asian_put"]
    STRIKE_SPOT_BARRIER = ["barrier_call", "barrier_put"]
    PATH_INDEPENDENT = ["call", "put"]
    PATH_DEPENDENT = ["lookback_min_call", "lookback_max_call",
                        "lookback_min_put", "lookback_max_put",
                        "barrier_call", "barrier_put", "asian_call", "asian_put"]
