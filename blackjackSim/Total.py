# -*- coding: utf-8 -*-
"""
Finding a total of a hand. 

@author: darko
"""
from numpy import array
from numpy import unique


def AddAce(card):
    if card == 'A': return AddAce(array([1, 11])) # Both cards aces
    else: 
        result = array([card + 1, card + 11]) 
        result = result.flatten()[result.flatten()<22] # Flatten and keep values < 22 only
        if len(unique(result))==1: return int(result) # Array of length 1 to int
        else: return unique(result)    # Remove repeting values
        
        
# Adding a card to a total:
def AddCards(cards, card):
    if cards == 'A': return AddAce(card)
    elif card == 'A': return AddAce(cards)
    elif isinstance(cards + card, int): return cards + card
    else: 
        result = cards + card 
        result = result.flatten()[result.flatten()<22]
        if len(unique(result))==1: return int(result)
        else: return unique(result)  
        
        
        
def Bust(cards):
    if isinstance(cards, int):
        if cards > 21: return True
    elif not isinstance(cards, int): 
        if len(cards) == 0: return True
    else: return False        