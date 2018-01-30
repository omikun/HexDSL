# setup players
# setup rules
# setup board

def isint(choice):
    try:
        int(choice)
        return True
    except:
        return False


def playerChoose(l):
    choice = 'what'
    while not isint(choice) or not (1 <= int(choice) <= len(l)):
        for i, it in enumerate(l):
            print i+1, it
        choice = raw_input('Enter a choice: ')
    return int(choice)-1


class Player:
    def __init__(self, name, t):
        self.name = name
        self.table = t
        self.rule = ''
    
    def play(self):
        #ask player to choose from a valid action
        topRowRules = ['trade', 'bolster', 'produce', 'use', 'skip'] 
        botRowRules = ['upgrade', 'deploy', 'build', 'recruit']
        self.playRules(topRowRules)
        self.playRules(botRowRules)

    def playRules(self, rules):
        rule = rules[playerChoose(rules)]
        ret = False
        # while not ret:
        #     if self.pay(rule):
        #         ret = getattr(self, rule)(rule)  # execute rule
        # return
        # alternative implementation
        while not ret:
            if rule == 'skip':
                break
            if self.pay(rule):
                ret = True
                for thing in self.table[rule]['actions']:
                    act, amount, kind = thing.split(' ')
                    if kind in alias:
                        kind = alias[kind][playerChoose(alias[kind])]
                    if act == 'gain':
                        self.table[kind] += int(amount)
                    elif act == 'build':
                        pass
                    elif act == 'deploy':
                        pass
                    elif act == 'recruit':
                        pass

    def pay(self, rule):
        if self.table['coin'] > self.table[rule]['cost']:
            self.table['coin'] -= self.table[rule]['cost']
            return True
        else:
            return False

alias = {'resource':['wood', 'metal', 'food', 'oil']}
t = {'name':'Rusviet', 'coin':3, 'star':0, 'heart':2, 'power':4, 'combatCard':2, 'wood':0, 'metal':2, 'food':1, 'oil':0, 
'trade':{'cost':2, 'actions':{'gain 2 resource', 'gain 1 heart'}}, 
'bolster':{'cost':2, 'actions':{'gain 2 resource', 'gain 1 heart'}}, 
'produce':{'cost':2, 'actions':{'gain 2 resource', 'gain 1 heart'}}, 
'use':{'cost':2, 'actions':{'gain 2 resource', 'gain 1 heart'}}, 
'upgrade':{'cost':2, 'actions':{'gain 2 resource', 'gain 1 heart'}}, 
'deploy':{'cost':2, 'actions':{'gain 2 resource', 'gain 1 heart'}}, 
'build':{'cost':2, 'actions':{'gain 2 resource', 'gain 1 heart'}}, 
'recruit':{'cost':2, 'actions':{'gain 2 resource', 'gain 1 heart'}}, 
'skip':{'cost':0}}
players = [Player('test', t)] * 4

i = 0
while True:
    player = players[i]
    player.play()
    if player.table['star'] >= 6:
        break;
    #change all player state as a result of current play
    i = (i + 1) % len(players)

print "Victory belongs to ", players[i].name
