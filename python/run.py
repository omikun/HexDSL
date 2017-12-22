from rule import *
import parser
import yaml
from player import *

if __name__ == '__main__':
    ruleBolster = 'bolster: if pay 2 coin blocked 2 slot then gain 1 resource and ( gain 1 resource or gain 1 heart ) endif'
    ruleItems = 'item: coin, heart, oil, food, metal, wood'
    ruleResource = 'resource: oil, food, metal, wood'
    rulePlayerSetup = """player: 
        name: Rusviet
        heart: 2
        coin: 3
        power: 4 
        mechs: 
            - walk on water
            - any tile to lake and lake to any tile
            - 1 more move
            - no workerscare"""
    #items
    ruleName, ast = parser.parse(ruleItems)
    #rules
    ruleName, ast = parser.parse(ruleBolster)
    rules[ruleName] = ast
    ast.printMe(0)
    #players
    pd = yaml.load(rulePlayerSetup)
    player1 = player(pd['player']['name'], pd)
