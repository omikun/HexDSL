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

## from chaos... legion?

### Rule from plain English to more parseable form

In each region with a Hero token, the player with the greatest Threat who also has at least one figure in that region must choose one of his figures in that region, and remove it from the board.

for each region in regions, if region has hero then the player with figures in region who has greatest threat return one of his figures in region

for each region with hero, (players with figures in region) with max threat remove 1 of his figures in region

for each region with hero, the player with max threat from (players with figures in region) with max threat remove 1 of his figures in region

    for each region in (regions with hero):
        thisplayer = (players with figures in region) with max threat
        ask thisplayer to return 1 of his figures in region
    
    regions_with_hero = regions with hero
    for each region in regions_with_hero:
        these_players = players with figures in region
        this_player = these_players with max threat
        those_figures = this_player, his figures in region
        ask this_player to return 1 of those_figures


### in BGDL

    player pick a figure from list:
        print list to player
        figure = player pick list   

    player return num figure from list:
        for i in num then
            player pick a figure from list
            name = figure.player
            add figure to collection.name 
            remove figure from list

    for each region in regions then
        if region has hero then
            maxthreatplayer = (players with figures in region) with max threat
            figures = mtp.figures in region
            ask maxthreatplayer return 1 figure from figures
        endif
    endfor

### implicit: 

    list.attr              >> [elem[attr] for elem in list if attr in elem]
    list with max attr     >> max(elem[attr] for elem in list)
    list with attr         >> filter(lambda x: x == attribute, list)
    list with attr == val  >> [elem for elem in list if elem[attr] == val]

## Civ like idea in modern setting

    items: pc, fc, sc, tech, military,citizen, official, president 

    USA:
        government: Democracy
        pc: 400
        fc: 7000
        sc: 300
        tech: 8999
        military: 1200
        officials: 100
        president: 1
        citizen: 100000000 # that votes
    
    citizen:
        # preferences
        security:50, 
        immigration: 20, 
        jobs:70, 
        education: 10, 
        healthcare: 40, 
        tax: 80
    vote:
        choose random # biased by citizen preference criteria
    officials:
        50 random citizen
    elect:
        citizen vote 50 officials
    Democracy:
        # 4 turns per year?
        # 50 officials elected every 10 turns, 100 total 
        elect 50 official every 20 turn
        in 10 turns, elect 50 official every 20 turn
        # 1 president elected every 16 turns
        elect 1 president every 16 turn

    TechTree:
        quantumComputing: 3000, AdvDecryption, AdvAnnealing, 
        AI: 4000, RapidDesign, DeepLearning, AdvControl, CheapInsurance 
        AdvancedRobotics: 2000, AdvSoldier, CheapCareTaker, AdvManufacturing, AutoLabor, CheapSurgery
        NuclearFusion: 2200, CheapEnergy, AdvSpaceTravel, AdvPowerPlant
        StemCell: 8800, FastHeal, Immortality, CheapTransplant
        AntiMatter: 9900, AdvSpaceTravel2, AdvWeaponry, 

    AdvDecryption:
        if pay 200 fc then gain 100 dirt
    AdvAnnealing:
        if pay 100 fc then gain 100 design
    AdvControl:
        #better military control
    CheapInsurance:
        if pay 400 fc then divide 2 Insurance
    DeepLearning:
        if pay 200 fc then gain SelfDriving
    RapidDesign:
        if pay 150 fc then divide 2 BuildTime
    Tank:
        is Military type
        if pay 10 fc then gain 100 tank in 2 BuildTime
    SelfDriving:
        set transport.service cost to 0

    turn:
        player 

    getPlayer:
        player = players.pop

    nextPlayer:
        push player to players
        getPlayer
        
    hasAnyoneWon:
        if player.goal then
            winner = player
            endGame
    game:
        getPlayer
        player turn
        hasAnyoneWon
        nextPlayer