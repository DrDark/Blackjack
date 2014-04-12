# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=2>

# Calculating Expected Utilities 

# <markdowncell>

# The cell that follows contains all the needed bacground functions such as shuffle, dealer's and player's strategies, and the function that determines the winner. These can all be run together.

# <codecell>

from basicFunctions import *
from pandas import DataFrame 
from numpy import random
from scipy.stats import describe
from numpy.random import shuffle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# <headingcell level=3>

# Monte Carlo simulation for calculating and comparing the expected utilities

# <markdowncell>

# We wish to know if out hand totals to 5, and the dealer's first card is also a 5, what is out expected utility if we play the `strategy of never busting` (always stay on a hard 12) and otherwise copying the basic strategy for soft cards. We will later also add the `basic strategy` and `copy the dealer` approach and compare the three. 

# <markdowncell>

# We want to compare a series of scenarios like the following: 

# <codecell>

count = 0
for i in range(10): 
    P = basicStrategy(5, 2, 3, deck)
    D = dealerPlay(5, deck) 
    print 'Player: ', P
    print 'Dealer: ', D
    print "Player's ", playerWin(D[0], P[0])[1]
    count += playerWin(D[0], P[0])[0]
    print ' '
print 'In ten rounds, the player lost/won: $',count    

# <markdowncell>

# In fact, we want to know the count for a much larger number of games for it to have any statistical significance. We pick 10000 rounds, but rather than printing all the games, keep track of count only:

# <codecell>

deck = deckShuffle()
count = 0
for i in range(10000): 
    P = basicStrategy(5, 2, 3, deck)
    D = dealerPlay(5, deck) 
    count += playerWin(D[0], P[0])[0]
    if len(deck)<10: deck = deckShuffle() 
print 'In 10,000 rounds, the player lost/won: $',count 

# <markdowncell>

# We could then figure out what percentage of 10,000 is the outcome and claim that as an estimate of expected utility, but since this number will tend to vary quite a bit even with 10,000 rounds, a more prudent approach is to pick a smaller number, say 1,000 rounds, and obtain a hundred results over 1,000 rounds and then average them out to get an estimate of expected utility. This, it turns out, gives us a pretty reliable estimate. 

# <markdowncell>

# Player plays 1000 rounds against the dealer. He does this 100 times. The results are averaged, and the expected return is found to be around -2.5%. By visually inspecting the list1, one sees that the player loses about 25 more times than he wins.

# <codecell>

deck = deckShuffle()
list1=[]
for j in range(100):
  count = 0
  for i in range(1000):
      P = basicStrategy(5, 2, 3, deck)
      D = dealerPlay(5, deck) 
      count += playerWin(D[0], P[0])[0] 
      if len(deck)<10: deck = deckShuffle()  
  list1.append(count)
print list1 

# <markdowncell>

# We average out the expected outcomes of 1000 hands played 100 times to get a good approximation of expected utility

# <codecell>

l = 0
for i in list1:
  l = l + i/1000.
print l/100.

# <markdowncell>

# Plot the variance. See that the mean is somewhere around -25 but it varies from one set of 1000  hands to another.

# <codecell>

plt.figsize(6,4)
plt.figure(1)
plt.hist(list1, color='k', alpha = .15)
plt.show()

# <codecell>

print '-------'
print '''Summary stats for Player 1 (never bust)'''
print '-------'
Size,  Range, Mean, variance, skewness, kurtosis = describe(list1)
print 'Number of observations: ', Size
print 'Mean: ',  Mean
print 'Min to Max: ', Range
print 'Variance: ', variance
print 'Standard Dev.: ', sqrt(variance)
print 'Skewness: ', skewness
print 'Kurtosis: ', kurtosis
print '-------'
print '-------'

# <markdowncell>

# We can ask more ambitious questions. Given two or more other player strategies, which one has the highest expected return given some peculiar features of a biased deck? A small extension of our method does just that.

# <codecell>

deck = deckShuffle()
list1=[]
list2=[]
list3=[]

player1 = 2
dealer = 5
player2 = 3

