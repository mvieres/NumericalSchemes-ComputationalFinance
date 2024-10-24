import numpy as np

supported_payoffs = {
    "call_option": lambda x, strike: np.maximum(x - strike, 0),
    "put_option": lambda x, strike: np.maximum(strike - x, 0),
    "lookback_min_call_option": lambda x, strike: np.maximum(np.min(x) - strike, 0),
    "lookback_max_call_option": lambda x, strike: np.maximum(np.max(x) - strike, 0),
    "lookback_min_put_option": lambda x, strike: np.maximum(strike - np.min(x), 0),
    "lookback_max_put_option": lambda x, strike: np.maximum(strike - np.max(x), 0),
    "barrier_call_option": lambda x, strike, barrier: np.maximum(x[-1] - strike, 0) * (np.max(x) > barrier),
    "barrier_put_option": lambda x, strike, barrier: np.maximum(strike - x[-1], 0) * (np.min(x) < barrier),
    "asian_call_option": lambda x, strike: np.maximum(np.mean(x) - strike, 0),
    "asian_put_option": lambda x, strike: np.maximum(strike - np.mean(x), 0)
}

classification = {
    "vanilla": ["call_option", "put_option"],
    "exotic": ["lookback_min_call_option", "lookback_max_call_option",
                    "lookback_min_put_option", "lookback_max_put_option",
               "barrier_call_option", "barrier_put_option", "asian_call_option", "asian_put_option"],
    "strike_spot": ["call_option", "put_option", "lookback_min_call_option", "lookback_max_call_option",
                    "lookback_min_put_option", "lookback_max_put_option", "asian_call_option", "asian_put_option"],
    "strike_spot_barrier": ["barrier_call_option", "barrier_put_option"],
    "path_independent": ["call_option", "put_option"],
    "path_dependent": ["lookback_min_call_option", "lookback_max_call_option",
                       "lookback_min_put_option", "lookback_max_put_option",
                       "barrier_call_option", "barrier_put_option", "asian_call_option", "asian_put_option"]
}