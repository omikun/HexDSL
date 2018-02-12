'government consists of programs and voting body on bills'
from common import srandom, itbounds, issueTopics
from issue import Issue, Citizen
from democracy import Democracy


class GovernmentProgram:
    'impacts public, good and bad'
    def __init__(self, name, topic, fund, t=None):
        'a gov program, possibly more than 1 per topic'
        self.name = name
        self.topic = topic
        self.annualFund = fund
        self.outrageThreshold = t if t else srandom.randint(10, 70)

    def changeFunding(self, amount):
        'reflect funding change'
        if amount < 0:
            self.cutFunding(-amount)
        else:
            self.addFunding(amount)
    
    def addFunding(self, amount):
        # if people love this above a threshold, boost productivity, political capital?
        self.annualFund += amount

    def cutFunding(self, amount):
        if self.annualFund < amount:  # can't cut more than current funding
            raise ValueError('hey man, you cant be cutting more than allocated' + self.topic + '.' + self.name)
        else:
            self.annualFund -= amount
        if (amount * 100) / self.annualFund > self.outrageThreshold:  # cutting more than
            print 'start a public outcry!!'
    
    def DoStuff(self):
        'event tick per turn, what does a program do??'
        # military: more money more security, dominance
        # surveillance: more money less privacy for citizens, more security, better able to spy other countries
        # immigration: more money more people through? 
        # cbp: more money less people, more hassle to travel
        # healthcare: more money more coverage, lower medical cost
        # manufacturing: more money more insentive
        # jobs: more money more jobs, more productivity?
        # tech: more money better tech, less jobs (sometimes more jobs)
        # 'security privacy immigration jobs education healthcare tax manufacture tech'


class Government:
    'public votes for senate members, senate votes on bills: budget in billions'
    # TODO implement public 
    def __init__(self, name, budget, citizens):
        self.name = name
        self.public = Democracy('public', 435, public=True)
        self.senate = Democracy('Senate', 100, public=False)
        self.budget = budget
        self.programs = {}
        self.citizens = citizens
        for t in issueTopics:
            self.programs[t] = GovernmentProgram(t, t, budget/len(issueTopics))
        # TODO implement mandatory/discretionary spending, bills to ammend
        # self.programs = {'Discretionary': [], 'Mandatory': []}

    def newBill(self):
        # figure out which gov program to change
        # compute available amount of money in bill
        pass

    def sendBillToSenate(self, bill):
        self.senate.countVote(bill)
    

if __name__ == '__main__':
    citizens = []  # need citizens...
    gov = Government('usa gov', 4000, citizens)