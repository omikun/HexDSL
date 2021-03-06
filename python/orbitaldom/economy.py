'models a rough economy'
import yaml
import math
from market import Market, Trade

range = xrange
# basic system of industries being producer/consumers


class Value:
    'tracks market price and quantity?'
    '''
    market is a dumping ground of all outputs, combined, 
        if each industry sells to the market, we can treat the market as a bank of money/commodities stores
            industry sells n outputs to market for m dollars
                industry.stock[output] -= n
                industry.stock[dollar] += m
                market.stock[output] += n
                market.stock[dollar] -= n
            buyers then must buy output at total dollars/total amount
        but this decouples producers from demand
            must build a backpressure into this, when demand dwindles, suppliers don't get their money
        industry transfers to market, where all outputs are pooled into ask entries:
            (per unit price, quantity, seller)
        buyers then submit bids (total amount)
        buyers with highest bids gets cheapest products first at asking price
    '''
    def __init__(self, s):
        self.number = 0
        self.net = 0
        self.name = s

    def __repr__(self):
        return str('%.2f' % self.number)

    def __add__(self, b):
        if isinstance(b, Value):
            b = b.number
        return self.number + b

    def __iadd__(self, b):
        if isinstance(b, Value):
            b = b.number
        elif isinstance(b, tuple):
            price = b[1]  # assumes price is worth of quantity added
            self.net += price  # need to add price to all operations
            b = b[0]
        self.number += b
        return self

    def takeout(self, b):
        'takes at most amounb b from self'
        if isinstance(b, Value):
            b = b.number
        amount = max(0, min(self.number, b))
        # print 'SUBTRACTING!!!!!!!!', self.name, 'num: ', self.number, '-', amount, '=', 
        self.number -= amount
        return amount


