

class PortfolioParams:
    """
    TODO: This class is somewhat not useful at the moment.

    """
    def __init__(self):
        self.simulation_config = None
        self.trades = None
        self.name = None

    def from_dict(self, data):
        self.simulation_config = data['simulation_config']
        self.trades = data['trades']
        self.name = data['name']

    def set_simulation_config(self, simulation_config):
        self.simulation_config = simulation_config

    def set_trades(self, trades):
        self.trades = trades

    def set_name(self, name):
        self.name = name

    def get_simulation_config(self):
        return self.simulation_config

    def get_trades(self):
        return self.trades

    def get_name(self):
        return self.name
