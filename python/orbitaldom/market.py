'''Market allows traders to park inventory and allow
    bids to access goods over a common interface
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
        return '%s selling %f %s at $%f/unit' % (self.trader.id, self.amount, self.name, self.unit_price)
    

class Market:
    def __init__(self):
        self.asks = {}
        self.bids = {}
        # commodities are dictionaries key=good
        # each entry is an array of asks ordered by unit price

    def addToSell(self, ask):
        'add ask to asks'
        self.addToMarket(ask, self.asks)

    def addToBuy(self, bid):
        'add bid to bids'
        self.addToMarket(bid, self.bids)

    def addToMarket(self, trade, traders):
        'add trade, merge same trader/price asks'
        traders.setdefault(trade.name, 
                            SortedCollection([], key=lambda x: x.unit_price))
        # search through and check if same price/trader
        for iter in traders[trade.name]:
            if iter.unit_price == trade.unit_price and \
            iter.trader == trade.trader:
                iter.amount += trade.amount
                break
        else:
            traders[trade.name].insert(trade)

    def tick(self):
        'commence trade between bids and asks'
        # take bids with highest bids
        for good, bids in self.bids.items():
            for bid in reversed(bids):
                print 'biding', bid
                self.buy(bid)

    def buy(self, bid):
        'searches for cheapest bid, transfer assets, return if successful'
        name = bid.name
        buyer = bid.trader
        can_pay = bid.unit_price * bid.amount
        for ask in self.asks[name]:  # assumes starting w/ cheapest asks
            if bid.amount == 0:
                break
            print ask
            seller = ask.trader
            unit_price = ask.unit_price
            # get amount that can be bought at ask price
            bid_amount = min(bid.amount, can_pay / unit_price)  # num units
            bid_amount = min(bid_amount, ask.amount)
            bid_price = bid_amount * unit_price
            amount = min(bid_amount, ask.amount)
            print 'bought ', name, 'at $', bid_price, ' for ', bid_amount, 'units from ', seller.id
            # transfer amount from com to bid.trader
            buyer.addToStock(name, amount)
            seller.takeFromStock(name, amount)
            bid.amount -= bid_amount
            ask.amount -= bid_amount
            # transfer dollars
            seller.addToStock('dollar', bid_price)
            buyer.takeFromStock('dollar', bid_price)
            can_pay -= bid_price
            if ask.amount == 0:
                print 'removed', ask
                self.asks[name].remove(ask)
        # if return false, then demand > supply
        return bid.amount == 0


class Industry:
    def __init__(self, id, cash, stock):
        self.id = id
        self.cash = cash
        self.stock = stock
    
    def stockAmount(self, name):
        if name == 'dollar':
            return self.cash
        else:
            return self.stock
    
    def addToStock(self, name, amount):
        if name == 'dollar':
            self.cash += amount
        else:
            self.stock += amount
    
    def takeFromStock(self, name, amount):
        self.addToStock(name, -amount)
    
    def __repr__(self):
        return 'trader: %d, $%.2f %.2f unit' % (self.id, self.cash, self.stock)

if __name__ == '__main__':
    market = Market()
    asks = [Industry(i, 100, 100) for i in xrange(5)] 
    print asks

    print 'trading'
    sells = [Trade('wood', 4, 30, asks[0]),
             Trade('wood', 4, 40, asks[1]),
             Trade('wood', 7, 30, asks[2])] 
    buys = [Trade('wood', 6, 30, asks[3]),
            Trade('wood', 2, 100, asks[4])]

    for sell in sells:
        market.addToSell(sell)
    for buy in buys:
        market.addToBuy(buy)

    market.tick()

    for trader in asks:
        print trader
