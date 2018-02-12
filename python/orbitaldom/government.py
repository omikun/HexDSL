'government consists of programs and voting body on bills'
from common import srandom, itbounds, issueTopics, is_int
from issue import Issue, Citizen
from democracy import Democracy
import yaml

class GovernmentProgram:
    'impacts public, good and bad'
    def __init__(self, name, topic, fund, effects, outrage=None):
        'a gov program, possibly more than 1 per topic'
        self.name = name
        self.topic = topic
        self.annualFund = fund
        self.outrageThreshold = outrage if outrage else srandom.randint(10, 70)
        self.effects = effects
    
    def __repr__(self):
        s = ''
        for k, v in self.__dict__.items():
            s += '\t' + k + ':' + str(v) + '\n'
        return s

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
    'programs that affect citizens, lets a senate vote on those bills'
    # TODO implement public 
    def __init__(self, name, budget, citizens):
        self.name = name
        self.bill = {}  # not same bill as senate.bill - this is just budget
        self.public = Democracy('public', 435, public=True)
        self.senate = Democracy('Senate', 100, public=False)
        self.budget = budget
        self.politicalcapital = 10
        self.darkmoney = 10
        self.citizens = citizens
        with open('govprogs.yaml') as f:
            budget = yaml.load(f)
        print budget
        self.programs = budget
        if 'Discretionary' not in self.programs:
            raise ValueError('needs to have discretionary spending in budget yaml')
        return
    
    def __repr__(self):
        s = ''
        for k, v in self.__dict__.items():
            if k != 'citizens':
                s += k + ' : ' + str(v) + '\n'
        return s

    def newBill(self):
        # figure out which gov program to change
        # compute available amount of money in bill
        # compute preference delta from funding changes
        # ask democracy to vote
        pass
        

    def voteBill(self):
        self.senate.voteBill()
        # it would be great to freeze a bill, and change one vote
    
    def doPolitics(self):
        'influence senators in general or influence a particular senator'
        topic, degree = self.askBillEntry()
        # how much would this cost? money? political capital? rider?
        if self.doPolitk(topic, degree):
            # take 2 most negative in topic and bump them by degree
            pass
    
    def doMorePolitics(self):
        'could try to get bill vetoed'
        print "That's going to cost you "
        topic, degree = self.askBillEntry()
        # do something special
        if self.doPolitk(topic, degree):
            self.senate.bill = None

    def doPolitk(self, topic, degree):
        'bribe with money, political cap, or a rider bill'
        politiks = 'money pc rider'.split(' ')
        p = srandom.choice(politiks)
        # TODO just testing
        p = 'rider'
        message = p + ' '
        bribe = None
        if p == 'money':
            bribe = srandom.randint(1, 5) * abs(degree)
            message += str(bribe)
        elif p == 'pc':
            bribe = srandom.randint(1, 5) * abs(degree)
            message += str(bribe)
        elif p == 'rider':
            # TODO check bribe_topic:amount is not less in magnitude than bill
            print self.programs['Discretionary'].keys()
            bribe_topic = srandom.choice(self.programs['Discretionary'].keys())
            bribe_amount = srandom.randint(1, 4) * abs(degree)
            message += bribe_topic + ' with ' + str(bribe_amount)
        else:
            raise ValueError('not a valid political move')
        answer = 'c'
        while answer != 'y' and answer != 'n':
            answer = raw_input('Spend ' + message + '? y/n\n> ')
        
        if answer == 'y':
            if p == 'money' and self.darkmoney > bribe:
                self.darkmoney -= bribe
            elif p == 'pc' and self.politicalcapital > bribe:
                self.politicalcapital -= bribe
            elif p == 'rider':
                if not self.senate.bill:
                    self.senate.bill = {}
                self.senate.bill[bribe_topic] = bribe_amount
            else:
                return False  # if can't do any of the following
            return True
        else:
            return False
    
    def enactBill(self):
        if self.senate.bill:
            pass  # apply bill to action!
        else:
            print 'no bill to enact'

    def askBillEntry(self):
        topic = ''
        while topic not in self.programs['Discretionary'].keys():
            topic = raw_input('Enter topic to change: ')
        degree = None
        while not is_int(degree):  # (-10 < degree < 10):
            degree = int(raw_input('Enter how much to change: '))
        return topic, degree

    def craftBill(self):
        self.bill = {}
        # TODO add random chance of fixed topic
        # up to 3 topics
        for i in xrange(1):
            topic, degree = self.askBillEntry()
            # while topic in self.bill:
            #    topic, degree = self.askBillEntry()
            #    if topic == 'skip':
            #        return
            self.bill[topic] = degree
        # convert to senate sentiment bill
        self.senate.bill = {}
        for topic in self.bill:
            for k, v in self.programs['Discretionary'][topic]['effect'].items():
                print 'config file: ', k, v
                if k in self.senate.bill:
                    self.senate.bill[k] += v
                else:
                    self.senate.bill[k] = v
        print 'senate bill: ', self.senate.bill




if __name__ == '__main__':
    c = [Citizen(public=False) for i in xrange(100)]  # need citizens...
    gov = Government('usa gov', budget=4000, citizens=c)
    print gov
    # per turn,
    while True:
        # craft bill & guage reactions
        gov.craftBill()
        # do politics
            # propaganda, shift senator xor publics opinion
        gov.doPolitics()
        # vote for bill
            # voting will cost political willpower
            # ex. if voted for tech=5, unlikely to vote for tech=5 again
        gov.voteBill()
        # enact bill
        gov.doMorePolitics()
        # block bill enforcement (veto, law suit)
        gov.enactBill()