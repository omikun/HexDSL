import random
import yaml
srandom = random.SystemRandom()

# the set of topics people care about in a country
# TOADD: debt - positive means paying for it!! but where does the debt go? whoever owns that debt - buyers of that debt, private companies, banks, individuals, or foreign companies, individuals, or governments!
# lower and upper bounds of preferences
issueInput = '''
    patriotism: [-1, 14]
    debt: [-10, 2]
    security: [-2, 6]
    privacy: [-8, 4]
    immigration: [-9, 5]
    jobs: [2, 6]
    trust: [-5, 4]
    health: [2, 5]
    tax: [-1, 10]
    roads: [-3,7]
    tech: [-7, 5]
    money: [4, 10]
    food: [-1, 8]
    '''

# issue topic boundaries of preferences
itbounds = yaml.load(issueInput)
# itbounds = {}
# for topic, scales in zip(issueTopics, itscales):
#     bounds = ([int(a) for a in scales.split(',')])
#     itbounds[topic] = bounds


def is_int(n):
    try:
        int(n)
        return True
    except:
        return False
