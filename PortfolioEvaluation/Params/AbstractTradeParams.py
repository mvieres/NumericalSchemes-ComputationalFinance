

class AbstractTradeParams:

    def __init__(self):
        self.category = None
        self.underlying = None
        self.id = None
        self.quantity = None

    def from_dict(self, data):
        self.id = data.get("id")
        self.underlying = data.get("underlying")
        self.quantity = data.get("quantity", 1)

    def get_id(self):
        return self.id

    def get_quantity(self):
        return self.quantity

    def set_id(self, id):
        self.id = id

    def set_quantity(self, quantity):
        self.quantity = quantity

    def set_category(self, category):
        self.category = category

    def get_category(self):
        return self.category