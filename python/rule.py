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

    def getMatchingRoot(self, tokens_, t, top=False):
        self.getMatchingRoots(tokens_, t, top)
        key = tokens_[0]
        print key, t
        ret = havePlayerSelect(t[key])
        t[key] = [ret]
        return ret

    def getSubTreeNode(self, tokens, p):
        'travels down tree and returns last node matching token list'
        # only supports 1 match
        # although currently, 1/28/18, only need to go down left sides
        # for verb.blockable.amount, operate on trade.left.amount,
        # assuming trade.left.action=='blockable
        print 'getRec: ', self, tokens, self.action == tokens[0]
        if tokens == []:
            print 'getRec: reached end'
            return None
        # TODO what if verb means rules as well? want to modify ex. block 2
        # topRow???
        if self.action == tokens[0] or (tokens[0] == 'verb' and self.action in verbs):
            print 'getRec: found a match', self.action
            if (len(tokens) == 2 and tokens[1] == 'amount') or len(tokens) == 1:
                return self
            if self.left:
                ret = self.left.getSubTreeNode(tokens[1:], p)
                if ret:
                    return ret
            if self.right:
                ret = self.right.getSubTreeNode(tokens[1:], p)
                if ret:
                    return ret
        print 'getRec: nothing worked??', self
        return None

    def getMatchingRoots(self, tokens_, t, top=False):
        'find matching nodes in cur tree to token list, adds root matches to t'
        # supports multiple matches!
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
            print 'partial match ', self.action, ' new tokens_: ', newtokens
        nexttop = top and not match
        lret, rret = None, None
        if self.left:
            lret = self.left.getMatchingRoots(newtokens, t, top=nexttop)
        if self.right:
            rret = self.right.getMatchingRoots(newtokens, t, top=nexttop)
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
