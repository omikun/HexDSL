'''Market allows traders to park inventory and 
    buyers a common interface to access goods
'''

from SortedCollection import *

class Trade:
    def __init__(self, commodity, unit_price, amount, trader):
        'params are float, float, Industry'
        self.unit_price = unit_price
        self.amount = amount
        self.trader = trader
        self.name = commodity

    def __repr__(self):
        return '%s selling %f %s at $%f/unit' \
            & (self.trader, self.amount, self.name, self.unit_price)
    

class Market:
    def __init__(self):
        self.com = {}
        # commodities are dictionaries key=good
        # each entry is an array of asks ordered by unit price

    def addTrade(self, ask):
        'add an ask, merge same trader/price asks'
        self.com.setdefault(ask.commodity, 
                            SortedCollection([], key=lambda x: x.unit_price))
        # search through and check if same price/trader
        for iter in self.com[ask.commodity]:
            if iter.unit_price == ask.unit_price and \
            iter.trader == ask.trader:
                iter.amount += ask.amount
                break
        else:
            self.com[ask.commodity].insert(ask)

    def buy(self, bid):
        'searches for cheapest bid, transfer assets'
        while bid.amount != 0 and self.com[bid.commodity] != []:
            
