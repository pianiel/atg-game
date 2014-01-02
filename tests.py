#!/usr/bin/env python

import game
import unittest


class TestGame(unittest.TestCase):

    def setUp(self):
        self.g = game.Game()

    def test_cmpdices(self):
        cases = []
        cases.append(('1223','6666', -1))
        cases.append(('1116','5555', 1))
        cases.append(('1116','1116', 0))
        cases.append(('111111','122346', -1))
        cases.append(('111112','111111', 1))
        cases.append(('111126','111112', 1))
        cases.append(('111226','111126', 1))
        cases.append(('111266','111226', 1))
        cases.append(('112266','111266', 1))
        for a, b, c in cases:
            self.assertEqual(c, self.g.cmp_subs(a,b))
            # print a, b, 'OK' if c==g.cmp_subs(a,b) else ':C', g.cmp_subs(a,b), c

    def test_sub_valid(self):
        cases = []
        cases.append(('11124', True))
        cases.append(('11421', False))
        cases.append(('11137', False))
        cases.append(('11421', False))
        for a, b in cases: 
            self.assertEqual(b, self.g.is_valid(a))
            # print a, 'OK' if g.is_sub_valid(a)==b else ':C'

if __name__ == '__main__':
    unittest.main()