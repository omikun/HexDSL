class Ask:
    def __init__(self, unit_price, amount, seller):
        'params are float, float, Industry'
        self.unit_price = unit_price
        self.amount = amount
        self.seller = seller
    

class Market:
    def __init__(self):
        self.com = {}
        # commodities are dictionaries key=good
        # each entry is an array of asks ordered by unit price
        pass

    def addAsk(self, ask):
        'add an ask, merge same seller/price asks'