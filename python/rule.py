rules = {}
items = {}
def printAST(name):
    rules[name].printMe(0)
    return

operators = ["+", "-", "and", "or"]
verbs = ["pay", "gain", "blocked"]
class ASTNode(object):
    def __init__(self, name):
        self.action = name
        self.left = None
        self.right = None
        self.amount = 0
        self.kind = ""
    
    def printMe(self, depth):
        if self == None:
            return
        print self.action,
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


