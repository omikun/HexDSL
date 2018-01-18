#this script demonstrates proof of concept functionalities:
# - contains rules and setup info
# - calls to hexparser to build abstract syntax trees (AST)
# - puts ASTs into rules list
# - initializes player stats
# - executes rules for given player

from rule import *
import hexparser
import yaml
from player import *

reload(hexparser)

#grabs rule from rule list and executes
def execRule(ruleName, p):
    #walk down ast
    r = rules[ruleName]
    if rexec(r, p) == False:
        print "Could not execute rule"
    else:
        print "Executed rule ", ruleName

#recursive execution over AST
#when a choice is encountered, present choices to player and ask for input
def rexec(r, p):
    if r == None:
        return
    if r.action == "if":
        cond = rexec(r.left, p)
        if cond == True:
            rexec(r.right, p)
    elif verbs.__contains__(r.action):
        cond = operate(p, r)
        return cond
    elif r.action == "or":
        num = [0] #numbering
        l = [] #options
        output = printOptions(r, num, l)
        print output
        inputNum = int(raw_input("Enter num:"))-1

        print "Executing sub expression: ",
        l[inputNum].printMe(0)
        print ""
        num = [0]
        rexec(l[inputNum], p)
    else:
        rexec(r.left, p)
        rexec(r.right, p)

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

#takes AST subtree and presents incremental option to player
def printOptions(r, num, l, prevIsOr=True):
    if r == None:
        return ""
    ret = ""

    #increment num ONLY if
    #1. all parents have been 'or'
    #2. self is NOT or
    hasBeenOr = r.action == "or" and prevIsOr == True
    inc = prevIsOr and r.action != "or"
    if inc:
        num[0] += 1
        ret += "\n" + str(num[0]) + ": "
        l.append(r)

    if operators.__contains__(r.action):
        ret += printOptions(r.left, num, l, hasBeenOr)

        if inc or not prevIsOr:
            ret += " %s " % r.action

        ret += printOptions(r.right, num, l, hasBeenOr)
    else:
        ret += r.getStr()

    return ret


#check if player has right kind, if not, check alias and ask user for kind
def operate(p, n):
    kind = n.kind
    #print "Executing: ", n.action, n.amount, n.kind
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
#   items: list of known items (kind)
#   aliases: (resource = wood, food, etc)
#   board: init board
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
    #player is a json string
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
    playerMat1 = """
        trade: 
            if pay 1 coin then 
                ( gain 2 resource or 1 heart blocked 1 slot ) and gain 0 power blocked 1 slot 
            endif 
        upgrade:
            if pay 3 oil blockable 1 slot then 
                gain 1 upgrade and ( you and nearby ) gain 0 power blocked 1 powerRecruit   
            endif
        bolster: if pay 2 coin then ( gain 2 power blocked 1 slot or gain 1 combatCard blocked 1 slot ) and gain 1 heart endif
        use: move 2 units max 1 tile or gain 1 coin blocked 1 slot endif
        produce: if pay 0 coin blocked 3 slot then gain 2 workerProducedResource blocked 1 slot endif
        col1: trade, upgrade
        col2: bolster, deploy
        col3: use, build
        col4: produce, enlist
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
