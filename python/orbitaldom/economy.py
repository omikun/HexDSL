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
        ret = min(ret, self.outputRate)
        # ret = min(ret, self.output_rate)
        print self.name, 'can make', ret, self.output_name
        print self.stock
        ret *= self.getOutputFraction()
        return self.output_name, ret

    def getOutputFraction(self):
        'compute fraction of max output w/ logic'
        if self.logic:
            fraction = 0
            x = self.logic[0]
            x = self.stockAmount(x) / float(self.maxStock(x))
            statement = ''
            for i, l in enumerate(self.logic):
                if i == 0:
                    continue
                if l == 'log':
                    fraction = eval('math.log(x)')
                else:
                    fraction = eval('fraction' + str(l))
            print 'logicing~~~~~~~ %.2f %.2f' % (x, fraction) 
            return fraction
        else:
            return 1

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


def obsolete():
    common = {'Waste': Value('waste', 0)}
    industries = {}
    while True:  # each turn
        for n_ind, ind in industries.items():
            print n_ind + ':'
            # determine max output from stock
            stock = ind['stock']
            max_output = 0
            print 'stock:', stock
            for n_out, output in ind.items():
                if n_out == 'stock':
                    continue
                max_output = min(stock[n_in] // amount
                                 for n_in, amount in output['Input'].items())
                max_output = max(0, max_output)
                print n_ind, 'can make', max_output * output['Output'], n_out
                common['Waste'] += output['Waste'] * max_output
                if n_out not in common:
                    common[n_out] = Value(n_out, 0)
                common[n_out] += max_output * output['Output']
                # print 'Adding to common:', n_out, max_output * output['Output']
                # get consume stock, produce to common store
                for n_in, amount in output['Input'].items():
                    if stock[n_in] < max_output * amount:
                        raise ValueError(str(n_in, stock[n_in], '<', max_output, '*', amount))
                    stock[n_in] -= max_output * amount

            # get more stock from common store
            for n_in, amount in stock.items():
                if n_in not in common:
                    continue
                # say max stock of 100
                need_fill = max(0, 10 - amount)
                stock[n_in] += common[n_in].takeout(need_fill)
        for thing, num in common.items():
            print thing, ': ', num
        raw = raw_input('enter something: ')
    # print common store
