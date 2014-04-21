


# Calculating Expected Utilities of Clumping



from basicFunctions import *
from pandas import DataFrame 
# from scipy.stats import describe
from numpy.random import shuffle
import numpy as np
import pandas as pd
from __future__ import division


def playerStrategy(dealer, card1, card2, deck):
    player = [card1, card2]
    total = AddCards(card1, card2)
    if (not isinstance(total, int) and total[1] == 21): 
        return 'BJ', player
    while not Bust(total) and ((not isinstance(total, int) and ((dealer in [9, 10, 'A'] and total[1] < 19) or (dealer not in [9, 10, 'A'] and total[1] < 18))) or  (isinstance(total, int) and ((total < 17 and dealer in [7, 8, 9, 10, 'A']) or  (total < 13 and dealer in [2, 3, 4, 5, 6]) and not (total == 12 and dealer in [4, 5, 6])))): 
        if len(deck) == 0:
            deck = countAdjustedDeck[:]
        card = drawACard(deck)
        player = player + [card]
        total = AddCards(total, card)
    if isinstance(total, int): 
        if total > 21: 
            return 'Bust', player
        else: return total, player
    else: 
        if len(total) == 2: 
            return int(total[1]), player
        else: 
            return 'Bust', player


def dealerPlay(dealer, deck, hard = 17, soft = 17):
    Dealer =[dealer]
    if len(deck) == 0: deck = countAdjustedDeck[:]
    card = drawACard(deck)
    Dealer.append(card) 
    dealer = AddCards(dealer, card)

    if (not isinstance(dealer, int) and dealer[1] == 21): 
        return 'BJ', Dealer


    while not Bust(dealer) and ((isinstance(dealer, int) and dealer < hard) or(not isinstance(dealer, int) and dealer[1] < soft)):
        
            if len(deck) == 0:
                 deck = countAdjustedDeck[:]
            card = drawACard(deck)
            Dealer.append(card) 
            dealer = AddCards(dealer, card)
    if isinstance(dealer, int): 
            if dealer > 21: 
                return 'Bust', Dealer
            else: 
                return dealer, Dealer
    else: 
            if len(dealer) == 2: 
                return int(dealer[1]), Dealer
            else: 
                return 'Bust', Dealer
            
            

countAdjustedDeck = deckShuffle(NDecks =1, decks = singleDeck(tens = 11))
deck = countAdjustedDeck
count = 0
for i in range(23): 
    d = drawACard(deck)
    P = playerStrategy(d, drawACard(deck), drawACard(deck), deck)
    D = dealerPlay(d, deck) 
    print 'Player: ', P
    print 'Dealer: ', D
    print "Player's ", playerWin(D[0], P[0])[1]
    count += playerWin(D[0], P[0])[0]
    print ' '
print 'In 23 rounds, the player lost/won: $',count 
print 'The remaining cards: ', len(deck)




def expUtilGivenDealerCard(countAdjustedDeck, runNumber=100, handNumber =10000):
    dic = {}
    for card in range(2, 11) + ['A']:
        Deck = countAdjustedDeck[:]
        dic[card]=cardUtility(card, Deck, runNumber, handNumber)
    return dic    
    

#countAdjustedDeck = deckShuffle(NDecks =1, decks = singleDeck(tens = 11))
#data = expUtilGivenDealerCard(countAdjustedDeck, runNumber=100, handNumber =100)
#data = DataFrame(data)


## Decreased expected utility of removing 1 to 15 tens from a single decck, 1000 hands 100 times
dict1 = {}
for i in range(1,17):
    countAdjustedDeck = deckShuffle(NDecks =1, decks = singleDeck(tens = i))
    data = expUtilGivenDealerCard(countAdjustedDeck, runNumber=100, handNumber =1000)
    data = DataFrame(data)
    dict1[i]=data.mean(axis=0)

data1 = DataFrame(dict1)
data1.to_csv('tens1000.csv', sep=',')

## Decreased expected utility of removing 0 to 5 tens, 0 to 3 eights and 0 to 3 nines from a single deck, 1000 hands 100 times
dic = {}
for ten in range(11,17):
    for nine in range(1,5):
        for eight in range(1,5):
            countAdjustedDeck = deckShuffle(NDecks =1, decks = singleDeck(eights= eight, nines=nine, tens = ten))
            data = expUtilGivenDealerCard(countAdjustedDeck, runNumber=100, handNumber =1000)
            data = DataFrame(data)
            dic[(4-eight, 4-nine, 16-ten)]=data.mean(axis=0)
dataHigh = DataFrame(dic) 
dataHigh.to_csv(‘highs.csv', sep=',')


## Increased expected utility of removing 0 to 3 twos, 0 to 3 fours and 0 to 3 sixes from a single deck, 1000 hands 100 times
dic = {}
for two in range(1,5):
    for four in range(1,5):
        for six in range(1,5):
            countAdjustedDeck = deckShuffle(NDecks =1, decks = singleDeck(twos=two, fours=four, sixes=six))
            data = expUtilGivenDealerCard(countAdjustedDeck, runNumber=100, handNumber =1000)
            data = DataFrame(data)
            dic[((4-two), (4-four), (4-six))]=data.mean(axis=0)
dataLow = DataFrame(dic) 
dataLow.to_csv(‘lows.csv', sep=',')



dic = {}
for seven in range(1,5):
    for eight in range(1,5):
        for nine in range(1,5):
            countAdjustedDeck = deckShuffle(NDecks =1, decks = singleDeck(sevens=seven, eights= eight, nines=nine))
            data = expUtilGivenDealerCard(countAdjustedDeck, runNumber=100, handNumber =1000)
            data = DataFrame(data)
            dic[((4-seven), (4-eight), (4-nine))]=data.mean(axis=0)
dataNeut = DataFrame(dic) 
dataNeut.to_csv('neuts.csv', sep=',')



