

class AbstractTradeParams:

    def __init__(self):
        self.underlying = None
        self.id = None
        self.quantity = None
        self.models = None

    def from_dict(self, data):
        self.id = data.get("id")
        self.underlying = data.get("underlying")
        self.quantity = data.get("quantity", 1)
        self.models = data.get("models", None)

    def get_id(self):
        return self.id

    def get_quantity(self):
        return self.quantity

    def set_id(self, id):
        self.id = id

    def set_quantity(self, quantity):
        self.quantity = quantity

    def get_underlying(self):
        return self.underlying

    def get_models(self):
        return self.models

    def set_models(self, model):
        self.models = model