# -*- coding: utf-8 -*-
"""
Create a deck of cards. Defaults create an unbiased 52 card blackjack deck with 16 10s rather 
than queens, kings, etc. 

@author: darko
"""
from numpy.random import shuffle

def single(twos = 4, threes = 4, fours = 4, fives = 4, sixes = 4, sevens = 4, eights = 4, nines = 4, tens = 16, aces = 4):
    '''Single cards are isolated and can be biased independently. For instance,
    a single(twos = 2) creates a 50 card deck with only two 2s. single() returns a
    standard 52 card deck.'''    
    cards = [2]*twos + [3]*threes + [4]*fours + [5]*fives + [6]*sixes +[7]*sevens + [8]*eights + [9]*nines + [10]*tens + ['A']*aces
    return cards
    


def byClass(no_l=1, no_n=1, no_h=1, no_A=1):
    '''byClass() has a single balanced deck as a default, but any number
       of decks are possible. One can also create unbalanced decks with more
       high or low cards, etc.
    '''    
    Low =range(2, 7)*4 * no_l
    Neut = range(7, 10)*4 * no_n
    High = [10]*16 * no_h
    Ace = ['A']*4 * no_A
    All = Low+Neut+High+Ace
    shuffle(All)
    return All    
    
    
    