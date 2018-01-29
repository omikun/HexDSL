'defines Abstract Syntax Tree class, data structure to represent rules'
from common import *

# global arrays to be used by game
rules = {}
items = {}
alias = {}


def printAST(name):
    rules[name].printMe(0)
    return


# operators are separate from verbs
# operators affect AST
# verbs are all the same, but have different impact when executed
operators = ["+", "-", "and", "or", ">", ">=", "<", "<="]
verbs = ["pay", "gain", "add", "subtract", "block", "unblock", "spawn"]


class ASTNode(object):
    def __init__(self, name):
        self.action = name
        self.left = None
        self.right = None
        self.amount = 0
        self.kind = ""

    def getMatchingNode(self, tokens_, t, top=False):
        self.getMatchingNodes(tokens_, t, top)
        key = tokens_[0]
        print key, t
        ret = havePlayerSelect(t[key])
        t[key] = [ret]
        return ret

    def getMatchingNodes(self, tokens_, t, top=False):
        'find matching nodes in cur tree to token list, add matches to dict t'
        # top means first level with no match or first token match
        if len(tokens_) == 0 or tokens_[0] == 'amount':
            print 'match found!?!?!'
            return True
        print 'getNodeList: ', self
        newtokens = tokens_
        match, lastMatch = False, False
        if self.action == tokens_[0] or self.action in verbs:
            match = True
            lastMatch = len(tokens_) == 2 and tokens_[-1] == 'amount'
            newtokens = tokens_[1:]
            print 'partial match found! ', self.action, ' new tokens_: ', newtokens
        nexttop = top and not match
        lret, rret = None, None
        if self.left:
            lret = self.left.getMatchingNodes(newtokens, t, top=nexttop)
        if self.right:
            rret = self.right.getMatchingNodes(newtokens, t, top=nexttop)
        if match and (lastMatch or lret or rret):
            if top:
                print 'adding to t: ', self
                t.setdefault(tokens_[0], []).append(self)
            return True
        return False


    def getNodesWithChild(self, a):
        'return list of nodes with a child of action a, assumes no nesting'
        if self is None:
            return False
        ret = []
        lret, rret = None, None
        if self.action == a:
            return True
        if self.left:
            lret = self.left.getNodesWithChild(a)
        if self.right:
            rret = self.right.getNodesWithChild(a)
        if lret or rret:
            return self
        if lret and lret:
            ret.append(lret)
        if rret and rret:
            ret.append(rret)
        return ret

    def getNodes(self, a):
        'return list of nodes with action a, returns can nest'
        if self is None:
            return None
        ret = []
        if self.action == a:
            ret.append(self)
        if self.left:
            lret = self.left.getNodes(a)
            if lret:
                ret.append(lret)
        if self.right:
            rret = self.right.getNodes(a)
            if rret:
                ret.append(rret)
        return ret

    def printSelf(self):
        print "node: ", self.action, self.amount, self.kind

    def __repr__(self):
        return "%s %s %s" % (self.action, str(self.amount), self.kind)

    def printMe(self, depth=0):
        "print sub tree with self as root"
        if self is None:
            return
        print self,
        if self.left is not None:
            print "\t->L", depth, " ",
            self.left.printMe(depth + 1)
        if self.right is None:
            return
        tabs = "\t"
        for i in xrange(depth):
            tabs = tabs + "\t"

        print ""
        print tabs, "->R", depth, " ",
        self.right.printMe(depth + 1)


if __name__ == '__main__':
    a = ASTNode('or')
    a.left = ASTNode('pay')
    a.left.left = ASTNode('blockable')
    a.right = ASTNode('gain')
    a.right.left = ASTNode('blockable')
    l = a.getNodesWithChild('blockable')
    for i, c in enumerate(l):
        print i,
        c.printMe()
        print ''
