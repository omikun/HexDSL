c = {}
tokentypes = 'list attr val with func =='.split(' ')

class Token:
    def __init__(self, n):
        name = n
        kind = n  # list, attr, val with, func

def islist(m, lname):
    if lname in c and type(c[lname]) is list:
        m['list'] = c[lname]
        return 'list' 
    return None

def isattr(m, attr):
    if 'list' not in m:
        raise ValueError('no list found for attr find')
    return any(attr in e for e in m['list'])

def isfunc(m, func):
    ret = callable(func) or func in vars(__builtins__)
    #print func, 'is func?', ret
    return ret

def isany(m, a):
    print 'isany ', a
    return True

def isVerb(m, a):
    pass

def parseListAttr(tokens):
    'list.attr'
    global c
    lname, attr = tokens
    l = c[lname]
    return [e[attr] for e in l if attr in e ]

def parseReduceList(tokens):
    'list with max attribute'
    lst, wth, func, attr = tokens
    lst = c[lst]
    if func in vars(__builtins__):
        return vars(__builtins__)[func](lst, key=lambda e: e[attr])
    else:
        raise ValueError(func+' not recognized as builtin, declare this func first?, and implement custom func support')

def parseFilterList(tokens):
    'list with attribute'
    lst, wth, attr = tokens
    lst = c[lst]
    return filter(lambda e: attr in e, lst)

def parseFilterListByMembership(tokens):
    'list with attribute in list2'
    lst, wth, attr, i, lst2 = tokens
    lst, lst2 = c[lst], c[lst2]
    return filter(lambda e: attr in e and e[attr] in lst2, lst)

def parseFilterListWithVal(tokens):
    'list with attribute == val'
    lst, wth, attr, eq, val = tokens
    lst = c[lst]
    return filter(lambda e: attr in e and e[attr] == val, lst)

def parseVerb(tokens):
    pass

def scheduleVerb(tokens):
    scheduler.addRecurring(parseVerb, tokens[:2])

funcs = {'list': islist, 'attr': isattr, 'func': isfunc, 'any': isany, 'verb': isVerb}
parserules = [('list attr'.split(' '), parseListAttr),
              ('list with attr == any'.split(' '), parseFilterListWithVal),
              ('list with attr in list'.split(' '), parseFilterListByMembership),
              ('list with attr'.split(' '), parseFilterList),
              ('list with func attr'.split(' '), parseReduceList),
              ('verb num item every num turn').split(' '), scheduleVerb),
              ('verb num item').split(' '), parseVerb),
              ]

def parser(tokens):
    'identify how to parse tokens and calls corresponding rule parser'
    # ex cats with poop >>= list with attr
    m = {}
    for parserule, parsefunc in parserules:
        # print 'trying ', parserule, parsefunc.__name__
        matchparserule = True
        if len(tokens) != len(parserule):
            continue
        for token, term in zip(tokens, parserule):
            if not (term in funcs and funcs[term](m, token)) \
              and term != token:
                matchparserule = False
                break
        if matchparserule:
            print parsefunc.__name__, parserule, tokens
            return parsefunc(tokens)
    raise ValueError('Error: malformed token sequence '+tokens)

if __name__ == '__main__':
    for f in 'brown black blacknwhite white grey'.split(' '):
        c.setdefault('cats', []).append({'fur': f})
    for i, cat in enumerate(c['cats']):
        cat['poop'] = i
    c['cats'][1]['name'] = 'shadow'
    c['cats'][2]['name'] = 'momo'
    
    print c
    rule = "cats name".split(' ')
    print parser(rule)
    rule2 = 'cats with max poop'.split(' ')
    print parser(rule2)
    rule3 = 'cats with name'.split(' ')
    print parser(rule3)
    rule4 = 'cats with name == momo'.split(' ')
    print parser(rule4)
    rule5 = 'cats with fur in allergicToMe'.split(' ')
    c['allergicToMe'] = 'blacknwhite brown'.split(' ')
    print parser(rule5)
