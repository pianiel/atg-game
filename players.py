#!/usr/bin/env python

import random


class Player(object):
    
    def __init__(self):
        # self.points = 0  # ?
        pass

    def setName(self, i):
        '''
        metoda wywolywana na poczatku gry, 
            - jako parametr gracz otrzymuje swoj numer (1, 2, 3 lub 4)
        '''
        self.name = i
        self.k = 3  # liczba kosci w grze, na poczatku 4

    def start(self, dice):
        '''
        metoda wywolywana na poczatku rundy,
            - parametr dice to lista z wartosciami kosci gracza
        '''
        self.dice = dice
        self.k = self.k + 1

    def play(self, history):
        '''
        metoda wywolywana w momencie, gdy nastepuje kolej gracza, zeby zagrac.
            - parametr history zawiera liste wszystkich dotychczasowych zgloszen 
            wraz z numerami graczy, ktorzy ich dokonali 
            (najnizszy indeks ma najnowsze zgloszenie; 
            czyli dla gracza 4 w powyzszym przykladzie wygladalaby tak: 
            [[3,"111126"],[2,"111112"],[1,"111111"]]). 
        Funkcja powinna zwrocic lancuch opisujacy zgloszenie gracza 
        lub slowo "CHECK" zeby sprawdzic
        '''

        raise NotImplementedError("Player's play(history) method not implemented")

    def result(self, points, dices):
        '''
        funkcja wywolywana po zakonczeniu rundy; 
            - parametr points jest 4 elementowa lista, z iloscia punktow dla kolejnych graczy (0, 1, lub -1);
            - parametr dices jest 4 elementowa lista zawierajaca napisy, opisujace kosci kolejnych graczy 
            (od 1 do 4, kazdy napis jest posortowany w kolejnosci niemalejacej kosci; 
            po rundzie 3 z przykladu powyzej parametr dices mialby wartosc ["34","1","6","22"])
        '''
        pass


class Incrementer(Player):

    def __init__(self):
        super(Player, self).__init__()
    
    def play(self, history):
        '''
        zwraca zgloszenie o jedno oczko na najwyzszej kostce wieksze
        '''
        if history == []:
            return ''.join('1' * self.k)
        last = list([int(e) for e in history[0][1]])
        highest = last[-1]
        for i in range(len(last)):
            if last[-1-i] < highest:
                last[-1-i] = last[-1-i] + 1
                return ''.join([str(e) for e in last])
        if highest < 6:
            last[-1] = highest + 1
            return ''.join([str(e) for e in last])
        return 'CHECK'


class IncrementerRandomChecker(Player):

    def __init__(self):
        super(Player, self).__init__()
    
    def play(self, history):
        '''
        zwraca zgloszenie o jedno oczko na najnizszej kostce wieksze
        CHECK z prawdopodobienstwem p
        '''
        p = 0.1
        if history == []:
            return ''.join('1' * self.k)
        last = list([int(e) for e in history[0][1]])
        if random.random() < p:
            return 'CHECK'
        for i in range(len(last)):
            if last[-1-i] < 6:
                last[-1-i] = last[-1-i] + 1
                return ''.join([str(e) for e in last])
        return 'CHECK'   
