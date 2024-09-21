

class AbstractModelParams:

    def __init__(self):
        self.t_start = None
        self.t_end = None
        self.s0 = None

    def get_t_start(self):
        return self.t_start

    def get_t_end(self):
        return self.t_end

    def get_s0(self):
        return self.s0

    def set_s0(self, s0: float):
        self.s0 = s0

    def set_t_start(self, t_start: float):
        self.t_start = t_start

    def set_t_end(self, t_end: float):
        self.t_end = t_end
