#! /home/apps/python_org/2.7.6/bin/python
import rule
from rule import ASTNode
'Board Game Description Language'

def tokenize(rule):
    "takes rule string and convert to list of tokens"
    bigTokens = rule.split(':')
    if (len(bigTokens) > 2):
        print "ERROR - more than 2 things from :"
    ruleName = bigTokens[0]
    tokens = bigTokens[1].strip().replace(',', "").split(' ')
    return ruleName, tokens
    
def parse(rule):
    "tokenize, then parseExpression"
    name, tokens = tokenize(rule)
    print "parsing ", name
    print tokens
    it = iter(tokens)
    ast = parseExpression(it)
    return name, ast
    #return it

def parseItems(inputRule):
    "for parsing items and aliases only"
    name, tokens = tokenize(inputRule)
    it = iter(tokens)
    ast = None
    if name == "item":
        try:
            while True:
                token = it.next()
                rule.items[token] = []
        except StopIteration:
            pass
    else: #alias
        l = []
        try:
            while True:
                token = it.next()
                l.append(token)
        except StopIteration:
            pass
        rule.alias[name] = l

    return

def parseIfThen(it):
    #if ->L condition
    #   ->R then    ->L execute if condition == True
    #               ->R None
    #TODO need to be able to differentiate between if then and if then else, 
    #otherwise just stick with if then
    ifNode = ASTNode("if")
    thenNode = ASTNode("then")
    ifNode.left = parseExpression(it, "then")
    ifNode.right = thenNode
    thenNode.left = parseExpression(it, "endif")
    #TODO how to handle optional else case?
    return ifNode

def parseVerb(token, it):
    #verbs are always defined as verb amount kind; eg. pay 2 coin
    node = ASTNode(token)
    node.amount = int(it.next())
    node.kind = it.next()
    return node

def parseExpression(it, endMarker="eol"):
    "recursive parser, returns when endMarker is encountered"
    #expressions operator expressions
    #if ... then ... endif
    #verb number kind
    
    outputs = []
    ops = []
    localNode = None
    localRoot = None
    lastVerb = None
    prevWasVerb = False
    try:
        token = it.next()
        while token != endMarker:
            if token == "if":
                localNode = parseIfThen(it)
                ops.append(localNode)
            elif token == "(":
                localNode = parseExpression(it, ")")
                outputs.append(localNode)
            elif rule.operators.__contains__(token):
                localNode = ASTNode(token) 
                ops.append(localNode)
            elif rule.verbs.__contains__(token):
                localNode = parseVerb(token, it)
                if prevWasVerb == True:
                    lastVerb.left = localNode
                lastVerb = localNode
                outputs.append(localNode)
            elif token == "ask": #TODO maybe don't need this?
                localNode = ASTNode(token)
                localNode.left = parseExpression(it, "endask")
                ops.append(localNode)
            else:
                outputs.append(ASTNode(token))

            prevWasVerb = rule.verbs.__contains__(token)

            if localRoot == None:
                localRoot = localNode
                
            token = it.next()
    except StopIteration:
        pass

    #shunt-yard algorithm, check wiki; 
    # pop both queues, op.right = output, op.left = next op
    if len(ops) > 0:
        localRoot = ops[-1]
        prevNode = None
        while (len(ops) > 0):
            node = ops.pop()
            if (prevNode != None):
                prevNode.left = node
            if len(outputs) > 0:
                node.right = outputs.pop()
            prevNode = node
    
        if len(outputs) > 0:
            prevNode.left = outputs.pop()
    return localRoot

if __name__ == '__main__':
    #TODO get rid of endif unless there's nested ifs
    ruleBolster = 'bolster: if pay 2 coin blocked 2 slot then gain 1 resource and ( gain 1 resource or gain 1 heart ) endif'
    ruleName, ast = parse(ruleBolster)
    rule.rules[ruleName] = ast
    ast.printMe(0)
