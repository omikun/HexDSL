def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def in_range(l, n):
    return 1 <= n <= len(l)


def havePlayerSelect(l):
    'given a list, ask player to choose a valid selection and return that element'
    if not l or len(l) == 0:
        raise ValueError('not a valid list for player to choose from')
    if len(l) == 1:
        print 'only 1 choice: ', l[0]
        return l[0]
    choice = 'not a valid choice'
    for i, n in enumerate(l):
        print "%d. %s" % (i + 1, n)
    while not is_int(choice) or not in_range(l, int(choice)):
        choice = raw_input('Enter choice: ')
    return l[int(choice) - 1]
