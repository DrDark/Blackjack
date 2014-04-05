# -*- coding: utf-8 -*-
"""
Blackjack, card drawing, counting, and shuffling methods

@author: darko
"""
from numpy.random import shuffle
from numpy.random import choice
from Deck import single as singleDeck

def deckShuffle(NDecks = 6, decks = singleDeck()):
    '''The function deckShuffle shuffles 6 decks of cards. 
    The default six decks can be changed using kwarg NDecks, and 
    the kind of deck using decks (one can bias `decks` first, 
    say giving it fewer 10s or extra low cards, then select the 
    number of such decks.)
    '''
    A = decks * NDecks
    shuffle(A) # numpy.random function shuffle modifies the deck in place
    return A
    
    
def drawACard(deck):
    '''
    Draw a random card from a given deck without replacement. 
    Returns the drawn card and `pops` it from the deck.
    '''
    x = choice(len(deck)) # Sellect a random card's index 
    return deck.pop(x) # Return the card removing it from the deck    
    
    
def drawCont(Deck=deckShuffle()):
    '''
    The function drawCont simulates draws from a continuous shuffle. 
    One still feeds in the deck as the number of cards still matters 
    but also in order that biased decks can be passed on: the deck 
    remains unchanged by the draw. 
    It is given standard six decks as a default. 
    '''
    return Deck[choice(len(Deck))] 
    
def orderedDraw(deck = deckShuffle()):
    '''
    Another card drawing procedure. 
    This one simply draws the first card in from a list. 
    '''
    return deck.pop(0)    

def cardCount(card, count):
    '''
    Card counting function. It takes a card and a count and 
    returns a new count. The numbering is somewhat backward. Though
    we are interested in high cards, we add 1 each time we come 
    accross a low card. Thus a high positive count means a lot of
    high cards still to go  in the deck together with relatively
    fewer low cards. The function is a current rather than `true` count.
    True count can be defined in a variety of ways. A particularly simple
    one is to take the current count and divide it by the number 
    of decks remaining.
    '''
    low = range(2, 8)         # `Low`: 2 to 7, total 24 per deck
    high = range(8, 11)     # `High`:  8, 9, and 10, total 24 per deck
    neutral = ['A']     #  `Neutral`: Aces, total 1x4 per deck
    if card in low: return count + 1
    elif card in neutral: return count
    elif card in high: return count - 1

def cardCount1(card, count):
    low = range(2, 7)         # `Low`: 2 to 6, total 20 per deck
    neutral = range(7, 10)     # `Neutral`: 7, 8, 9, total 12 per deck
    high = ['A', 10]     #  `High`: Aces and 10s, total 20 per deck
    if card in low: return count + 1
    elif card in neutral: return count
    elif card in high: return count - 1
        
def trueCount(count, len_deck):
    d = max(1, len_deck/52.) # The number of decks remaining
    return count / d       

def drawPeriodic(count, period, Deck=deckShuffle()):
    '''
    Periodic draw utilizes card counting and ensures that the count 
    stays within some predefined count limit [-n, n]. `period` set to 1 
    ensures that you never see more than two low or two high cards in an 
    unbroken sequence, but it also ensures that the difference between 
    the number of high and low cards drawn is never higher than |1|. 
    As we increase countLimit we get sequences of cards that resemble 
    true randomness. Notice taht the cards with a low limit may appear 
    `more` random to a naked eye, but are definitely not so. A sequence 
    of 5 consecutive 10s in a six deck card shuffle would be a near certainty, 
    and yet impossible if the countLimit regime is |2|.
    '''
    i = choice(len(Deck))
    if Deck[i] == 'A': 
        return cardCount(Deck[i], 0) + count, Deck.pop(i)
    else:     
        while (abs(cardCount(Deck[i], count)) > period) or (Deck[i]=='A'):
            i = choice(len(Deck))
    return cardCount(Deck[i], 0) + count, Deck.pop(i)



def periodShuffle(period, deckSize=6):
    '''
    Procedure for creating a periodic deck of predetermined number of decks 
    and predetermined period. Below, the count period is 3, the number of 
    decks is 10. The new periodically shuffled deck is stored in 
    the list `periodDeck`.
    '''
    deck = deckShuffle(deckSize)
    Count = 0
    periodDeck = []
    countList = []
    for j in range(len(deck)):
        Count, i = drawPeriodic(Count, period = period, Deck=deck)
        periodDeck.append(i)
        countList.append(Count)
    return periodDeck 

  
    
    