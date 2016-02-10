#! /usr/bin/env python

from math import sqrt
from trueskill import Rating
from trueskill.backends import cdf
from trueskill import quality_1vs1
from trueskill import TrueSkill
from random import random
from trueskill import calc_draw_margin


class Player:

    def __init__(self, name, rating):
        self.n = name
        self.rating = rating
        self.score = 0


class TSCalc:
    
    def __init__(self):
        self.mu0 = 25.0
        self.sigma0 = self.mu0
        self.beta = self.mu0
        self.tau = self.sigma0 / 100.0
        self.draw = 0.05

        self.env = TrueSkill(self.mu0, self.sigma0, self.beta, self.tau, self.draw, 'scipy')

    def win_probability(self, player, opponent):
        delta_mu = player.rating.mu - opponent.rating.mu - calc_draw_margin(self.draw, 2, self.env)
        denom = sqrt(2 * (self.beta * self.beta) + pow(player.rating.sigma, 2) + pow(opponent.rating.sigma, 2))
        return cdf(delta_mu / denom)

    def result(self, player0, player1):
        win0 = self.win_probability(player0, player1)
        win1 = self.win_probability(player1, player0)
        draw = 1.0 - win0 - win1
        res = random()
        if res < draw:
            return [0.5, 0.5]
        elif res < draw + win0:
            return [1.0, 0.0]
        else:
            return [0.0, 1.0]

    def result3p(self, player0, player1, player2):
        # I'm not sure pairwise comparison is appropriate; I'm doing it anyway for demonstration
        res01 = self.result(player0, player1)
        res12 = self.result(player1, player2)
        # This is only used if result isn't logically decided by the first two.
        res02 = self.result(player0, player2)
        
        # Two draws is a simple case
        if res01 == res12 == [0.5, 0.5]:
            return [3, 3, 3]

        if res01 == [1.0, 0.0]:
            if res12 == [0.5, 0.5]:
                return [5, 2, 2]
            elif res12 == [1.0, 0.0]:
                return [5, 3, 1]
            elif res12 == [0.0, 1.0]:
                if res02 == [0.5, 0.5]:
                    return [4, 1, 4]
                elif res02 == [1.0, 0.0]:
                    return [5, 1, 3]
                elif res02 == [0.0, 1.0]:
                    return [3, 1, 5]
        if res01 == [0.5, 0.5]:
            if res12 == [1.0, 0.0]:
                return [4, 4, 1]
            if res12 == [0.0, 1.0]:
                return [2, 2, 5]
        if res01 == [0.0, 1.0]:
            if res12 == [0.5, 0.5]:
                return [1, 4, 4]
            elif res12 == [0.0, 1.0]:
                return [1, 3, 5]
            elif res12 == [1.0, 0.0]:
                if res02 == [0.5, 0.5]:
                    return [2, 5, 2]
                elif res02 == [1.0, 0.0]:
                    return [3, 5, 1]
                elif res02 == [0.0, 1.0]:
                    return [1, 5, 3]


class Tournament:
    
    def __init__(self, players):
        self.players = players
        self.tc = TSCalc()
    
    
    def round_match(self, player0, player1, player2):
        result = self.tc.result3p(player0, player1, player2)
        player0.score += result[0]
        player1.score += result[1]
        player2.score += result[2]

    def print_standings(self):
        for p in self.players:
            print p.n + ': ' + str(p.score)
        print '\n'

    def run_round(self, pairings):
        for g in pairings:
            self.round_match(self.players[g[0]], self.players[g[1]], self.players[g[2]])


        

def adamH_semifinal_1(players):
    trn = Tournament(players)

    pairings = []
    pairings.append([ [0, 5, 6], [1, 4, 7], [2, 3, 8] ])
    pairings.append([ [2, 3, 7], [0, 5, 8], [1, 4, 6] ])
    pairings.append([ [0, 3, 7], [1, 5, 8], [2, 4, 6] ])
    pairings.append([ [2, 4, 8], [0, 3, 6], [1, 5, 7] ])

    for p in pairings:
        trn.run_round(p)
    return trn

def one_thousand_adamH_semifinal_1(filename):
    players = initialize_players(filename)
    for i in range(0, 1000):
        t = adamH_semifinal_1(players)
    print '------------------------'
    print 'AdamH Reply 17'
    print '------------------------'
    t.print_standings()

def adamH_january_semifinal(players):
    trn = Tournament(players)

    pairings = []
    pairings.append([ [0, 5, 8], [1, 4, 7], [2, 3, 6] ])
    pairings.append([ [2, 4, 6], [0, 3, 8], [1, 5, 7] ])
    pairings.append([ [1, 3, 7], [2, 5, 6], [0, 4, 8] ])

    for p in pairings:
        trn.run_round(p)
    return trn

def one_thousand_adamH_january_semifinal(filename):
    players = initialize_players(filename)
    for i in range(0, 1000):
        t = adamH_january_semifinal(players)
    print '-----------------------'
    print 'AdamH January Tournament'
    print '-----------------------'
    t.print_standings()


def round_robin(players):
    trn = Tournament(players)

    pairings = []
    pairings.append([ [0, 3, 6], [1, 4, 7], [2, 5, 8] ])
    pairings.append([ [0, 5, 7], [1, 3, 8], [2, 4, 6] ])
    pairings.append([ [0, 4, 8], [1, 5, 6], [2, 3, 7] ])
    pairings.append([ [0, 1, 2], [3, 4, 5], [6, 7, 8] ])

    for p in pairings:
        trn.run_round(p)
    return trn

def one_thousand_round_robin(filename):
    players = initialize_players(filename)
    for i in range(0, 1000):
        t = round_robin(players)
    print '------------------------'
    print 'Infthitbox Reply 25'
    print '------------------------'
    t.print_standings()

def test_all_same_player(players):
    trn = Tournament(players)

    pairings = [ [0, 1, 2] ]
    trn.run_round(pairings)
    return trn

def one_thousand_test_all_same_player(filename):
    players = initialize_players(filename)
    for i in range (0, 1000):
      t = test_all_same_player(players)
    print '-------------------------'
    print 'Testing 3 identical'
    print '-------------------------'
    t.print_standings()

def test_draw(player):
    win0 = 0
    win1 = 0
    draw = 0
    tc = TSCalc()
    for i in range(0, 1000):
        result = tc.result(player, player)
        if result == [1.0, 0.0]:
            win0 += 1
        elif result == [0.0, 1.0]:
            win1 += 1
        elif result == [0.5, 0.5]:
            draw += 1
    print 'Player 0 wins: ' + str(win0)
    print 'Player 1 wins: ' + str(win1)
    print 'Draws: ' + str(draw)

def initialize_players(filename):
    players = []
    with open(filename) as f:
        for x in f:
            x = x.rstrip()
            if not x: continue
            line = x.split(',')
            r = Rating(float(line[1]), float(line[2]) / 3)
            players.append(Player(line[0], r))

    return players
