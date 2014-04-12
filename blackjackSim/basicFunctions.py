# -*- coding: utf-8 -*-
"""
Basic functions required for Blackjack. Build a deck, shuffle, add up cards, 
compare hands, player and dealer basic strategies.
@author: darko
"""
from numpy.random import shuffle
from numpy.random import choice
from numpy import array
from numpy import unique
#%matplotlib inline


def singleDeck(twos = 4, threes = 4, fours = 4, fives = 4, sixes = 4,
               sevens = 4, eights = 4, nines = 4, tens = 16, aces = 4):
    return [2]*twos + [3]*threes + [4]*fours + [5]*fives + [6]*sixes +[7]*sevens + [8]*eights + [9]*nines + [10]*tens + ['A']*aces


def deckShuffle(NDecks = 6, decks = singleDeck()):
    A = decks * NDecks
    shuffle(A) # numpy.random function shuffle modifies the deck in place
    return A


def drawACard(deck):
    x = choice(len(deck)) # Sellect a random card's index 
    return deck.pop(x) # Return the card removing it from the deck


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
    
    
def playerWin(dealer, player, blackjack = 1.5):
    if dealer == 'BJ':
        if player == 'BJ': return 0, 'Push'
        else: return -1, 'Loss'
    if player == 'BJ':
        if dealer == 'BJ': return 0, 'Push'
        else: return blackjack, 'Win'
    elif dealer == 'Bust'and player != 'Bust': return 1, 'Win'
    elif player == 'Bust': return -1, 'Loss'
    elif player > dealer: return 1, 'Win' 
    elif player < dealer: return -1, 'Loss'
    else: return 0, 'Push'
    
    
    
# Dealer plays the usual strategy:
def dealerPlay(dealer, deck, hard = 17, soft = 17):
    lst =[dealer]
    if len(deck) == 0: deck = deckShuffle()
    card = drawACard(deck)
    lst.append(card) 
    dealer = AddCards(dealer, card)
    count = 2
    if (not isinstance(dealer, int) and dealer[1] == 21): return 'BJ', count, lst

    while not Bust(dealer) and ((isinstance(dealer, int) and dealer < hard) 
                                or(not isinstance(dealer, int) and dealer[1] < soft)):
            count = count + 1
            if len(deck) == 0:
                 deck = deckShuffle()
            card = drawACard(deck)
            lst.append(card) 
            dealer = AddCards(dealer, card)
    if isinstance(dealer, int): 
            if dealer > 21: return 'Bust', count, lst
            else: return dealer, count, lst
    else: 
            if len(dealer) == 2: return int(dealer[1]), count, lst
            else: return 'Bust', count, lst
            
            
            
# Basic strategy: 
def basicStrategy(dealer, card1, card2, deck):
    player = [card1, card2]
    total = AddCards(card1, card2)
    count = 2
    if (not isinstance(total, int) and total[1] == 21): return 'BJ', count, player
    while not Bust(total) and ((not isinstance(total, int) and ((dealer in [9, 10, 'A'] and total[1] < 19) or (dealer not in [9, 10, 'A'] and total[1] < 18))) or  
            (isinstance(total, int) and ((total < 17 and dealer in [7, 8, 9, 10, 'A']) or  (total < 13 and dealer in [2, 3, 4, 5, 6]) and not (total == 12 and dealer in [4, 5, 6])))): 
        count = count + 1
        if len(deck) == 0:
            deck = deckShuffle()
        card = drawACard(deck)
        player = player + [card]
        total = AddCards(total, card)
    if isinstance(total, int): 
        if total > 21: return 'Bust', count, player
        else: return total, count, player
    else: 
        if len(total) == 2: return int(total[1]), count, player
        else: return 'Bust', count, player
        
        
        
        
# Player never hits a hard 12, and thus never busts, but otherwise plays basic strategy. 
def neverBust(dealer, card1, card2, deck):
    player = [card1, card2]
    total = AddCards(card1, card2)
    count = 2
    if (not isinstance(total, int) and total[1] == 21): return 'BJ', count, player
    while not Bust(total) and ((not isinstance(total, int) and ((dealer in [9, 10, 'A'] and total[1] < 19) or (dealer not in [9, 10, 'A'] and total[1] < 18))) or  (isinstance(total, int) and ((total < 12)))): 
        count = count + 1
        if len(deck) == 0:
            deck = deckShuffle()
        card = drawACard(deck)
        player = player + [card]
        total = AddCards(total, card)
    if isinstance(total, int): 
        if total > 21: return 'Bust', count, player
        else: return total, count, player
    else: 
        if len(total) == 2: return int(total[1]), count, player
        else: return 'Bust', count, player
        
# Player mirrors dealer's strategy
def copyDealer(dealer, card1, card2, deck):
    player = [card1, card2]
    total = AddCards(card1, card2)
    count = 2
    if (not isinstance(total, int) and total[1] == 21): return 'BJ', count, player
    while not Bust(total) and ((isinstance(total, int) and total < 17) 
                                or(not isinstance(total, int) and total[1] < 17)):
        count = count + 1
        if len(deck) == 0:
            deck = deckShuffle()
        card = drawACard(deck)
        player = player + [card]
        total = AddCards(total, card)
    if isinstance(total, int): 
        if total > 21: return 'Bust', count, player
        else: return total, count, player
    else: 
        if len(total) == 2: return int(total[1]), count, player
        else: return 'Bust', count, player        