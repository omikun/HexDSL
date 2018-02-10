import random
import numpy as np

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

# same as above, assigns upper/lower boundaries to each topic
# {itbounds[t]:([int(a) for a in b.split(',')]) for t, b in zip(issueTopics, itscales)}

print itbounds
class Issue:
    'for/against of issues in a bill, a person, an official, or even government'
    def __init__(self, kv=None):
        self.topics = {}
        self.threshold = 0  # could be tweaked based on hate against gov
        if kv:
            # self.topics = dict.fromkeys(self.topics, 0)  # reset entries to 0
            for k, v in kv.items():
                self.topics[k] = v
        else:
            for topic,b in itbounds.items():
                self.topics[topic] = srandom.randint(b[0], b[1])
                # TODO: try numpy bimodal distribution (some how? multivariate? mix normal?)
                # or just make up my own distribution with this: 
                # np.random.choice(ny.arange(1, 7), p=[0.1, 0.05, 0.05, 0.2, 0.4, 0.2])
            return

    def getOpinionOn(self, issue):
        s = sum(self.topics[k] * v for k, v in issue.topics.items())
        l = len(issue.topics)
        return s / float(l)

    def vote(self, issue):
        'didvote must be called first!'
        #didntvote = srandom.randint(-2,0) < opinion < srandom.randint(0, 4)
        return self.opinion > self.threshold
    
    def didvote(self, issue):
        'simulates voter suppression or voter apathy'
        # what about politicians? why wouldn't one vote? hates the vote even though it is good for public?
        self.opinion = self.getOpinionOn(issue) 
        return not srandom.randint(-10,0) < self.opinion < srandom.randint(1, 10)

class GovernmentProgram:
    def __init__(self, name, topic, fund, t=None):
        'a gov program, possibly more than 1 per topic'
        self.name = name
        self.topic = topic
        self.annualFund = fund
        self.outrageThreshold = t if t else srandom.randint(10, 70)

    def changeFunding(self, amount):
        if amount < 0:
            self.cutFunding(-amount)
        else:
            self.addFunding(amount)
    
    def addFunding(self, amount):
        # if people love this above a threshold, boost productivity, political capital?
        self.annualFund += amount

    def cutFunding(self, amount):
        if self.annualFund < amount:  # can't cut more than current funding
            raise ValueError('hey man, you cant be cutting more than allocated' + self.topic + '.' +self.name)
        else:
            self.annualFund -= amount
        if (amount * 100) / self.annualFund > self.outrageThreshold:  # cutting more than
            print 'start a public outcry!!'
    
    def DoStuff(self):
        'event tick per turn, what does this program do??'

class Democracy:
    'represents 1 layer of democracy, ie: public/poltician, politician/bill'
    def __init__(self, name, pop, public=True):
        self.name = name
        self.numPop = pop
        self.pop = [Issue() for i in xrange(numPop)]
        self.bill = None

    def newBill(self):
        numTopics = srandom.randint(1,len(issueTopics)/4)
        #contents = {srandom.choice(issueTopics):srandom.randint(-10, 10) for i in xrange(numTopics)}
        contents = {}
        for i in xrange(numTopics):
            randtopic = srandom.choice(issueTopics)
            while randtopic in contents.keys():
                randtopic = srandom.choice(issueTopics)
            # need to start with fiscal impact, then translate that to voter pref impact

            # currently calculates preference or impact to voter pref
            b = itbounds[randtopic]
            contents[randtopic] = srandom.randint(-10, 10)  # b[0], b[1])
        self.bill = Issue(contents)
        self.billPassed = False
        print self.name, ' bill: ', self.bill.topics

    def countVote(self, didVote):
        if didVote:
            self.numvoted += 1
        return didVote

    def voteBill(self):
        self.numvoted = 0
        votes = sum( cit.vote(self.bill) for cit in self.pop if self.countVote(cit.didvote(self.bill))) 
        # for each topic, 
        #   for each cit
        #       sum cit.topics[topic]
        prefs = {topic:sum(cit.topics[topic] for cit in self.pop)/float(len(self.pop)) for topic in self.bill.topics }
        opinion = sum(cit.opinion for cit in self.pop) / float(len(self.pop))
        print 'avg pref: ', prefs, ' avg opinion: ', opinion
        print 'votes on bill ', votes, ' out of ', self.numvoted, ': ', votes/float(self.numvoted)
        if public:
            self.billPassed = votes * 2 >= self.numVoted
        else:
            self.billPassed = votes * 2 >= numPop

    def enactBill(self):
        if not self.billPassed:
            print 'bill not passed, bill not put into effect'
            return
        for topic in self.bill.topics:
            # take available funding for this quarter and divy up across topics, but also remove a proportional amount from existing topic if needed
            # what happens if funding to remove from topic is more than current funding?
            # education -4
            # 


if __name__ == '__main__':
    srandom = random.SystemRandom()
    numPop = 100
    usa = Democracy('usa', numPop)
    usa.newBill()
    usa.voteBill()
    usa.enactBill()
 
