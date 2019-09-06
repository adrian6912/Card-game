'''
Created on Sep 6, 2018

@author: Adrian Ridder
'''

#import CardGame
from copy import copy
from CardGame import cardDeck, compareHands,drawRandomCommunityCards, getBestCommunityCards

def hypotheticalHands(times, deck, hand, community, bestCommunityCards = False):
    '''Creates hypothetical hands with randomly chosen community cards. RANDOM.'''
    wins = 0
    losses = 0
    for i in range(times):
        haventLostYet = True
        copyDeck = cardDeck(copy(deck.deck))
        opponents = list()         
        for x in range(5):
            if bestCommunityCards == False: 
                opponents.append(drawRandomCommunityCards(copyDeck.dealHand(3), community))
            else:
                opponents.append(getBestCommunityCards(copyDeck.dealHand(3), community))
        ind = 0
        while(haventLostYet and ind < 5):
            if compareHands(hand, opponents[ind]) == opponents[ind]:
                losses += 1
                haventLostYet = False   #now we HAVE lost. Wampasaurus.
            ind += 1
        if haventLostYet:
            wins += 1 
    return wins / times

def getExpectedWin(indStats, number):
    twentyStats = dict()
    for x in range(500):
        if indStats[number][x] not in twentyStats.keys(): #if not a key, make it a key
            twentyStats[indStats[number][x]] = indStats[number][x]
        else:
            twentyStats[indStats[number][x]] += indStats[number][x]
    expectedValue = 0
    for key in twentyStats.keys():
        expectedValue += (key * twentyStats[key])
    return expectedValue / 500

def theRealDeal(stats, randomHypothetical = False):
    for time in range(500):
        deck = cardDeck()
        hand = deck.dealHand(3)
        community = deck.dealHand(5)
        hand = getBestCommunityCards(hand, community)
        
        if randomHypothetical == True:
            stats[20].append(hypotheticalHands(20, deck, hand, community, True))
            stats[100].append(hypotheticalHands(100, deck, hand, community, True))
            stats[200].append(hypotheticalHands(200, deck, hand, community, True))
        else:
            stats[20].append(hypotheticalHands(20, deck, hand, community))
            stats[100].append(hypotheticalHands(100, deck, hand, community))
            stats[200].append(hypotheticalHands(200, deck, hand, community))
        
        #Actual Hand
        opponents = list()         
        for x in range(5): #do this five times because there are five opponents
            opponents.append(getBestCommunityCards(deck.dealHand(3), community))
        haventLostYet = True
        ind = 0
        while(haventLostYet and ind < 5):
            if compareHands(hand, opponents[ind]) == opponents[ind]:
                stats['real'].append(0)
                haventLostYet = False   #now we HAVE lost
            ind += 1
        if haventLostYet:
            stats['real'].append(1)

if __name__ == '__main__':
    
    #Run test for random community card choice
    stats = {20:[], 100:[], 200:[], 'real':[]}
    theRealDeal(stats)
    
    wins = list(stats['real']).count(1)
    realWin = wins / 500
    
    twentyExpected = getExpectedWin(stats, 20)
    twentyError = abs(realWin - twentyExpected)
    
    hundredExpected = getExpectedWin(stats, 100)
    hundredError = abs(realWin - hundredExpected)
    
    twoHundredExpected = getExpectedWin(stats, 200)
    twoHundredError = abs(realWin - twoHundredExpected)
    
    print(f"Expected win rate at 20: {twentyExpected} Actual win rate: {realWin} Error: {twentyError}")
    print(f"Expected win rate at 100: {hundredExpected} Actual win rate: {realWin} Error: {hundredError}")
    print(f"Expected win rate at 200: {twoHundredExpected} Actual win rate: {realWin} Error: {twoHundredError}")
    
    #Reset everything for the best community cards
    stats = {20:[], 100:[], 200:[], 'real':[]}
    theRealDeal(stats, True)
    
    wins = list(stats['real']).count(1)
    realWin = wins / 500
    
    twentyExpected = getExpectedWin(stats, 20)
    twentyError = abs(realWin - twentyExpected)
    
    hundredExpected = getExpectedWin(stats, 100)
    hundredError = abs(realWin - hundredExpected)
    
    twoHundredExpected = getExpectedWin(stats, 200)
    twoHundredError = abs(realWin - twoHundredExpected)
    
    print(f"Expected win rate at 20: {twentyExpected} Actual win rate: {realWin} Error: {twentyError}")
    print(f"Expected win rate at 100: {hundredExpected} Actual win rate: {realWin} Error: {hundredError}")
    print(f"Expected win rate at 200: {twoHundredExpected} Actual win rate: {realWin} Error: {twoHundredError}")
    
    