for j in range(100):
  count = 0
  count1 = 0
  count2 = 0  
  for i in range(1000):
      P = neverBust(dealer, player1, player2, deck)
      P2 = copyDealer(dealer, player1, player2, deck) # Player 2 plays copy the dealer strategy 
      P3 = basicStrategy(dealer, player1, player2, deck)  # Player 3 plays basic strategy  
      D = dealerPlay(dealer, deck) 
      count += playerWin(D[0], P[0])[0]
      count1 += playerWin(D[0], P2[0])[0] 
      count2 += playerWin(D[0], P3[0])[0]
      if len(deck)<10: deck = deckShuffle()  
  list1.append(count)
  list2.append(count1)
  list3.append(count2) 
        

ls = zip(list1, list2, list3)
l = 0
l2 = 0
l3 = 0
for i, j, k in ls:
  l = l + i/1000.
  l2 = l2 + j/1000.
  l3 = l3 + k/1000.  
print 'Expected return for P playing never bust: ', l/100.
print 'Expected return for P2 copying the dealer: ', l2/100.
print 'Expected return for P3 playing basic strategy: ', l3/100.        



# We can plot the three strategies and see that `basic` (blue) and `never bust` (gray) are more or less the same on this problem, and average close to -0.025, but the third strategy, `copy dealer`, does much worse at around -0.17.



plt.figsize(14, 5)
plt.hist(list1, color = 'k', alpha = .1)
plt.hist(list2, color = 'r', alpha = .1)
plt.hist(list3, color = 'b', alpha = .1)
plt.show();



# A basic engine for calculating the expected utilities, variances, and some other data for comparing strategies



# You set your hand, choose stragegies you wish to compare, 


