# HexDSL
A programming language specifically designed for describing turn based hex-grid board games rules and simulating them.

The goal of this language is to be as straight-forward for non-programmers as possible while retaining programmable flexibility in the construction of game rules to maximize board game design space for fun and creativity.

Game loop:

    - item/resource setup
    - rule setup (acts on items)
    - player setup, player-specific rules
    - board setup
    - loop until winning condition reached
        - player execute rule
        - meta rule executed
        - rules modified as a result of player-executed-rule take into effect   
        - select next player

Game data structures are generally dictionary entires

**Rule** - global or per-player logic, composed of one or more actions stored as a tree of nodes (see AST)

**Item** - countable units per player or global (bank)

**Alias** - a word that can be player-resolved into a number of items xor rules

**Verb** - specifies action to be performed,
    
    - AST - rules are stored as a pseudo abstract syntax trees
        - each node can either be an operator or a verb
            - operators govern the structure of the tree (and, or, if, then, else)
            - verbs specifies how to modify game data
            - verbs may also modify rules themselves
        - each node has an action, an amount, and a kind
        - ex. pay 3 coin becomes a verb with action='pay' amount=3 and kind='coin'
    - data is contained globally, per player, per tile, per unit on tile, or per AST node in rule or per-player-rule.
    - each player is a dictionary that can contain items (coin, food, etc), alias, and rules
    - a verb acts on items
    - a metaVerb acts on other verbs inside a rule
    - an alias may contain all items or all rules
    - when an alias is encountered, player will resolve ambiguity with a selection

# TODO
cancel an action - a rule or verb may return true or false, but player may wish to undo action before 

dot syntax - implies hierarchy, properties
    
    1. can be dictionary lookup: ex player.coin is translated to player['coin'] internally
    2. can be tree traversal:
        - ex. verb.blocked.amount is ASTNode.left.amount IF verbs.__contains__(ASTNode.action) and IF ASTNode.left.action == 'blocked'
    - Assumes 1. if kind is an item and 2. if kind is a rule
    
metaVerb - verbs that modifies other verbs

    - metaVerbs are determined by how they are used
        - a rule that uses a metaVerb must specify a rule or a rule alias as its kind type, eg kind='trade'
    - all metaVerbs act on 1 verb inside a rule, when a rule has more than one verb, player decides
    - 

    ex. #metaVerb
        unblock: if verb.blocked.amount > 0 then verb.amount++ and verb.blocked.amount--
        #rule alias
        topRow: bolster, trade, use, 
        #rule that enacts a metaVerb on 1 unit of a verb aliased to topRow
        upgrade: unblock 1 topRow
    

metaRule - rules executed in response to player executed rules after a turn
    
    - register which rule a player just executed, then execute corresponding metaRules; beware of dependencies and metarule execution order requirements; can metaRules be dependent on other metaRules?
    - ex. if player exec upgrade then 
            for p in player.adjacent do 
                if p.upgrade.recruit then 
                    p gain 1 power 
                endif 
             endloop 
           endif

player reference 

    - player (the player of current turn)
    - adjacent.player - players physically adjacent to player of current turn
data reference

    - data in per player rule (upgrade.recruit.power)
    - data on board location (tile.resource)
    - data indirect references (adjacent.player.worker.position.tile.resource)

movement

    - move units on hex grid
    - hex board setup and resource placement in association with tiles

priorities

    - priorities should be programmable
        - prioritize player.rule over global.rule or vice versa
