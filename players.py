#!/usr/bin/env python

import random

class Player(object):
    
    def __init__(self):
        # self.points = 0  # ?
        pass

    def setName(self, i):
        '''
        metoda wywolywana na poczatku gry, 
        jako parametr gracz otrzymuje swoj numer (1, 2, 3 lub 4)
        '''
        self.name = i
        self.k = 3

    def start(self, dice):
        '''
        metoda wywolywana na poczatku rundy,
        parametr dice to lista z wartosciami kosci gracza
        '''
        self.dice = dice
        self.k = self.k + 1

    def play(self, history):
        '''
        metoda wywolywana w momencie, gdy nastepuje kolej gracza, zeby zagrac.
        Parametr history zawiera liste wszystkich dotychczasowych zgloszen 
        wraz z numerami graczy, ktorzy ich dokonali 
        (najnizszy indeks ma najnowsze zgloszenie; 
            czyli dla gracza 4 w powyzszym przykladzie wygladalaby tak: 
            [[3,"111126"],[2,"111112"],[1,"111111"]]). 
        Funkcja powinna zwrocic lancuch opisujacy zgloszenie gracza 
        lub slowo "CHECK" zeby sprawdzic
        '''

        raise Exception, 'player not implemented'
        pass

    def result(self, points):
        '''
        funkcja wywolywana po zakonczeniu rundy; 
        parametr points jest 4 elementowa lista, 
        z iloscia punktow dla kolejnych graczy (0, 1, lub -1).
        '''
        pass


class Incrementer(Player):

    def __init__(self):
        super(Player, self).__init__()
    
    def play(self, history):
        '''
        zwraca zgloszenie o jedno oczko na jednej kostce wieksze
        '''
        if history == []:
            return ''.join('1' * self.k)
        last = list([int(e) for e in history[0][1]])
        for i in range(len(last)):
            if last[-1-i] < 6:
                last[-1-i] = last[-1-i] + 1
                return ''.join([str(e) for e in last])
        reply = 'CHECK'
        return reply       


class IncrementerRandomChecker(Player):

    def __init__(self):
        super(Player, self).__init__()
    
    def play(self, history):
        '''
        zwraca zgloszenie o jedno oczko na jednej kostce wieksze
        srednio po 5 razach sprawdza
        '''
        if history == []:
            return ''.join('1' * self.k)
        last = list([int(e) for e in history[0][1]])
        if random.random() < 0.1:
            return 'CHECK'
        for i in range(len(last)):
            if last[-1-i] < 6:
                last[-1-i] = last[-1-i] + 1
                return ''.join([str(e) for e in last])
        reply = 'CHECK'
        return reply       

