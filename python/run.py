from rule import *
import hexparser
import yaml
from player import *

reload(hexparser)
def execRule(ruleName, p):
    #walk down ast
    r = rules[ruleName]
    if rexec(r, p) == False:
        print "Could not execute rule"
    else:
        print "Executed rule ", ruleName

def rexec(r, p):
    if r == None:
        return False
    if r.action == "if":
        cond = rexec(r.left, p)
        if cond == True:
            rexec(r.right, p)
    elif verbs.__contains__(r.action):
        cond = operate(p, r)
        return cond
    elif r.action == "or":
        #print list of options with numbers
        #recursively go left then right with number for each
        num = [0]
        l = []
        output = printOptions(r, num, l)
        print output
        inputNum = int(raw_input("Enter num:"))-1
        l[inputNum].printMe(0)
        print ""
        num = [0]
        rexec(l[inputNum], p)
    else:
        rexec(r.left, p)
        rexec(r.right, p)

def runOption(r, p, runNum, num):
    if r == None:
        return
    num[0] = num[0] +1
    if runNum == num[0]:
        rexec(r, p)
        return
    runOption(r.left, p, runNum, num)
    runOption(r.right, p, runNum, num)

# a or b and c
# 1. a
# 2. b and c
# (a and b ) or (c and d or e)
# or ->L and ->L a
#            ->R b
#    ->R and ->L c
#            ->R or ->L d
#                   ->R e
# 1. a and b
# 2. c and 
#   3. d
#   4. e
#r=rule, num=depth, 
#l=list of nodes corresponding to option number in ret
def printOptions(r, num, l, prevIsOr=True):
    if r == None:
        return ""
    ret = ""

    #ONLY increment num if
    #1. self is or
    #2. children is NOT or
    #3. parent is or
    print num[0], r.getStr(), "prevIsOr ", prevIsOr
    hasBeenOr = r.action == "or" and prevIsOr == True
    if prevIsOr and r.action != "or":
        num[0] += 1
        ret += "\n" + str(num[1]) + ": "
        print "+1 then self"
        l.append(r)

    if operators.__contains__(r.action):
        ret += printOptions(r.left, num, l, hasBeenOr)

        if r.action != "or":
            ret += " %s " % r.action

        ret += printOptions(r.right, num, l, hasBeenOr)
    else:
        ret += r.getStr()

    return ret


#check if player has right kind, if not, check alias and ask user for kind
def operate(p, n):
    kind = n.kind
    print n.action, n.amount, n.kind
    while not p.__contains__(kind):
        if alias.__contains__(kind):
            print alias[n.kind]
        kind = raw_input("Enter "+ n.kind+": ")

    if n.action == "pay":
        newAmount = p[kind] - n.amount
        if newAmount < 0:
            return False
        p[kind] = newAmount
    elif n.action == "gain":
        p[kind] = p[kind] + n.amount
    return True

#main idea: simulate a turn based game
#   
#setup board game rules,
#   items: list of known items ()
#   aliases: (resource = wood, food, etc)
#   players: init resources; player specific tweaks to rules
#setup player setup rules
#roundrobin execute player/rules, 
#   go to next player, 
#   check winning condition after each action

if __name__ == '__main__':
    ruleBolster = 'bolster: if pay 2 coin blocked 2 slot then gain 1 resource or ( gain 1 resource and gain 1 heart ) endif'
    ruleTest = 'test: if pay 2 coin blocked 2 slot then gain 4 resource or ( gain 1 resource and ( gain 1 heart or gain 1 power ) ) or gain 2 heart endif'
    ruleItems = 'item: coin, heart, oil, food, metal, wood'
    ruleResource = 'resource: oil, food, metal, wood'
    rulePlayerSetup = """Rusviet:
        heart: 2
        coin: 3
        power: 4 
        wood: 0
        oil: 0
        food: 0
        metal: 0
        mechs: 
            - walk on water
            - any tile to lake and lake to any tile
            - 1 more move
            - no workerscare
        move: gain 1 move
        """
    #items
    ruleName = hexparser.parseItems(ruleItems)
    hexparser.parseItems(ruleResource)
    #rules
    ruleName, ast = hexparser.parse(ruleBolster)
    rules[ruleName] = ast
    ast.printMe(0)
    ruleName, ast = hexparser.parse(ruleTest)
    rules[ruleName] = ast
    #players
    player1 = yaml.load(rulePlayerSetup)['Rusviet']
    execRule('test', player1)
