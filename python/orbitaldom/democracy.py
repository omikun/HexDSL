from common import *
from issue import Issue, Citizen


class Democracy:
    'a population voting on bills that affects their preferences'
    # TODO reduce number of 100% votes...
    def __init__(self, name, pop, public=True):
        self.name = name
        self.numpop = pop  # number of peeps voting for bills
        self.topics = itbounds
        self.pop = [Citizen(itb=itbounds, public=public) for i in xrange(pop)]
        self.bill = None  # dict{ program: value change, }
        self.public = public

    def __repr__(self):
        return str(self.getPulse())

    def newBill(self, details=None):
        if details:
            self.bill = details
            return
        numTopics = srandom.randint(1, len(issueTopics)/4)
        # contents = {srandom.choice(issueTopics):srandom.randint(-10, 10) for i in xrange(numTopics)}
        contents = {}
        for i in xrange(numTopics):
            randtopic = srandom.choice(issueTopics)
            while randtopic in contents.keys():
                randtopic = srandom.choice(issueTopics)
            # need to start with fiscal impact, then translate that to voter pref impact

            # currently calculates preference or impact to voter pref
            b = itbounds[randtopic]
            contents[randtopic] = srandom.randint(-10, 10)  # b[0], b[1])
        self.bill = Issue(kv=contents)
        self.billPassed = False
        print self.name, ' bill: ', self.bill.topics

    def countVote(self, didVote):
        if didVote:
            self.numvoted += 1
        return didVote

    def getPulse(self, topics=None):
        if not topics:
            topics = self.topics
        prefs = {}
        for t in topics:
            tmin = min(cit.topics[t] for cit in self.pop)
            tmax = max(cit.topics[t] for cit in self.pop)
            tavg = sum(cit.topics[t] for cit in self.pop)/float(len(self.pop))
            prefs[t] = [tavg, tmin, tmax]
        return prefs

    def voteBill(self, bill=None):
        'takes a poll of how many in democracy population would and does vote for bill'
        if bill:
            self.bill = bill
        self.numvoted = 0
        votes = sum(cit.vote(self.bill) for cit in self.pop if self.countVote(cit.didvote(self.bill))) 
        # prefs = {topic:sum(cit.topics[topic] 
        #           for cit in self.pop)/float(len(self.pop)) 
        #               for topic in self.bill.topics }
        prefs = self.getPulse(self.bill)
        opinion = sum(cit.opinion for cit in self.pop) / float(len(self.pop))
        print 'avg pref: ', prefs, ' avg opinion: ', opinion
        print 'votes on bill ', votes, ' out of ', self.numvoted, ': ', votes/float(self.numvoted)
        billPassed = None
        if self.public:
            billPassed = votes * 2 >= self.numvoted
        else:
            billPassed = votes * 2 >= self.numpop
        return billPassed

if __name__ == '__main__':
    numPop = 100
    usa = Democracy('usa', numPop, public=False)
    usa.newBill()
    for i in xrange(10):
        usa.voteBill()
