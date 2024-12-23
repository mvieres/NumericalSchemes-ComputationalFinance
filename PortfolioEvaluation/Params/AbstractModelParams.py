

class AbstractModelParams:

    def __init__(self):
        self.t_start = None
        self.t_end = None
        self.starting_point = None

    def get_t_start(self):
        return self.t_start

    def get_t_end(self):
        return self.t_end

    def get_starting_point(self):
        return self.starting_point

    def set_starting_point(self, s0: float):
        self.starting_point = s0

    def set_t_start(self, t_start: float):
        self.t_start = t_start

    def set_t_end(self, t_end: float):
        self.t_end = t_end
