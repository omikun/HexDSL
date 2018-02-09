import random


class Issue:
    def __init__(self, kv=None):
        random.seed(random.randint(0, 10000))
        self.topics = {}
        if kv:
            # self.topics = dict.fromkeys(self.topics, 0)  # reset entries to 0
            for k, v in kv.items():
                self.topics[k] = v
        else:
            self.topics['security']    = random.randint(-100, 100)
            self.topics['immigration'] = random.randint(-100, 100)
            self.topics['jobs']        = random.randint(-100, 100)
            self.topics['education']   = random.randint(-100, 100)
            self.topics['healthcare']  = random.randint(-100, 100)
            self.topics['tax']         = random.randint(-100, 100)
            self.topics['manufacture'] = random.randint(-100, 100)
            self.topics['tech']        = random.randint(-100, 100)


    def getOpinionOf(self, issue):
        s = sum(self.topics[k] * v for k, v in issue.topics.items())
        l = len(issue.topics)
        return s / float(l)


class Democracy:
    def __init__(self, i):
        self.s = i

if __name__ == '__main__':
    cit1 = Issue()
    cit2 = Issue()
    bill = Issue({'tax': 1, 'immigration': 5})
    print bill.topics
    print cit1.topics
    print sum(cit1.topics.values())
    print cit1.getOpinionOf(bill)

    print cit2.topics
    print sum(cit2.topics.values())
    print cit2.getOpinionOf(bill)