def utilComputation(dealer, player1,  player2, deck = deckShuffle()):

    from basicFunctions import neverBust as StrategyOne
    from basicFunctions import copyDealer as StrategyTwo
    from basicFunctions import basicStrategy as StrategyThree
    #from somePlace import xxx as StrategyFour
    #from somePlace import xxx as StrategyFive
    #from somePlace import xxx as StrategySix
    
    
    
    '''
    Part 1: Enter the player's hard total n and dealer's card m for which you want 
    to see the expected utility:
    
    Part 2: Simulate 100 times 1000 rounds of play. Three players representing three strategies:
    P: never bust
    P2: play like the dealer (stay on soft and hard 17)
    P3: basic strategy
    Return results as three lists of final outcomes. Each list has 100 elements, each of which is
    a number between -1000 and 1000 (perhaps a bit more if 'BJ' is possible)
    if you bet a dollar in each round, than this number would simply represent the extra dollars
    in your pocket after 1000 rounds (with negative numbers representing dollars lost).
    so -236 means that you lost 236 dollars over 1000 rounds, so your realized utility is -23.6% 
    or -0.236. In Part 3, these numbers are averaged out to obtain an estimate of expected utility.
    100 such numbers are added for each strategy and the total divided by 100. 
    Expected utility should strictly speaking be represented in $ but here we can represent it as
    a percentage of the bet size since it scales linearly.
    '''
    
    
    deck = deckShuffle()
    list1=[]
    list2=[]
    list3=[]
    #list2=[]
    #list3=[]
    #list2=[]
    #list3=[]
    for j in range(100):
      count1 = 0
      count2 = 0
      count3 = 0
      #count4 = 0
      #count5 = 0
      #count6 = 0    
      for i in range(1000):
          P1 = StrategyOne(dealer, player1, player2, deck)
          P2 = StrategyTwo(dealer, player1, player2, deck) 
          P3 = StrategyThree(dealer, player1, player2, deck)   
          #P4 = StrategyFour(dealer, player1, player2, deck)
          #P5 = StrategyFive(dealer, player1, player2, deck) 
          #P6 = StrategySix(dealer, player1, player2, deck)      
          D = dealerPlay(dealer, deck) 
          count1 += playerWin(D[0], P1[0])[0]
          count2 += playerWin(D[0], P2[0])[0] 
          count3 += playerWin(D[0], P3[0])[0]
          #count4 += playerWin(D[0], P4[0])[0]
          #count5 += playerWin(D[0], P5[0])[0] 
          #count6 += playerWin(D[0], P6[0])[0]  
          if len(deck)<10: deck = deckShuffle()  
      list1.append(count1)
      list2.append(count2)
      list3.append(count3) 
      #list4.append(count4)
      #list5.append(count5)
      #list6.append(count6)          
    print 'Strategy 1 outcomes:'
    print list1
    print '-----'
    print ' '
    print ' '
    print 'Strategy 2 outcomes:'
    print list2
    print '-----'
    print ' '
    print ' '
    print 'Strategy 3 outcomes:'
    print list3
    print '-----'
    '''
    print 'Strategy 4 outcomes:'
    print list4
    print '-----'
    print ' '
    print ' '
    print 'Strategy 5 outcomes:'
    print list5
    print '-----'
    print ' '
    print ' '
    print 'Strategy 6 outcomes:'
    print list6
    print '-----'
    '''
    print '-----'
    print ' '
    print ' '
    print ' '
    print ' '
    
    
    '''
    Parts 3 and 4 of the engine need to be adapted for more or fewer than 3 strategies
    '''
    
    '''
    Part 3
    Calculate the expected utility
    '''
    
    ls = zip(list1, list2, list3)
    l1 = 0
    l2 = 0
    l3 = 0
    for i, j, k in ls:
      l1 = l1 + i/1000.
      l2 = l2 + j/1000.
      l3 = l3 + k/1000.  
    print 'Expected return for P1 playing never bust: ', l1/100.
    print 'Expected return for P2 copying the dealer: ', l2/100.
    print 'Expected return for P3 playing basic strategy: ', l3/100.
    print ' '
    print ' '
    print ' '
    print ' '
    
    
    
    '''
    Part 4: Plot the variance of returns: to see that a distribution of your 
    outcomes over 100 attempts of playing 1000 hands. The plot captures the frequency of 
    various realized outcomes over 100 runs on y-axis, and their magnitudes on x-axis. If at
    x of -100 the y is around 20, then about 20 times out of 100 you lost $100. 
    '''
    #plt.figsize(14, 5)
    plt.figure(1)
    plt.title("Strategy 1 in Gray, Strategy 2 in Pink, Strategy 3 in Blue")
    plt.xlabel("Magnitude of a return (could in principle range from -1000 to 1000)")
    plt.ylabel("Frequency of a return (out of 100)")
    plt.hist(list1, color = 'k', alpha = .1)
    plt.hist(list2, color = 'r', alpha = .1)
    plt.hist(list3, color = 'b', alpha = .1);
    
    
    
    '''
    Part 5
    '''
    
    print '-------'
    print '''Summary stats for Strategy 1'''
    print '-------'
    Size,  Range, Mean, variance, skewness, kurtosis = describe(list1)
    print 'Number of observations: ', Size
    print 'Mean: ',  Mean
    print 'Min to Max: ', Range
    print 'Variance: ', variance
    print 'Standard Dev.: ', sqrt(variance)
    print 'Skewness: ', skewness
    print 'Kurtosis: ', kurtosis
    print '-------'
    print '-------'
    
    print ' '
    print ' '
    print ' '
    
    Size,  Range, Mean, variance, skewness, kurtosis = describe(list2)
    print 'Summary stats for Strategy 2'
    print '-------'
    print 'Number of observations: ', Size
    print 'Mean: ',  Mean
    print 'Min to Max: ', Range
    print 'Variance: ', variance
    print 'Standard Dev.: ', sqrt(variance)
    print 'Skewness: ', skewness
    print 'Kurtosis: ', kurtosis
    print '-------'
    print '-------'
    print ' '
    print ' '
    print ' '
    
    Size,  Range, Mean, variance, skewness, kurtosis = describe(list3)
    print 'Summary stats for Strategy 3 '
    print '-------'
    print 'Number of observations: ', Size
    print 'Mean: ',  Mean
    print 'Min to Max: ', Range
    print 'Variance: ', variance
    print 'Standard Dev.: ', sqrt(variance)
    print 'Skewness: ', skewness
    print 'Kurtosis: ', kurtosis
    print 'Summary stats for Player 2'
    print '-------'
    print ' '
    print ' '
    print ' '
    return list1, list2, list3
    

