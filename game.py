#!/usr/bin/env python

import random
import players


# players_cls = [players.Player] * 4
players_cls = [
  players.Incrementer, 
  players.Incrementer, 
  players.IncrementerRandomChecker, 
  players.Incrementer
]

class Game(object):

    def __init__(self):
        self.k = [1,1,1,1]
        self.scores = [0]*4
        self.players = []
        for i in range(4):
            p = players_cls[i]()
            p.setName(i+1)
            self.players.append(p)

    def play(self, n_rounds=5):
        first = 0
        for i in range(n_rounds):
            print "### NEW ROUND %s ###" % `i+1`
            self.init_round()
            first = self.run_round(first)
        print "scores", self.scores
        print "dice counts", self.k


    def init_round(self):
        for i,p in enumerate(self.players):
            p.start(self.gen_dices(self.k[i]))

    def run_round(self, first):
        for p in self.players:
            print "player:%d, dices: %s" % (p.name, p.dice)
            ended = False
        curr = first-1
        points = [0] * 4
        history = []
        print 'state:', self.dice_state()
        while not ended:
            curr = (curr+1)%4
            print "player", curr+1,
            p = self.players[curr]
            move = p.play(history)
            print "move", move
            if move == "CHECK":
                ended = True
                print 'state',self.dice_state()
                result = self.cmp_subs(history[0][1], self.dice_state())
                if result == 1:
                    print "player", history[0][0], "lost"
                    points[curr] = 1
                    curr = (history[0][0]+3)%4
                    # print curr
                    self.k[curr] += 1
                    points[curr] = -1
                elif result == -1:
                    print "player", curr+1, "lost"
                    # print curr
                    self.k[curr] += 1
                    points[(curr+3)%4] = 1
                    points[curr] = -1
                elif result == 0:
                    print "draw"
                    # points = [0]*4
                for p in self.players:
                    p.result(points)
                self.scores = [s+p for s,p in zip(self.scores,points)]
                print 'points',points
                return curr
            if not self.is_valid(move):
                print "sub %s not valid, player"%move, curr+1, "lost"
                # print curr
                self.k[curr] += 1
                points[curr] = -1
                for p in self.players:
                    p.result(points)
                self.scores = [s+p for s,p in zip(self.scores,points)]
                print 'points',points
                return curr
            elif history and self.cmp_subs(move, history[0][1]) <= 0:
                print "sub %s not higher than %s, player"%(move,history[0][1]), curr+1, "lost"
                # print curr
                self.k[curr] += 1
                points[curr] = -1
                for p in self.players:
                    p.result(points)
                self.scores = [s+p for s,p in zip(self.scores,points)]
                print 'points',points
                return curr
            history.insert(0, (curr+1, move))

    def dice_state(self):
        state = []
        for p in self.players:
            state.extend(p.dice)
        return ''.join(sorted(state))

    def gen_dices(self, k):
        return [str(int(random.random()*6 + 1)) for _ in range(k)]

    def cmp_subs(self, s1, s2):
        '''
        funkcja przyjmujaca dwa zgloszenia i zwracajaca
             1 gdy s1 jest starsze od s2
             0 gdy s1 jest rowne s2
            -1 gdy s1 jest mlodsze od s2
        '''
        # print [s1, s2]
        if len(s1) != len(s2):
            raise Exception, "submissions lengths not equal"
        return cmp(s1[::-1], s2[::-1])

    def is_valid(self, s):
        if s == "CHECK": return True
        if not all(map(lambda x: '0' < x < '7', s)): return False
        return s==''.join(sorted(s))


def main():
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
    # test_cmpdices()
    # test_sub_valid()
    # from collections import Counter
    # n = 600000
    # cnt = Counter(gen_dices(n)).most_common()
    # print [(i,'%.3f'%(c/(n+0.))) for i,c in cnt]
    # print ''.join([`c[0]` for c in cnt])