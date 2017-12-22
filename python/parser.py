#! /home/apps/python_org/2.7.6/bin/python
import rule
from rule import ASTNode
'Board Game Description Language'

def tokenize(rule):
    bigTokens = rule.split(':')
    if (len(bigTokens) > 2):
        print "ERROR - more than 2 things from :"
    ruleName = bigTokens[0]
    tokens = bigTokens[1].strip().split(' ')
    return ruleName, tokens
    
def parse(rule):
    name, tokens = tokenize(rule)
    it = iter(tokens)
    ast = None
    if name == "item":
        ast = parseItems(it)
    else:
        ast = parseExpression(it)
    return name, ast
    #return it

def parseItems(it):
    try:
        while True:
            token = it.next()
            rule.items[token] = []
    except StopIteration:
        pass
    return

def parseIfThen(it):
    ifNode = ASTNode("if")
    thenNode = ASTNode("then")
    ifNode.left = parseExpression(it, "then")
    ifNode.right = thenNode
    thenNode.left = parseExpression(it, "endif")
    #TODO how to handle optional else case?
    return ifNode

def parseVerb(token, it):
    node = ASTNode(token)
    node.amount = int(it.next())
    node.kind = it.next()
    return node

def parseExpression(it, endMarker="eol"):
    print "Parsing expression: " 
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
                print "got an if"
                localNode = parseIfThen(it)
                ops.append(localNode)
            elif token == "(":
                print "got a ("
                localNode = parseExpression(it, ")")
                outputs.append(localNode)
            elif rule.operators.__contains__(token):
                print "operator ", token
                localNode = ASTNode(token) 
                ops.append(localNode)
            elif rule.verbs.__contains__(token):
                print "verb: ", token
                localNode = parseVerb(token, it)
                if prevWasVerb == True:
                    lastVerb.left = localNode
                lastVerb = localNode
                outputs.append(localNode)
            else:
                print "noun: ", token
                outputs.append(ASTNode(token))

            prevWasVerb = rule.verbs.__contains__(token)

            if localRoot == None:
                localRoot = localNode
                
            token = it.next()
    except StopIteration:
        pass
    print "outputs collected: " 
    for output in outputs:
        print output.action, ", "
    print "operations collected: " 
    for o in ops:
        print o.action, ", "

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
