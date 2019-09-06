'''
Created on Sep 6, 2018

@author: Adrian Ridder
'''
import _tracemalloc
from random import randint
from copy import copy

class cardDeck(object):
    '''
    classdocs
    '''
    def __init__(self, deck = None):
        '''
        Creates deck
        '''
        self.suits = ('spades', 'clubs', 'diamonds', 'hearts')
        self.numbers = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
        self.deck = list()
        if deck != None:
            self.deck = deck
            self.deckSize = (len(self.deck) - 1)
        else:
            self.deckSize = 51
            self.createDeck() #Create the deck for first use.
        
    def createDeck(self):
        self.deckSize = 51
        for suit in self.suits:
            for number in self.numbers:
                self.deck.append( (number, suit) ) 
                  
       
    def drawCard(self, *_card):
        '''Draws a single card from the deck'''
        if not _card:
            thing = randint(0, self.deckSize)
            card = self.deck[thing]
            self.deckSize -= 1
            self.deck.remove(card) #removes card from the deck
            return card
        else:
            self.deck.pop(_card)
            self.deckSize -= 1
            return
    
    
    def dealHand(self, handSize):
        hand = []
        for x in range(handSize):
            card = self.drawCard()
            hand.append(card) 
        return hand


def straightFlush(hand):
    '''Determines if the hand held is a straight flush'''
    if ( flush(hand) and straight(hand) ):
        return True
    else:
        return False  
      
def fourOfAKind(hand):
    count = dict()
    for card in hand: 
        if card[0] not in count.keys():
            count[card[0]] = 1
        else:
            count[card[0]] += 1
    if 4 in count.values():
        return True
    else:
        return False

def fullHouse(hand):
    count = dict()
    for card in hand: #add up the values
        if card[0] in count.keys():
            count[card[0]] += 1
        else:
            count[card[0]] = 0
    if( (3 in count.values()) and (2 in count.values()) ):
        return True
    else:
        return False

def flush(hand):
    #print(hand)
    count = dict()
    for card in hand: #create the keys
        count[card[1]] = 0
    for card in hand: #add up the values
        count[card[1]] += 1
    if 5 in count.values() :
        return True
    else:
        return False

def straight(hand): #hand looks like this: [ (x, str0), (y, str1), ... ]
    indexLimit = len(hand) - 1
    hand = sorted(hand, key=lambda card: card[0])
    for ind in range(indexLimit):
        if (hand[ind + 1][0] != hand[ind][0] + 1): #y != x + 1
            return False
    return True

def threeOfAKind(hand):
    count = dict()
    for card in hand: 
        if card[0] not in count.keys():
            count[card[0]] = 1
        else:
            count[card[0]] += 1
    if 3 in count.values():
        return True
    else:
        return False

def twoPair(hand):
    count = dict()
    for card in hand: 
        if card[0] not in count.keys():
            count[card[0]] = 1
        else:
            count[card[0]] += 1
    if list(count.values()).count(2) == 2: #see if there are two pairs of cards. Gotta turn it into a list first
        return True
    else:
        return False

def onePair(hand):
    count = dict()
    for card in hand: 
        if card[0] not in count.keys():
            count[card[0]] = 1
        else:
            count[card[0]] += 1
    if 2 in count.values(): #see if there are two pairs of cards
        return True
    else:
        return False

def handValue(hand):
    '''Returns unique value for every hand possible. Highest valued hand is the winner'''
    value = 0
    if straightFlush(hand):
        #print("here1")
        value += 9000
        value += max(hand, key=lambda card: card[0])[0]
        return value
        
    elif fourOfAKind(hand):
        value += 8000
        for card in hand:
            if hand[hand.index(card) + 1][0] == card[0]:
                value += card[0]
                return value
            
    elif fullHouse(hand):
       # print("here3")
        value += 7000
        count = dict()
        for card in hand:
            if card[0] not in count.keys():
                count[card[0]] = 1
            else:
                count[card[0]] += 1
        if count[count.keys()[0]] == 3:
            value += count.keys()[0]
        else:
            value += count.keys()[1]
        return value       
        
    elif flush(hand):
       
        value += 6000
        count = dict()
        for card in hand:
            if card[0] not in count.keys():
                count[card[0]] = 1
            else:
                count[card[0]] += 1
        copyKeys = copy(list(count.keys()))
        for i in range(5):
            value += ( max(copyKeys) / (100 ** i) )
            copyKeys.remove(max(copyKeys))
        return value
    
    elif straight(hand):
        #print("here5")
        value += 5000
        value += max(hand, key=lambda card: card[0])[0]
        return value
        
    elif threeOfAKind(hand):
        #print("here6")
        value += 4000
        count = dict()
        for card in hand:
            if card[0] not in count.keys():
                count[card[0]] = 1
            else:
                count[card[0]] += 1
        if count[list(count.keys())[0]] == 3:
            value += list(count.keys())[0]
            return value
        elif count[list(count.keys())[1]] == 3:
            value += list(count.keys())[1]
            return value
        else:
            value += list(count.keys())[2]
            return value 
        
    elif twoPair(hand):
        #print("here7")
        value += 3000
        count = dict()
        for card in hand:
            if card[0] not in count.keys():
                count[card[0]] = 1
            else:
                count[card[0]] += 1
        for key in count.keys():
            if count[key] == 2:
                value += (key * 20)
            else:
                value += key
        return value
        
    elif onePair(hand):
        #print("here8")
        value += 2000
        count = dict()
        
        for card in hand:
            if card[0] not in count.keys():
                count[card[0]] = 1
            else:
                count[card[0]] += 1
        copyKeys = copy(list(count.keys()))
        for key in count.keys():
            if count[key] == 2:
                value += key
                copyKeys.remove(key)
                break
        for i in range(3):
            value += ( max(copyKeys) / (100 ** i) )
            copyKeys.remove(max(copyKeys))      
        return value
        
    else:
        value += 1000
        count = dict()
        for card in hand:
            if card[0] not in count.keys():
                count[card[0]] = 1
            else:
                count[card[0]] += 1
        copyKeys = copy(list(count.keys()))
        for i in range(5):
            value += ( max(copyKeys) / (100 ** i) )
            copyKeys.remove(max(copyKeys))
        return value
    
def compareHands(hand1, hand2):
    '''Returns winning hand of the two hands'''
    if handValue(hand1) >= handValue(hand2):
        #print(handValue(hand1))
        return hand1
    else:
        #print(handValue(hand2))
        return hand2
    
    
def getBestCommunityCards(hand, communityCards): #Should have the hand of 3 cards and then another list of 5 comm cards cards [ (x, str0), (y, str1), ... ]
    '''Returns hand with the best community cards chosen'''
    highestHand = hand + [communityCards[0], communityCards[1]] #choose arbitrary highest hand to begin
    #print(highestHand)
    for card1 in communityCards:    #choose one card from communityCards
        communityCardsCopy = copy(communityCards)   #make copy of community cards
        communityCardsCopy.remove(card1)
        for card2 in communityCardsCopy:  #delete card from community cards copy, then iterate through the rest of the cards
            highestHand = compareHands(highestHand, hand + [card1, card2])
    return highestHand
            
def drawRandomCommunityCards(hand, community):
    card1 = community[randint(0, 4)]
    communityCardsCopy = copy(community)
    communityCardsCopy.remove(card1)
    card2 = communityCardsCopy[randint(0, 3)]
    return hand + [card1, card2]
    
    
    
    