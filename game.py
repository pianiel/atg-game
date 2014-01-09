#!/usr/bin/env python

import random
import players

DEBUG = False
# DEBUG = True

from collections import defaultdict, Counter
# stats = defaultdict(int)

class Game(object):

    def __init__(self, players_cls):
        self.n = 4
        self.k = [1,1,1,1]
        self.win = [0,0,0,0]
        self.loss = [0,0,0,0]
        self.scores = [0]*self.n
        self.players = []
        for i in range(len(players_cls)):  #self.n):
            p = players_cls[i]()
            p.setName(i+1)
            self.players.append(p)

    def play(self, n_rounds=5):
        first = 0
        for i in range(n_rounds):
            if DEBUG: print "### NEW ROUND %s ###" % `i+1`
            self.init_round()
            first = self.run_round(first)
        if DEBUG: print "scores", self.scores
        if DEBUG: print "dice counts", self.k


    def init_round(self):
        for i,p in enumerate(self.players):
            p.start(self.gen_dices(self.k[i]))

    def succ(self, i):
        return (i + 1) % self.n

    def pred(self, i):
        return (i + self.n - 1) % self.n

    def run_round(self, first):
        dices = []
        points = [0] * self.n
        history = []
        for p in self.players:
            if DEBUG: print "player:%d, dices: %s" % (p.name, p.dice)
            dices.append(''.join(sorted(p.dice)))
            ended = False
        curr = first-1
        if DEBUG: print 'state:', self.dice_state()
        # badyet = False
        while not ended:
            curr = self.succ(curr)
            if DEBUG: print "player", curr+1,
            p = self.players[curr]
            move = p.play(history)
            # if not badyet and not self.is_in_dices(move, self.dice_state()):
            #     badyet = True
            #     stats[self.dice_state()] += 1
            if DEBUG: print "move", move
            if not self.is_valid(move) or (history and self.cmp_subs(move, history[0][1]) <= 0):
                ended = True
                if not self.is_valid(move):
                    if DEBUG: print "# sub %s not valid, player %d loses, player %d wins" % (move, curr+1, self.pred(curr)+1)
                else:
                    if DEBUG: print "# sub %s not higher than %s, player %d loses, player %d wins" % (move,history[0][1], curr+1, self.pred(curr)+1)
                self.k[curr] += 1
                points[curr] = -1
                points[self.pred(curr)] = 1
            if move == "CHECK":
                ended = True
                if DEBUG: print 'state',self.dice_state()
                if self.is_in_dices(history[0][1], self.dice_state()):
                    if DEBUG: print "# player", curr+1, "loses"
                    if DEBUG: print "# player", self.pred(curr)+1, "wins"
                    self.k[curr] += 1
                    points[curr] = -1
                    points[self.pred(curr)] = 1
                else:
                    if DEBUG: print "# player", self.pred(curr)+1, "loses"
                    if DEBUG: print "# player", curr+1, "wins"
                    points[curr] = 1
                    self.k[self.pred(curr)] += 1
                    points[self.pred(curr)] = -1
                    curr = self.pred(curr) # zeby przegrany zaczynal gre
            history.insert(0, (curr+1, move))
        for p in self.players:
            p.result(points, dices)
        if DEBUG: print "result(points=%s, dices=%s)" % (points, dices)
        self.scores = [s+p for s,p in zip(self.scores,points)]
        self.win[points.index(1)] += 1
        self.loss[points.index(-1)] += 1
        return curr

    def dice_state(self):
        state = []
        for p in self.players:
            state.extend(p.dice)
        return ''.join(sorted(state))

    def gen_dices(self, k):
        return [str(int(random.random()*6 + 1)) for _ in range(k)]

    def is_in_dices(self, s, d):
        '''
        funkcja przyjmujaca zgloszenie i zwracajaca True gdy zgloszenie jest dobre
        '''
        # print 's,d',s,d
        for i in range(len(s)):
            if s[i] > d[i]:
                return False
        return True

    def cmp_subs(self, s1, s2):
        '''
        funkcja przyjmujaca dwa zgloszenia i zwracajaca
             1 gdy s1 jest starsze od s2
             0 gdy s1 jest rowne s2
            -1 gdy s1 jest mlodsze od s2
        '''
        # leksykograficznie porownaj odwrocone zgloszenia
        return cmp(s1[::-1], s2[::-1])

    def is_valid(self, s):
        if s == "CHECK":
            return True
        if len(s) != sum(self.k):
            return False
        if not all(map(lambda x: '0' < x < '7', s)):
            return False
        return s==''.join(sorted(s))


def main(players_cls, n_games):
    win = [0,0,0,0]
    loss = [0,0,0,0]
    scores = [0,0,0,0]
    rounds = [0,0,0,0]
    for _ in range(n_games):
        g = Game(players_cls)
        g.play(n_rounds=5)
        for i in range(len(win)):
            win[i] += g.win[i]
            loss[i] += g.loss[i]
            scores[i] += g.scores[i]
        sm = max(g.scores)
        for i in range(len(g.scores)):
            if g.scores[i] == sm:
                rounds[i] += 1
    for i in range(len(players_cls)):
        print 'wins: %d\t| score: %d\t| rounds won: %d\t| rounds lost: %d\t| player: %s' %  \
            (rounds[i], scores[i], win[i], loss[i],players_cls[i].__name__)
    # means = {}
    # for s,c in stats.items():
    #     means[s] = sum([float(e) for e in s])/len(s)
    # means = {(s,sum([float(e) for e in s])/len(s)) for s, c in stats.items()]}
    # cnt = Counter(stats).most_common(10)
    # print cnt
    # print [(s,means[s]) for s,c in cnt]
    # print means
    # print Counter(means).most_common(10)


if __name__ == '__main__':
    players_cls = [
        players.Incrementer, 
        players.IncrementerRandomChecker,
        players.Incrementer,
        players.IncrementerRandomChecker
    ]
    n_games = 100
    main(players_cls, n_games)
