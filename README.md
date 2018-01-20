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

Game data structures

    - AST - rules are stored as a pseudo abstract syntax trees
        - each node can either be an operator or a verb
            - operators govern the structure of the tree (and, or, if, then, else)
            - verbs specifies how to modify game data
            - verbs may also modify rules themselves
    - data is contained globally, per player, per tile, per unit on tile, or per AST node in rule or per-player-rule.

**TODO**

metaVerb - verbs that modifies other verbs

metaRule - rules executed in response to player executed rules after a turn
    - register which rule a player just executed, then execute corresponding metaRules; beware of dependencies and metarule execution order requirements; can metaRules be dependent on other metaRules?

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
