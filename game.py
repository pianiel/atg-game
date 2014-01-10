#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import sys
import players

DEBUG = False

class Game(object):

    class PlayerState():
        def __init__(self, player_class, player_id, name):
            self.dices = []
            self.dices_count = 1
            self.wins = 0
            self.loses = 0
            self.player_class = player_class
            self.name = name

            self.player = self.player_class()
            self.id = player_id
            self.player.setName(self.name)

        def start_round(self):
            self._random_dices()
            self.player.start(self.dices)

        def player_loses(self):
            self.loses += 1
            self.dices_count += 1

        def player_wins(self):
            self.wins += 1

        def _random_dices(self):
            self.dices = ''.join(sorted([str(random.randint(1, 6)) for _ in range(self.dices_count)]))

            if DEBUG:
                print "%s: dices: %s" % (self.id, self.dices)

    def __init__(self, players_cls):
        self.players = []
        self.round_number = 0
        self.starting_player = 0

        for i, (player_id, player_class) in enumerate(players_cls):
            self.players.append(self.PlayerState(player_class, player_id, i+1))

    def play(self, n_rounds=5):

        if DEBUG:
            print "\n### New game, players: %s " % (map(lambda p: p.id, self.players))

        for i in range(n_rounds):
            self._run_round()

        scores = []
        for i, player in enumerate(self.players):
            scores.append((player.id, player.wins - player.loses))

            if DEBUG:
                print "%s: wins: %i, loses: %i, score: %i" % \
                      (player.id, player.wins, player.loses, player.wins - player.loses)


        scores = sorted(scores, cmp = lambda x, y: cmp(x[1], y[1]), reverse = True)

        winners = []
        max_score = scores[0][1]
        for id, score in scores:
            if score == max_score:
                winners.append(id)
            else:
                break

        return winners

    def _succ(self, i):
        """
        Funkcja zwraca numer następnego gracza
        """
        return (i + 1) % len(self.players)

    def _pred(self, i):
        """
        Funkcja zwraca numer poprzedniego gracza
        """
        return (i + len(self.players) - 1) % len(self.players)

    def _run_round(self):
        self.round_number += 1

        for player in self.players:
            player.start_round()

        curr_player = self.starting_player
        history = []

        while True:
            p = self.players[curr_player].player
            move = p.play(history)

            if DEBUG:
                print "%s: move: %s" % (self.players[curr_player].id, move)

            if not self._is_valid(move) or not self._is_older_than_last(move, history):
                self._round_results(self._pred(curr_player), curr_player)
                break

            if move == "CHECK":
                if DEBUG:
                    print "%s checks" % (self.players[curr_player].id, )

                if self._is_in_dices(history[0][1], self.dice_state()):
                    self._round_results(self._pred(curr_player), curr_player)
                else:
                    self._round_results(curr_player, self._pred(curr_player))
                break

            history.insert(0, (curr_player + 1, move))
            curr_player = self._succ(curr_player)

        self.give_results_to_players()

    def _round_results(self, winner, loser):
        """
        Funkcja zawiera logikę wykonywaną przy zakończeniu rundy. Przyjmuję numer gracza wygrywającego
        i przegrywającego oraz uaktualnia statystyki
        """
        if DEBUG:
            print "%s wins, player %s loses" % (self.players[winner].id, self.players[loser].id)

        self.players[winner].player_wins()
        self.players[loser].player_loses()
        self.starting_player = loser

    def give_results_to_players(self):
        """
        Funkcja wywołuje na graczach metodę result przekazując im wyniki po rundzie
        """
        points = [p.wins - p.loses for p in self.players]
        dices = [p.dices for p in self.players]

        if DEBUG:
            print "points: %s, dices: %s" % (points, dices)

        for player in self.players:
            player.player.result(points, dices)

    def dice_state(self):
        return ''.join(sorted([p.dices for p in self.players]))

    @staticmethod
    def _is_in_dices(submission, state):
        '''
        funkcja przyjmujaca zgloszenie i zwracajaca True gdy zgloszenie jest dobre
        '''

        for i in range(len(submission)):
            if submission[i] > state[i]:
                return False

        return True

    @staticmethod
    def _cmp_subs(s1, s2):
        '''
        funkcja przyjmujaca dwa zgloszenia i zwracajaca
             1 gdy s1 jest starsze od s2
             0 gdy s1 jest rowne s2
            -1 gdy s1 jest mlodsze od s2
        '''
        # leksykograficznie porownaj odwrocone zgloszenia
        return cmp(s1[::-1], s2[::-1])

    def _is_valid(self, submission):
        """
        Funkcja sprawdza czy zgłoszenie jest prawidłowe, tj.:
           - ma odpowiednią długość
           - ma liczby z zakresu 1-6
           - jest dobrze posortowane
        """
        if submission == "CHECK":
            return True
        if len(submission) != len(self.players) + self.round_number - 1:

            if DEBUG:
                print "submission %s has wrong length" % (submission, )

            return False

        if not all(map(lambda x: '1' <= x <= '6', submission)):

            if DEBUG:
                print "submission %s has wrong numbers" % (submission, )

            return False

        if submission != ''.join(sorted(submission)):

            if DEBUG:
                print "submission %s has wrong order" % (submission, )

            return False

        return True

    def _is_older_than_last(self, submission, history):
        """
        Fukncja sprawdza czy podane zgłoszenie jest starsze od ostatniego w historii
        """
        if len(history) > 0 and self._cmp_subs(submission, history[0][1]) <= 0:

            if DEBUG:
                print "submission %s is not older than last in history %s" % (submission, history[0][1])

            return False
        return True

def main(players_cls, n_games):

    scores = {}
    for player_id, _ in players_cls:
        scores[player_id] = 0

    for _ in range(n_games):
        random.shuffle(players_cls)
        g = Game(players_cls)
        winners = g.play(n_rounds=5)

        for winner in winners:
            scores[winner] += 1

    for player_id, player_score in scores.items():
        print "%s: %i" % (player_id, player_score)

    print ""

if __name__ == '__main__':
    players_cls = [
        ("Incrementer1", players.Incrementer),
        ("IncrementerRandom1", players.IncrementerRandomChecker),
        ("Incrementer2", players.Incrementer),
        ("IncrementerRandom2", players.IncrementerRandomChecker)
    ]

    n_games = 10

    main(players_cls, n_games)
