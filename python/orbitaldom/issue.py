'just the class Issue, with politics and stuff'
from common import srandom, itbounds


class Issue(object):
    'for/against of issues in a bill, a person, an official, or even government'
    def __init__(self, itb=itbounds, kv=None):
        self.topics = {}
        self.threshold = 0  # could be tweaked based on hate against gov
        if kv:
            # self.topics = dict.fromkeys(self.topics, 0)  # reset entries to 0
            for k, v in kv.items():
                self.topics[k] = v
        else:
            for topic, b in itb.items():
                self.topics[topic] = srandom.randint(b[0], b[1])
                # TODO: try numpy bimodal distribution (some how? multivariate? mix normal?)
                # or just make up my own distribution with this:
                # np.random.choice(ny.arange(1, 7), p=[0.1, 0.05, 0.05, 0.2, 0.4, 0.2])
            return

    def __repr__(self):
        return 'threshold: ' + str(self.threshold) + ' ' + str(self.topics)

    def getOpinionOn(self, issue):
        s = sum(self.topics[k] * v for k, v in issue.topics.items())
        l = len(issue.topics)
        return s / float(l)

    def vote(self, issue):
        'returns if opinion over threshold to vote for issue'
        # opinion from -100 to 100 against to for
        # NOTE: didvote must be called first!
        return self.opinion > self.threshold
    
    def didvote(self, issue):
        'simulates voter suppression or voter apathy'
        self.opinion = self.getOpinionOn(issue) 
        return not srandom.randint(-10, 0) < self.opinion < srandom.randint(1, 10)


class Citizen(Issue):
    'a citizen is the atomic unit of a democracy'
    def __init__(self, itb=itbounds, kv=None, public=True):
        super(Citizen, self).__init__(itb, kv)  # Issue.__init__(self)
        self.public = public
        self.productivity = srandom.randint(1, 10)
        self.health = srandom.randint(4, 10)
        self.belly = srandom.randint(0, 10)  # == 1 - hunger
        self.privacy = srandom.randint(0, 10)  # 10 cares a lot about privacy
        self.wealth = srandom.randint(0, 1000)
        self.income = srandom.randint(0, 140)  # $71k average income
        # todo retirees...
        self.wealth = srandom.randint(0, 10)  
    
    def vote(self, issue):
        return self.opinion > self.threshold

    def didVote(self, issue):
        self.opinion = self.getOpinionOn(issue) 
        if self.public:
            return not srandom.randint(-10, 0) < self.opinion < srandom.randint(1, 10)
        return True  # non public, ie senators, must always vote


if __name__ == '__main__':
    issue = Issue()
    citizen = Issue()
    print 'issue:', issue
    print 'citizen', citizen
    print 'did vote?', citizen.didvote(issue)
    print 'vote: ', citizen.vote(issue)
    print 'opinion: ', citizen.opinion