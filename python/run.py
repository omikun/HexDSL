#this script demonstrates proof of concept functionalities:
# - contains rules and setup info
# - calls to hexparser to build abstract syntax trees (AST)
# - puts ASTs into rules list
# - initializes player stats
# - executes rules for given player
import sys, os
from rule import *
import hexparser
import yaml
from player import *
from playerMat import *
reload(hexparser)

#common
# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

#grabs rule from rule list and executes
def execRule(r, p):
    #walk down ast
    if rexec(r, p) == False:
        print "Could not execute rule"
    else:
        print "Executed rule ", ruleName

#tokens = [token for token in tokens if token is not 'amount']
#algorithm: in t['targetRule'], get list of all nodes that fits this set of token specifications
#ex. verb.blocked.amount -> look for a verb->blocked pattern
#idea: return only top matching node (verb in verb.blockable.amount)
#       and let accessor go back and find verb.blockable in simple tree iterator
#idea2: get last matching node (blockable in verb.blockable.amount) and 
#       accessor directly 
#idea1 allows easy showing of what is getting changed if needed (complete verb.blockable)
#top firstMatch
#false false - no matches
#false true  - matched but no longer first, only return a matched has occur
#true  false - no matches, recur call with top=True
#true  true  - first match, if rest matches, add matched node to dict, recur call with top=false
#nextTop = top and not match
def getNodeList(cur, tokens_, t, top=False):
    'find matching nodes in cur tree to token list, add matches to dict t'
    #top means first level with no match or first token match
    if len(tokens_) == 0 or tokens_[0] == 'amount':
        print 'match found!?!?!'
        return True
    if cur == None:
        return False
    print 'getNodeList: ', cur
    newTokens = tokens_
    match = False
    if cur.action == tokens_[0] or cur.action in verbs:
        match = True
        newTokens = tokens_[1:]
        print 'partial match found! ', cur.action, ' new tokens_: ', newTokens
    nexttop = top and not match
    lret = getNodeList(cur.left, newTokens, t, top=nexttop)
    rret = getNodeList(cur.right, newTokens, t, top=nexttop)
    if match and (lret or rret):
        if top:
            t.setdefault(tokens_[0], []).append(cur)
        return True
    return False

def havePlayerSelect(l):
    'given a list, ask player to choose a valid selection and return that element'
    if not l or len(l) == 0:
        raise ValueError('not a valid list for player to choose from')
    if len(l) == 1:
        print 'only 1 choice: ', l[0]
        return l[0]
    choice = 'not a valid choice'
    for i, n in enumerate(l):
        print "%d. %s" % (i+1, n)
    while not is_int(choice) or not (1 <= int(choice) <= len(l)):
        choice = raw_input('Enter choice: ')
    return l[int(choice)-1]

#recursive execution over AST
#when a choice is encountered, present choices to player and ask for input
#AST has 2 points: left, right; always execute left then right
#1/18/18: currently only supports if A then B; no else or finally
#   if you need else/finally, wrap it up with an or/and and ()
#   ex. instead of: if a then b else c finally d
#          do this: (if a then b) and (if not a then c) and d
def rexec(r, p, t=None):
    if r == None:
        return
    print '~rexec: ', r.printMe()

    if t:
        print t
    if r.action == "if":
        cond = rexec(r.left, p, t)
        print 'rexec if cond: ', cond
        if cond == True:
            rexec(r.right, p, t)
    elif '.' in r.action: #metaVerb, should go into operate()
        #this node just returns a value, will not be operated on... ex if verb.amount > 1
        #verb.amount is this node
        print 'rexec has a .', t
        if t == None:
            raise ValueError("oh crap this isn't suppose to happen! t should be something!")
        #tokens = filter(lambda x: x != 'amount', r.action.split('.')) 
        tokens = r.action.split('.')
        print 'trying to match ', tokens
        root = t['targetNode']
        root.printMe()
        getNodeList(root, tokens, t, top=True)
        #if t has many nodes, ask user to decide
        #after choice made, go down and get amount if amount in action
        print t
        for k,v in t.items():
            print 'dict:', k,v
        key = tokens[0] 
        print 'printing key, tokens: ', key, tokens
        ret = havePlayerSelect(t[key])
        t[key] = [ret] #replace array of possible nodes with user selected
        if 'amount' in r.action and ret:
            return getRecursiveDictLookUp(ret, tokens, p).amount #last qualifier (ex. verb.blockable->blockable)
        else:
            print 'something wrong: ', r.action, ret
        
    elif r.action in p or r.action in verbs:
        print 'rexec action in player rule'
        cond = operate(p, r, t)
        return cond
    elif r.action == ">":
        print 'rexecing on >, passing t down'
        ret = rexec(r.left, p, t) > rexec(r.right, p, t)
        print 'result of rexec >: ', ret
        return ret
    elif is_int(r.action):
        print 'rexecing an int', r.action
        return int(r.action)
    elif r.action == "or":
        print 'rexec or'
        num = [0] #numbering
        l = [] #options
        output = printOptions(r, num, l)
        print output
        inputNum = int(raw_input("Enter num:"))-1

        print "Executing sub expression: ",
        l[inputNum].printMe(0)
        print ""
        num = [0]
        rexec(l[inputNum], p, t)
    else: # if r.action == "and":
        print 'rexec else'
        rexec(r.left, p, t)
        rexec(r.right, p, t)


