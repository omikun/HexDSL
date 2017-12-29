"handles player mat setup"

from rule import *
import hexparser
import yaml
from player import *

reload(hexparser)

playerMat1 = """
        trade: 
            if pay 1 coin then 
                ( gain 2 resource or 1 heart blocked 1 slot ) and gain 0 power blocked 1 slot 
            endif 
        upgrade:
            if pay 3 oil blockable 1 slot then 
                gain 1 upgrade and ( you and nearby ) gain 0 power blocked 1 powerRecruit   
            endif
        bolster: if pay 1 coin then ( gain 2 power blocked 1 slot or gain 1 combatCard blocked 1 slot ) and gain 1 heart endif
        use: move 2 units max 1 tile or gain 1 coin blocked 1 slot endif
        produce: if pay 0 coin blocked 3 slot then gain 2 workerProducedResource blocked 1 slot endif
        col1: trade and upgrade
        col2: bolster and deploy
        col3: use and build
        col4: produce and enlist
        """

def parsePlayerMat(mat):
    #compact all lines tabs to first line w/o tabs
    pmRules = formatMat(mat)
    print pmRules
    for rule in pmRules:
        ruleName, ast = hexparser.parse(rule)
        rules[ruleName] = ast

def formatMat(mat):
    #strip new lines and extra spaces from input player mat
    tokens = [t.strip() for t in mat.split('\n')]
    #get index of all tokens at beginning of rule (those with ':')
    ruleHeads = [i for i, t in enumerate(tokens) if hasChar(t, ':')]
    ruleHeads.append(None)
    pmRules = []
    for i in xrange(len(ruleHeads)-1):
        pmRules.append(" ".join(tokens[ruleHeads[i] : ruleHeads[i+1]]))
    return pmRules

def hasChar(s, c):
    return s.find(c) >= 0
print "hello"
