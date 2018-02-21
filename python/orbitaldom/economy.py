'models a rough economy'
import yaml

range = xrange
# basic system of industries being producer/consumers


class Value:
    'implements a concrete number, one with existance, no copy'
    def __init__(self, s, n):
        self.number = n
        self.name = s

    def __repr__(self):
        return str(self.number)

    def __add__(self, b):
        if isinstance(b, Value):
            b = b.number
        return self.number + b

    def __iadd__(self, b):
        if isinstance(b, Value):
            b = b.number
        self.number += b
        return self

    def takeOut(self, b):
        'takes at most amounb b from self'
        if isinstance(b, Value):
            b = b.number
        amount = max(0, min(self.number, b))
        # print 'SUBTRACTING!!!!!!!!', self.name, 'num: ', self.number, '-', amount, '=', 
        self.number -= amount
        return amount


class Industry:
    'a company that turns some resources into others'
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs

if __name__ == '__main__':
    industries = None
    with open('industry_dep.yaml') as f:
        industries = yaml.load(f)
        print industries
    # ore is free
    common = {'Waste': Value('waste', 0)}
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
                stock[n_in] += common[n_in].takeOut(need_fill)
        for thing, num in common.items():
            print thing, ': ', num
        raw = raw_input('enter something: ')
    # print common store
