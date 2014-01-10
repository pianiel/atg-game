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
https://github.com/mjkpl/atg-game/blob/master/game.py#L241

Wpis jest tuplą, której pierwszy element to identyfikator (human readable) bota, a drugi to jego klasa.

    players_cls = [
        ("Incrementer1", players.Incrementer),
        ("IncrementerRandom1", players.IncrementerRandomChecker),
        ("Incremeter2", players.Incrementer),
        ("IncrementerRandom2", players.IncrementerRandomChecker)
    ]


Uruchamianie:

    python game.py
