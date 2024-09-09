from Market.Market import Market


class JumpToRuin(Market):
    """
    Jump to ruin model introduced by Merton (1976).
    """
    def __init__(self, t_start: float, t_end: float, s0: float, r: float, mue: float, sigma: float, lamb: float, scheme: str):
        super().__init__(t_start, t_end, s0, r)
        pass