#takes AST subtree and presents incremental option to player
#r=rule, num=depth, 
#l=list of nodes corresponding to option number in ret
# say the input text is this:
# (a and b ) or (c and d or e)
# then the resulting AST is this: ->L is left link, ->R is right link,
# head is at the far left (or in this case)
# or ->L and ->L a
#            ->R b
#    ->R and ->L c
#            ->R or ->L d
#                   ->R e
# and printOption will print this:
# 1. a and b
# 2. c and d or e
# if player chooses 2, it will execute c and print
# 1. d
# 2. e
# repeat
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

    if r.action in operators:
        ret += printOptions(r.left, num, l, hasBeenOr)

        if inc or not prevIsOr:
            ret += " %s " % r.action

        ret += printOptions(r.right, num, l, hasBeenOr)
    else:
        ret += r

    return ret

def getRecursiveDictLookUp(d, tokens, p):
    'travels down tree and operate on last node matching tokens'
    #for verb.blockable.amount, operate on trade.left.amount, 
    # assuming trade.left.action=='blockable
    print 'getRec: ', d, tokens, d.action == tokens[0]
    if tokens == [] or d is None:
        print 'getRec: reached end'
        return None
    if d.action == tokens[0] or (tokens[0] == 'verb' and d.action in verbs): #TODO what if verb means rules as well? want to modify ex. block 2 topRow???
        print 'getRec: found a match', d.action
        if (len(tokens) == 2 and tokens[1] == 'amount') or len(tokens) == 1:
            return d
        ret = getRecursiveDictLookUp(d.left, tokens[1:], p)
        if ret:
            return ret
        ret = getRecursiveDictLookUp(d.right, tokens[1:], p)
        if ret:
            return ret
    print 'getRec: nothing worked??', d
    return None

