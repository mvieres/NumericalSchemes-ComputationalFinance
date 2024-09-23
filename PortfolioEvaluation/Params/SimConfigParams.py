

class SimConfigParams:

    def __init__(self):
        self.discretization = None
        self.n_paths = None
        self.use_constant_interest_rate = None
        self.reference_yield_curve = None
        self.default_models_fallback = {
            "stock_option": "BlackScholes",
            "interest_rate": "TrolleSchwartz",
            "foreign_exchange": "Heston"
        }
        self.default_models = None

    def from_dict(self, data):
        self.discretization = data.get('discretization', 100)
        self.n_paths = data.get('mc_steps', 1000)
        self.use_constant_interest_rate = data.get('use_constant_interest_rate', False)
        self.reference_yield_curve = data.get('reference_yield_curve')
        self.default_models = data.get('default_models', self.default_models_fallback)

    def set_discretization(self, discretization):
        self.discretization = discretization

    def set_n_paths(self, n_paths):
        self.n_paths = n_paths

    def set_use_constant_interest_rate(self, use_constant_interest_rate):
        self.use_constant_interest_rate = use_constant_interest_rate

    def set_reference_yield_curve(self, reference_yield_curve):
        self.reference_yield_curve = reference_yield_curve

    def set_default_models(self, default_models):
        self.default_models = default_models

    def get_discretization(self):
        return self.discretization

    def get_n_paths(self):
        return self.n_paths

    def get_use_constant_interest_rate(self):
        return self.use_constant_interest_rate

    def get_reference_yield_curve(self):
        return self.reference_yield_curve

    def get_default_models(self):
        return self.default_models
