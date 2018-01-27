last qualifier (ex. verb.blockable->blockable)
        
    elif r.action in p or r.action in verbs:
        print 'rexec action in player rule'
        cond = operate(p, r)
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


#check if player has right kind, if not, check alias and ask user for kind
def operate(p, n):
    'modify a player resource, player[n.kind]'
    kind = n.kind
    print 'operating node: ', n.printMe()
    #print "Executing: ", n.action, n.amount, n.kind
    while kind not in p:
        if n.kind in alias:
            print alias[n.kind]
        kind = raw_input("Enter "+ n.kind+": ")
    #metaverb: block 1 trade
    print 'you entered ', kind, ' is this a rule? ', isinstance(p[kind], ASTNode)
    if isinstance(p[kind], ASTNode): #kind refers to a rule (of type ASTNode); it's a metaVerb!
        print 'metaverb found! ', n.action
        rexec(p[n.action], p, {'targetNode': p[kind]}) #execute as a rule with a target dictionary
    if n.action == "pay":
        newAmount = p[kind] - n.amount
        if newAmount < 0:
            return False
        p[kind] = newAmount
    elif n.action == "gain":
        p[kind] = p[kind] + n.amount
    elif n.action == "block" and False:
        #remove 1 unit from a verb with attached blockable
        #find all blockable nodes in given rule
        choices = p[kind].getNodesWithChild("blockable")
        sel = ''
        s = None
        while not is_int(sel) or in_range(choices, int(sel)):
            for i, c in enumerate(choices):
                print i, 
                c.printMe()
                print ''
            sel = raw_input("Enter number: ")
            s = choices[int(sel)]
        #int(sel) is the user choice for which parent of a blockable gets to be blocked
        #choices[int(sel)]
        #s is the node with an attached blockable
        if s.left.amount > 0 and s.amount > 0:
            s.amount -= 1
            s.left.amount -= 1
    elif n.action == "unblock":
        print "TODO: implement unblock"
    else:
        print 'Unrecognized verb'

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
            if verb.blockable.amount > 1 then 
                subtract 1 verb.amount and subtract 1 verb.blockable.amount
            endif
        unblock:
            if verb.blocked.amount > 1 then
                add 1 verb.amount and subtract 1 verb.blockable.amount
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
        botRow: upgrade, deploy, build, enlist
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

    r = rules['test'] #global rules
    #r = player1['trade'] #per player rule
    #execRule(r, player1)

    aliases = formatMat(actionAliases)
    for a in aliases:
        print 'adding ', a
        hexparser.parseItems(a)
    parsePlayerMat(playerMat1, player1)
    r = player1['upgrade'] #global rules
    player1['block'].printMe()
    execRule(r, player1)
