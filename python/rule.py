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
    def printSelf(self):
        print "node: ", self.action, self.amount, self.kind

    def getStr(self):
        return "%s %s %s" % (self.action , str(self.amount) , self.kind)
        
    def printMe(self, depth):
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


