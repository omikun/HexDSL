from common import *
import numpy as np
from issue import Issue
from government import Government
from democracy import Democracy


# same as above, assigns upper/lower boundaries to each topic
# {itbounds[t]:([int(a) for a in b.split(',')]) for t, b in zip(issueTopics, itscales)}


class Country:
    def __init__(self, name, budget, p):
        self.name = name
        self.productivity = p
        self.citizens = [Citizen()]
        self.government = Government(name, budget, citizens=self.citizens)

# citizens
#   -> taxed by gov 13%
#   -> rent 40% -> land owners
#   -> food 10% -> agriculture
#   -> goods 20% -> manufacturers
#   -> investment 17%? -> stock market

# gov spends 4T, taxes 3.3T (13% assumes corps don't exist)
# citizens make 20T
# gov spends 4T, goes to citizens
# gov taxes 3.3T from citizens





if __name__ == '__main__':
    numPop = 100
    usa = Democracy('usa', numPop)
    usa.newBill()
    usa.voteBill()
    usa.enactBill()
 
