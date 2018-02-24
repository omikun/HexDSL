'models a rough economy'
import yaml
import math

range = xrange
# basic system of industries being producer/consumers


class Value:
    'implements a concrete number, one with existance, no copy'
    def __init__(self, s, n):
        self.number = n
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
        self.input = out['Input']
        self.output = out['Output']
        self.logic = None
        if 'Logic' in out:
            self.logic = out['Logic']

    def outputRate(self):
        return self.output[0]

    def waste(self):
        return self.output[1]

    def inRate(self, name):
        # print 'inRate:', name, self.input
        # print type(self.input[name][0])
        return self.input[name][0]

    def inFactor(self, name):
        return self.input[name][1]

    def addToStock(self, name, amount):
        self.stock[name][0] += amount

    def takeFromStock(self, name, amount):
        self.stock[name][0] -= amount

    def stockAmount(self, name):
        # print 'stockAmount:', name, self.stock
        return self.stock[name][0]
    
    def maxStock(self, name):
        return self.stock[name][1]

    def replStockRate(self, name):
        'designated max rate of replenishing stock per turn'
        return self.stock[name][2]

    def replStockAmount(self, name):
        'amount to replenish stock per turn'
        to_fill = self.maxStock(name) - self.stockAmount(name)
        to_fill = min(to_fill, self.stock[name][2])
        return to_fill
    
    def getMaxOutput(self):
        ret = min(self.stockAmount(n) // self.inRate(n) for n in self.input)
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

    def produce(self):
        'get max output, consume equivalent inputs'
        output, num_out = self.getMaxOutput()
        for n in self.input:
            self.takeFromStock(n, self.inRate(n) * num_out)
        waste = self.waste() * num_out
        return output, num_out, waste

    def replenishStock(self, common):
        for name, e in self.stock.items():
            if name not in common or name not in self.input:
                continue
            to_fill = self.replStockAmount(name)
            self.addToStock(name, common[name].takeout(to_fill))

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
    # ore is free
    common = {'Waste': Value('waste', 0)}
    while True:
        for name, ind in industries.items():
            output_name, output, waste = ind.produce()
            ind.replenishStock(common)
            common['Waste'] += waste
            if output_name not in common:
                common[output_name] = Value(output_name, 0)
            print '%s added %.2f' % (output_name, output)
            common[output_name] += output
        for thing, num in common.items():
            print '%s: %s' % (thing, num)
        raw = raw_input('enter something: ')
