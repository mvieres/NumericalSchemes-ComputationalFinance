from enum import Enum


class OptionEnum(Enum):

    CALL = "call_option"
    PUT = "put_option"
    LOOKBACK_MIN_CALL = "lookback_min_call_option"