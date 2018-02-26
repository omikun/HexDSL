from common import *
from SortedCollection import *
import bisect

class Event:
    def __init__(self, time, func, args):
        self.time = time
        self.func = func
        self.args = args

class Scheduler:
    def __init__(self, turnPerYear):
        self.turnPerYear = turnPerYear
        self.turn = 1
        self.events = SortedCollection([], key=lambda x : x.time)
    
    def nextTurn(self):
        self.turn += 1
        time, func, args = self.events[0]
        if len(self.events) > 0 and self.turn == time:
            self.events.pop(0)
            func(args)

    def add(self, relTime, func, args):
        self.events.insert(Event(relTime+self.turn, func, args))

    def addRecurring(self, startTime, everyTime, func, args):
        ast = startTime+self.turn  # abs start time
        self.events.insert(Event(ast, func, args))
        self.events.insert(Event(ast+everyTime, addRecurring, None))
