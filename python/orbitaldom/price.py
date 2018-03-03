'evaluate the price'
from common import srandom
from decimal import *

class Price:
    def __init__(self, d, s):
        self.demand = d
        self.supply = s
        self.high = 20
        self.low = -10
        self.trust = 4
        self.price = 0

    def __repr__(self):
        return price

    def getPrice(self):
        center = self.demand / float(self.supply / 4.0)
        low = max(0, center + self.low)
        high = center + self.high
        high = high if high > (low + 2) else low+2
        self.price = srandom.random() * (high - low) + low
        print '%.2f %.2f %.2f' % (self.price, high, low)

if __name__ == '__main__':
    wood = Price(4, 3)
    getcontext().prec = 2
    for i in xrange(10):
        # print  '%.2f' % wood
        wood.getPrice()
        wood.supply += i