class Industry:
    'a company that turns some resources into one output resource'
    def __init__(self, n, d):
        self.d = d
        self.market = None
        self.name = n
        self.stock = d['stock']
        if len(d) > 2:
            raise ValueError('cant handle more than 1 output')
        out = None
        for name, e in d.items():
            if name == 'stock':
                continue
            out = e
            self.output_name = name
        self.input_ = out['Input']
        self.output_ = out['Output']
        self.waste_ = out['Waste']
        self.logic = None
        if 'Logic' in out:
            self.logic = out['Logic']

    def outputRate(self):
        return self.output_[0]

    def waste(self):
        return self.waste_[0]

    def wastePrice(self):
        return self.waste_[1]

    def pricePerOutput(self):
        'TODO compute cost of inputs + profit per unit output'
        cost_per_output = 0
        for name, good in self.input_.items():
            cost_per_output += self.priceOfStockUnit(name) * self.inRate(name)
        return cost_per_output
    
    def price(self):
        return self.output_[1]

    def inRate(self, name):
        # print 'inRate:', name, self.input
        # print type(self.input[name][0])
        return self.input_[name][0]

    def inFactor(self, name):
        return self.input_[name][1]

    def addToStock(self, name, amount, cost=None):
        self.stock[name][0] += amount
        if cost:
            self.addToStockCost(name, cost)
    
    def takeFromStock(self, name, amount, cost):
        self.addToStock(name, -amount, -cost)

    def priceOfStockUnit(self, name):
        return self.stockCost(name) / float(self.stockAmount(name))

    def stockAmount(self, name):
        # print 'stockAmount:', name, self.stock
        return self.stock[name][0]
    
    def minStock(self, name):
        return self.stock[name][1]

    def maxStock(self, name):
        return self.stock[name][2]

    def replStockRate(self, name):
        'designated max rate of replenishing stock per turn'
        return self.stock[name][3]

    def stockCost(self, name):
        'cumulative cost of everything in stock'
        return self.stock[name][4]

    def addToStockCost(self, name, amount):
        self.stock[name][4] += amount

    def subStockCost(self, name, amount):
        self.subStockCost(name, -amount)

    def replStockAmount(self, name):
        'amount to replenish stock per turn'
        to_fill = self.maxStock(name) - self.stockAmount(name)
        to_fill = min(to_fill, self.replStockRate(name))
        return to_fill
    
    def getMaxOutput(self):
        ret = min(self.stockAmount(n) // self.inRate(n) for n in self.input_)
        ret = max(0, ret)
        ret = min(ret, self.outputRate())
        ret *= max(0, min(1, self.getOutputFraction()))
        # ret = min(ret, self.output_rate)
        print self.name, 'can make', ret, self.output_name
        print self.stock
        return self.output_name, ret

    def getOutputFraction(self):
        'compute fraction of max output w/ logic'
        if not self.logic:
            return 1
        x = self.logic[0]
        x = self.stockAmount(x) / float(self.maxStock(x))
        fraction = eval(self.logic[1])
        fraction = round(fraction, 2)
        print 'logicing~~~~~~~ %.2f %.2f' % (x, fraction) 
        return fraction

    #### modifies actual data
    def produce(self, market):
        'create outputs, add output/waste to market'
        output, num_out, price, waste = self.makeOutput()
        unit_price = price / float(num_out)
        market.addToSell(Trade(output, unit_price, num_out, self)
        market.addToSell(Trade('waste', .01, waste, self)
    
    def makeOutput(self):
        'get max output, consume equivalent inputs'
        output, num_out = self.getMaxOutput()
        total_cost = 0
        for n in self.input_.keys():
            input_cost = self.pricePerOutput() * num_out
            total_cost += input_cost
            num_inputs = self.inRate(n) * num_out
            self.takeFromStock(n, num_inputs, input_cost)
        profit = 1
        waste = self.waste() * num_out
        return output, num_out, total_cost+profit, waste

    def replenishStock(self, market):
        'for each stock not at max, purchase from market'
        # TODO consider historical price: buy more at low price
        # TODO buy least stocked item/most needed/most valuable
        cash_on_hand = self.stockAmount('dollar')
        for name, e in self.stock.items():
            if name not in market.asks or name not in self.input_:
                continue
            to_fill = self.replStockAmount(name)
            if to_fill == 0:
                continue
            # make sure there's enough money for it
            can_afford = self.stockAmount('dollar') / self.market[name]
            print 'can afford: ', can_afford, name
            to_fill = min(to_fill, can_afford)
            self.addToStock(name, market[name].takeout(to_fill))
            self.takeFromStock('dollar', to_fill * self.market[name])


def writeIndustryCycleDot(industries):
    def arrow(first, second):
        return '\n' + first + ' -> ' + second

    out = 'digraph G {'
    for ind_name, ind in industries.items():
        out += '\n' + ind_name + ' [shape=box]'
        out += arrow(ind_name, ind.output_name)
        for in_name, inList in ind.input.items():
            out += arrow(in_name, ind.name)
    out += '\n}'
    with open('ind_dep.dot', 'w') as f:
        f.write(out)

if __name__ == '__main__':
    config = None
    industries = {}
    with open('industry_dep.yaml') as f:
        config = yaml.load(f)
        print config
        for name, ind in config.items():
            if name == 'Example':
                continue
            industries[name] = Industry(name, ind)

    # writeIndustryCycleDot(industries)

    # mines gets pre-existing ore, drilling gets wells
    # market = {'Waste': Value('waste')}
    market = Market()

    while True:
        for name, ind in industries.items():
            ind.produce(market)
        for name, ind in industries.items():
            ind.replenishStock(market)

            # get rid of everything else?
        #    output_name, output, price, waste = ind.produce()
        #    ind.replenishStock(market)
        #    market['Waste'] += waste
        #    market.setdefault(output_name, Value(output_name))
        #    market[output_name] += (output, price)
        #    print '%s added %.2f' % (output_name, output)
        for thing, num in market.items():
            print '%s: %s' % (thing, num)
        raw = raw_input('enter something: ')
