c = {}
tokentypes = 'list attr val with func =='.split(' ')

class Token:
    def __init__(self, n):
        name = n
        kind = n  # list, attr, val with, func

def islist(m, lname):
    print 'in islist', lname
    if lname in c and type(c[lname]) is list:
        print 'found list!'
        m['list'] = c[lname]
        return 'list' 
    return None

def isattr(m, attr):
    if 'list' not in m:
        raise ValueError('no list found for attr find')
    return attr in m['list']

def isfunc(m, func):
    return callable(func)

funcs = {'list':islist, 'attr':isattr, 'func':isfunc, 'any':lambda x: True}
parserules = [('list attr'.split(' '), parseListAttr),
              ('list with attr'.split(' '), parseFilterList),
              ('list with attr == any'.split(' '), parseFilterListWithVal),
              ('list with func attr'.split(' '), parseReduceList),
             ]

def parser(tokens):
    'identify how to parse tokens and calls corresponding rule parser'
    # ex cats with poop >>= list with attr
    # tree technique
    lst = None
    for parserule, parsefunc in parserules:
        matchparserule = True
        for token,term in zip(tokens, parserule):
            if (term in funcs and funcs[term](m, token) is None)
                and term != token:
                matchparserule = False
                break
        if matchparserule:
            return parseFunc(tokens)
    raise: ValueError('bad rule name')


    if islist(tokens[0]):
        if tokens[1] == 'with':
            if isattr(tokens[2]):
                if tokens[3] == '==':
                    return parseFilterListWithVal(tokens)
                else:
                    return parseFilterList(tokens)
            else:
                return parseReduceList(tokens)
        elif isattr(tokens[2]):
            return parseListAttr(tokens)
    # generic list technique, except attr needs to know what the list is
    #   for nested structures... attr is just a key in a dictionary
    #  tokenkinds = [f(t) for f in funcs for t in tokens if f(t)]  #all lists
    print 'tokenkinds:', tokenkinds
    tokenkinds = []
    # 2 list attr
    # 3 list with attr
    # 5 list with attr eq val
    # 4 list with func attr
    listName = tokens[0]
    if listName in c and any(tokens[1] in e for e in c[listName]):
        print 'found list.attr pattern'
        return parseListAttr(tokens)
        
def parseListAttr(tokens):
    'list.attr'
    global c
    lname, attr = tokens
    l = c[lname]
    return [e[attr] for e in l if attr in e ]

def parseReduceList(tokens):
    'list with max attribute'
    lst,wth,func,attr = tokens
    lst = c[lst]
    if func == 'max':
        print lst
        return max(lst, key=lambda e: e[attr])

def parseFilterList(tokens):
    'list with attribute'
    lst,wth,attr = tokens
    lst = c[lst]
    return filter(lambda e: attr in e, lst)

def parseFilterListWithVal(tokens):
    'list with attribute'
    lst,wth,attr,eq,val = tokens
    lst = c[lst]
    return filter(lambda e: attr in e and e[attr] == val, lst)

for fur in 'brown black blacknwhite white grey'.split(' '): c.setdefault('cats', []).append({'fur':fur})
for i, cat in enumerate(c['cats']): cat['poop'] = i
c['cats'][2]['name'] = 'shadow'
c['cats'][3]['name'] = 'momo'

print c
rule = "cats.name".split('.')
print parser(rule)
rule2 = 'cats with max poop'.split(' ')
print parseReduceList(rule2)
rule3 = 'cats with name'.split(' ')
print parseFilterList(rule3)
rule4 = 'cats with name == momo'.split(' ')
print parseFilterListWithVal(rule4)
