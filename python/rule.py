#defines Abstract Syntax Tree class, data structure to represent rules

#global arrays to be used by game
rules = {}
items = {}
alias = {}

#helper function
def printAST(name):
    rules[name].printMe(0)
    return

#operators are separate from verbs
#operators affect AST
#verbs are all the same, but have different impact when executed
operators = ["+", "-", "and", "or"]
verbs = ["pay", "gain", "blocked"]
class ASTNode(object):
    def __init__(self, name):
        self.action = name
        self.left = None
        self.right = None
        self.amount = 0
        self.kind = ""

    def getNodesWithChild(self, a):
        'return list of nodes with a child of action a, assumes no nesting'
        if self == None:
            return False
        ret = []
        if self.action == a:
            return True
        if self.left:
            lret = self.left.getNodesWithChild(a)
        if self.right:
            rret = self.right.getNodesWithChild(a)
        if lret == True or rret == True:
            return self
        if lret and lret != False:
            ret.append(lret)
        if rret and rret != False:
            ret.append(rret)
        return ret

    def getNodes(self, a):
        'return list of nodes with action a, returns can nest'
        if self == None:
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

    def getStr(self):
        return "%s %s %s" % (self.action , str(self.amount) , self.kind)
        
    def printMe(self, depth=0):
        "print sub tree with self as root"
        if self == None:
            return
        print self.getStr(),
        if self.left != None:
            print "\t->L", depth, " ",
            self.left.printMe(depth+1)
        if self.right == None:
            return
        tabs = "\t"
        for i in xrange(depth):
            tabs = tabs + "\t"

        print ""
        print tabs, "->R", depth, " ",
        self.right.printMe(depth+1)


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