"""
print '-------'
print 'Summary stats for Strategy 4'
print '-------'
Size,  Range, Mean, variance, skewness, kurtosis = describe(list4)
print 'Number of observations: ', Size
print 'Mean: ',  Mean
print 'Min to Max: ', Range
print 'Variance: ', variance
print 'Standard Dev.: ', sqrt(variance)
print 'Skewness: ', skewness
print 'Kurtosis: ', kurtosis
print '-------'
print '-------'

print ' '
print ' '
print ' '

Size,  Range, Mean, variance, skewness, kurtosis = describe(list5)
print 'Summary stats for Strategy 5'
print '-------'
print 'Number of observations: ', Size
print 'Mean: ',  Mean
print 'Min to Max: ', Range
print 'Variance: ', variance
print 'Standard Dev.: ', sqrt(variance)
print 'Skewness: ', skewness
print 'Kurtosis: ', kurtosis
print '-------'
print '-------'
print ' '
print ' '
print ' '

Size,  Range, Mean, variance, skewness, kurtosis = describe(list6)
print 'Summary stats for Strategy 6 '
print '-------'
print 'Number of observations: ', Size
print 'Mean: ',  Mean
print 'Min to Max: ', Range
print 'Variance: ', variance
print 'Standard Dev.: ', sqrt(variance)
print 'Skewness: ', skewness
print 'Kurtosis: ', kurtosis
print 'Summary stats for Player 2'
print '-------'
print ' '
print ' '
print ' '
"""

def testAHand(d, p1, p2, numberOfLoops = 10):
    '''
    Run a few hands to see how a particular hand behaves. 
    '''
    deck = deckShuffle(1)
    count = 0
    for i in xrange(10):
        P = basicStrategy(d, p1, p2, deck)
        D = dealerPlay(d, deck)
        print 'Player: ', P
        print 'Dealer: ', D
        print "Player's ", playerWin(D[0], P[0])[1]
        count += playerWin(D[0], P[0])[0]
        print ' '
    print 'In ten rounds, the player lost/won $ %d' %(count)


def testMtimesNHands(d, p1, p2, deck = deckShuffle(6), M = 100, N = 10000):
    '''
    Simulate a larger number of games and record the count averages against the house.
    '''
    list1=[]
    for j in range(M):
      count = 0
      for i in range(N):
          P = basicStrategy(d, p1, p2, deck)
          D = dealerPlay(d, deck) 
          count += playerWin(D[0], P[0])[0] 
          if len(deck)<10: deck = deckShuffle()  
      list1.append(count)
    l = 0
    for i in list1:
      l = l + i/(M*1.0)
      return l/(N*1.0), list1

    
    plt.hist(list1, color='k', alpha = .15)
    plt.show()
    
    print '-------'
    print '''Summary stats for Strategy 1'''
    print '-------'
    Size,  Range, Mean, variance, skewness, kurtosis = describe(list1)
    print 'Number of observations: ', Size
    print 'Mean: ',  Mean
    print 'Min to Max: ', Range
    print 'Variance: ', variance
    print 'Standard Dev.: ', sqrt(variance)
    print 'Skewness: ', skewness
    print 'Kurtosis: ', kurtosis
    print '-------'
    print '-------'




def largeNofHands(d, p1, p2, deckSiz = 6, N = 100000):
    '''
    Running a large (default 100,000) hand simulation for the given cards, size of deck
    '''
    deck = deckShuffle(deckSiz)
    count = 0
    for i in xrange(N):
    
        P = basicStrategy(d, p1, p2, deck)
        D = dealerPlay(d, deck) 
        count += playerWin(D[0], P[0])[0]
        if len(deck)<10: 
            deck = deckShuffle(6) 
    return count/(N*1.)





while not Bust(total) and ((not isinstance(total, int) and ((dealer in [9, 10, 'A'] and total[1] < 19) or (dealer not in [9, 10, 'A'] and total[1] < 18))) or  
            (isinstance(total, int) and ((total < 17 and dealer in [7, 8, 9, 10, 'A']) or  (total < 13 and dealer in [2, 3, 4, 5, 6]) and not (total == 12 and dealer in [4, 5, 6])))): 
        count = count + 1
        if len(deck) == 0:

# <codecell>

dealer = 3
total = 12
not Bust(total)

# <codecell>

not isinstance(total, int)

# <codecell>

dealer in [9, 10, 'A'] 

# <codecell>

dealer not in [9, 10, 'A']

# <codecell>

#total = array([2, 12])
(not isinstance(total, int)) and dealer in [9, 10, 'A'] and total[1] < 19

# <codecell>

dealer not in [9, 10, 'A'] and total[1] < 18

# <codecell>

isinstance(total, int) and total < 17 and dealer in [7, 8, 9, 10, 'A']

# <codecell>

isinstance(total, int) and total < 13 and dealer in [2, 3, 4, 5, 6]

# <codecell>

isinstance(total, int) and not (total == 12 and dealer in [4, 5, 6])

# <codecell>


