# Requirements for BGDL

    - Human readable, understandable with minimal ramp-up
        - Any non-programmers should be able to learn the language in 1 minute
        - Stick to a subset of English, minimize use of non-alphanumerics
        - Should be more terse than writing out equivalent logic in python 
	    - otherwise just stick to python
    - Language development workflow:
        - Start with an English description of rules
        - Reduce that down to a non-ambiguous, computer parseable form
        - Add symbols for hard to parse phrases or stick to simpler descriptions that may be more verbose
    - implicit: when an alias is encountered, ask player to pick

# keywords: 

    - players, alias, items, rules, winner, 
        - players is a list of players
        - alias is a list of names that mean other things
        - items is a list of countable things
        - rules is a list of actionable things
        - winner is a game winner - game will print the winning player's name
    - for endfor, in, then, if endif, add to, endGame, next, play
        - for... then ... endfor is a standard for loop
        - if... then ... endif is a standard if
        - then ends the condition of for/if
        - var in list is used to instantiate var
        - add thing to otherThing adds thing into the dictionary of otherThing
        - endGame ends the game/terminates loops
        - next returns next element in list
            - current is the current element, can be changed
        - player play rule plays global rules
        - player.play executes player specific rules
            - to do both: 
        	player play or player.play
    - : ,

# Sample BGDL:
## pick num:

players: p1, p2

nums: 1, 2, 3, 4, 5, 6

pickNum:

    return nums

Game:

    choose = player play pickNum
    player = players.next
    guess = player player pickNum
    if guess == choose then
	winner = player
	endGame
    endif

## simple_scythe.bgdl:

players: p1, p2, p3

alias:

    resource: wood, oil, food, metal
    play: trade, bolster, produce
    mats: mat1, mat2, mat3, mat4
    
items: wood, oil, food, metal, star, coin, power

rules: checkWinCondition, checkWinConditionFor

p1: 

    coin: 4
    power: 1
    heart: 0
    wood: 0
    oil: 1
    food: 1
    metal: 0

mat1:

    trade:
        if pay 2 coin then gain 4 star endif
    bolster:
        if pay 2 stars then gain 3 power endif
    produce:
        if pay 1 power then gain 4 star endif
	
checkWinCondition:

    for player in players then
        checkWinConditionFor player
    endfor

checkWinConditionFor player:

    if player.stars >= 20 then
        winner = player
        endGame
    endif

Setup:

    for player in players then
        add mats to player
    endfor

Game:

    player.play
    checkWinConditionFor player
    checkWinCondition
    player = players.next

## blackjack

    cards: ace, 2,3,4,5,6,7,8,9,jack,queen, king
    oneorace: 1, 10
    yesno: 0, 1
    stack: 
    
    resolve:
        score = 0
        for card in hand then
    	if card is jack or queen or king then
    	    score += 10
    	elseif card is ace then 
    	    score += ask oneorace
    	else
    	    score += card
    	endif
        endfor
        if score == 21 then
    	    winner = player
    	endgame
        else score > 21 then
    	    remove player from players
        endif
        if players.length == 1 then
    	    for player in players then
    	        winner = player
    	        endgame
    	    endfor
        endif
    
    pickCards:
        card = cards.top
        remove card from cards
        return card
    
    play:
        print 'get one more card?'
        if ask yesno then
    	    getCard
        endif
    
    getCard:
    	print hand
        hand += pickCards
        add card to player.hand
        print 'split hand?'
        if ask yesno then
    	    #this might be very complicated...
        endif
    
    setup:
        add cards to stack
        add cards to stack
        add cards to stack
        add cards to stack
        shuffle stack
    
    loop:
        player.play
        resolve 
