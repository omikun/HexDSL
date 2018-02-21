'models a rough economy'
import yaml

# basic system of industries being producer/consumers

class Industry:
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs

if __name__ == '__main__':
    with open('industry_dep.yaml') as f:
        industries = yaml.load(f)
        print industries
    # ore is free
    common = {'Waste':0}
    while True:  # each turn
        for name, ind in industries.items():
            print name, ':'
            # determine max output from stock
            stock = ind['stock']
            max_output = 0
            for output_name, output in ind.items():
                if output_name == 'stock':
                    continue
                max_output = min(stock[input_name] // amount for input_name, amount in output['Input'].items())
                print name, 'can make ', max_output, output_name
                common['Waste'] += output['Waste'] * max_output
                if output_name in common:
                    common[output_name] += max_output * output['Output']
                else:
                    common[output_name] = max_output
            # get consume stock, produce to common store
            for output_name, output in ind.items():
                if output_name == 'stock':
                    continue
                for input_name, amount in output['Input'].items():
                    print 'stock:', stock
                    stock[input_name] -= max_output * amount
            # get more stock from common store
            for input_name in stock.keys():
                if input_name not in common:
                    continue
                # say max stock of 100
                # if common has enough to fill stock to 100, do that
                # else fill rest into
                pass
        for thing, num in common.items():
            print thing, ': ', num
        raw = raw_input('enter something: ')
    # print common store