#check if player has right kind, if not, check alias and ask user for kind
def operate(p, n, t=None):
    'modify a player resource, player[n.kind]'
    #t is a dict {'verb':[ASTNode, ASTNode]}
    kind = n.kind
    print 'operating node: ', n.printMe()
    #print "Executing: ", n.action, n.amount, n.kind
    if '.' in n.kind:
        #kind refers to a particular quantity variable, not p[kind]
        #preferably could find value by getting recursive dict lookup
        tokens = n.kind.split('.')
        #operand = havePlayerSelect(t[tokens[0]]) #should only have 1 valid option
        node = getRecursiveDictLookUp(t[tokens[0]][0], tokens, p)
        if n.action == 'add':
            node.amount += n.amount
            #t[tokens[-2]][0].amount += n.amount
        if n.action == 'subtract':
            node.amount -= n.amount
            #t[tokens[-2]][0].amount -= n.amount
        return True
    while kind not in p:
        if n.kind in alias:
            print alias[n.kind]
        kind = raw_input("Enter "+ n.kind+": ")
    #metaverb: block 1 trade
    print 'you entered ', kind, ' is this a rule? ', isinstance(p[kind], ASTNode)
    if isinstance(p[kind], ASTNode): #kind refers to a rule (of type ASTNode); it's a metaVerb!
        print 'metaverb found! ', n.action
        return rexec(p[n.action], p, {'targetNode': p[kind]}) #execute as a rule with a target dictionary
    if n.action == "pay":
        newAmount = p[kind] - n.amount
        if newAmount < 0:
            return False
        p[kind] = newAmount
    elif n.action == "gain":
        p[kind] = p[kind] + n.amount
    else:
        print 'Unrecognized verb:', n

    return True

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
def in_range(l, n):
    return 0 <= n < len(l)

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
        oil: 3000
        food: 0
        metal: 0
        mechs: 
            - walk on water
            - any tile to lake and lake to any tile
            - 1 more move
            - no workerscare
        move: gain 1 move
        """
    #verbs operating on verbs
    metaVerb = '''
        block:
            if blockable then 
                remove 1 slot and remove 1 kind in parentNode
            endif
        unblock:
            if blocked then 
                remove 1 slot and add 1 kind in parentNode
            endif
        '''
    #executes when corresponding rule is executed, modifies player state conditioned on rule executed and player states
    metaRule = """
        if upgrade then
            player gain player.upgrade.recruit.kind
            adjacent.player gain adjacent.player.upgrade.recruit
        endif
    """
    #rules specific to a particular player (assigned on setup, can be randomized and/or player choose)
    playerMat1 = """
        trade: 
            if pay 3 coin blockable 2 slot then 
                ( gain 2 resource blocked 2 slot or 1 heart blocked 1 slot ) and gain 0 power blocked 1 slot 
            endif 
        bolster: 
            if pay 2 coin then 
                ( gain 2 power blocked 1 slot or gain 1 combatCard blocked 1 slot ) and gain 1 heart 
            endif
        use: move 2 units max 1 tile or gain 1 coin blocked 1 slot endif
        produce: 
            if pay 4 coin blocked 3 slot then 
                gain 2 worker.position.tile.resource blocked 1 slot 
            endif
        block:
            if verb.blockable.amount > 0 then 
                subtract 1 verb.amount and subtract 1 verb.blockable.amount
            endif
        unblock:
            if verb.blocked.amount > 0 then
                add 1 verb.amount and subtract 1 verb.blocked.amount
            endif
        upgrade:
            if pay 3 oil blockable 1 slot then 
                block 1 topRow and unblock 1 botRow
            endif
        deploy:
            if pay 2 wood blockable 1 slot then
                spawn 1 mech at worker.position
            endif
        build:
            if pay 3 iron blockable 1 slot then
                spawn 1 building at worker.position
            endif
        enlist:
            if pay 3 food blockable 2 slot then
                oncePerGame gain 1 power and gain 1 recruit.power
                oncePerGame gain 1 power and gain 1 recruit.power
            endif
        """
    actionAliases = """
        col1: trade, upgrade
        col2: bolster, deploy
        col3: use, build
        col4: produce, enlist
        action: col1, col2, col3, col4
        topRow: trade, bolster, use, produce
        botRow: upgrade, deploy, build, enlist, bolster
        """
    #items
    ruleName = hexparser.parseItems(ruleItems)
    hexparser.parseItems(ruleResource)
    #rules
    #ruleName, ast = hexparser.parse(ruleBolster)
    #rules[ruleName] = ast
    #ast.printMe(0)
    #ruleName, ast = hexparser.parse(ruleTest)
    #rules[ruleName] = ast
    #players
    player1 = yaml.load(rulePlayerSetup)['Rusviet']

    #r = rules['test'] #global rules
    #r = player1['trade'] #per player rule
    #execRule(r, player1)
    playerBolster = '''
        bolster: 
            if pay 2 coin then 
                ( gain 2 power blocked 1 slot or gain 1 combatCard blocked 1 slot ) and gain 1 heart 
            endif
            '''
    aliases = formatMat(actionAliases)
    for a in aliases:
        print 'adding ', a
        hexparser.parseItems(a)
    #parsePlayerMat(playerBolster, player1)
    parsePlayerMat(playerMat1, player1)
    r = player1['upgrade'] #global rules
    player1['block'].printMe()

    print 'bolster: '
    player1['bolster'].printMe()
    print ''
    #blockPrint()
    execRule(r, player1)
    #enablePrint()
    print 'trade: '
    player1['trade'].printMe()
    print ''
    print 'bolster: '
    player1['bolster'].printMe()