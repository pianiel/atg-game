atg-game
========

Implementacja gry używanej na Algorytmicznej Teorii Gier


Użytek
========

Boty wcale nie muszą znaleźć się się znaleźć w pliku players.py. Mogę gdzie indziej, a poniższy kod to ogarnie:

    import sys
    sys.path.append('../player')
    import bluff

Natomiast niezmiennie "szanować" muszą interfejs klasy Player ;)

Wybór botów do walki:
https://github.com/mjkpl/atg-game/blob/master/game.py#L169

    players_cls = [
        players.Incrementer, 
        players.IncrementerRandomChecker,
        players.Incrementer,
        players.IncrementerRandomChecker
    ]

Uruchamianie:

    python game.py
