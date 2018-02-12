import random

srandom = random.SystemRandom()

# the set of topics people care about in a country
issueTopics = 'security privacy immigration jobs education healthcare tax manufacture tech'.split(' ')
# TOADD: debt - positive means paying for it!! but where does the debt go? whoever owns that debt - buyers of that debt, private companies, banks, individuals, or foreign companies, individuals, or governments!
# lower and upper bounds of preferences
itscales = '-2,5 -4,4 -10,5 2,6 -5,3 2,5 -8,3 -2,4 -7,2'.split(' ')
# issue topic boundaries of preferences
itbounds = {}
for topic, scales in zip(issueTopics, itscales):
    bounds = ([int(a) for a in scales.split(',')])
    itbounds[topic] = bounds


def is_int(n):
    try:
        int(n)
        return True
    except:
        return False