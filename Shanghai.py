# -*- coding: utf-8 -*-
#@author: JG077923

import random

#values=['2','3','4','5','6','7','8','9','10','J','Q','K','A']
#valueDict = {'Joker':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13,'A':14}
#pointValues = {'Joker':20,'2':20,'3':5,'4':5,'5':5,'6':5,'7':5,'8':5,'9':5,'T':10,'J':10,'Q':10,'K':10,'A':15}
#scores = {} #maybe initialize in game object

#suits=["\u2660","\u2661","\u2662","\u2663"]
#wilds=['Joker','2']

#order = [1,2,3,0]

# =============================================================================
class Card:
    
    def __init__(self,value,suit):
        self.value = value
        self.suit = suit
                
    def show(self):
        print('{} of {}'.format(self.value,self.suit))
        
    def returns(self):
        return '{} of {}'.format(self.value,self.suit)
        
    def is_wild(self):
        if self.value in ['Joker','2']:
            return True
        else:
            return False
        
    def isnt_wild(self):
        if self.value in ['Joker','2']:
            return False
        else:
            return True


class Deck_of_Cards:
    
    def __init__(self,jokers=False,number_of_Decks=1):
        self.jokers = jokers
        self.number_of_Decks = number_of_Decks
        self.cards = []
        self.build()
        
    def build(self):
        n=0 
        while n<self.number_of_Decks:
            for suit in ["\u2660","\u2661","\u2662","\u2663"]:
                for value in ['2','3','4','5','6','7','8','9','T','J','Q','K','A']:
                    self.cards.append(Card(value,suit))
            if self.jokers==True:
                self.cards.append(Card('Joker',"\u2605"))
                self.cards.append(Card('Joker',"\u2606"))
            n+=1
        random.shuffle(self.cards)
                
        
class Player:
    
    def __init__(self,hand):
        self.status = 'Up'
        self.buys = 0
        self.hand = hand
        self.table = []
        self.valueDict = {'Joker':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13,'A':14}

    def showHand(self):
        print("Your Hand:")
        for ind,c in enumerate(self.hand):
            print(f"{ind}: {c.returns()}")
            
    def showTable(self):
        for ind,m in enumerate(self.table):
            print(f"{ind}: {m}")
            
    def sortHand(self,suit=False):
        if suit==True:
            self.hand = sorted(self.hand,key = lambda x:(x.isnt_wild(),x.suit,self.valueDict[x.value]),reverse=True)
        else:
            self.hand = sorted(self.hand,key = lambda x:self.valueDict[x.value],reverse=True)
                 
           
class Run:

    def __init__(self,cards):
        self.cards = cards
        #self.cards_orignal = cards #Not sure if i need this yet but maybe since im reordering them
        self.suit = 'n/a'
        self.str = ''
        self.wilds = 0
        self.valueDict = {'Joker':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13,'A':14}
        #self.checkRun() #When initialized it will autocheck if the run is valid and return T/F
        
    def __str__(self):
        return f"{self.str} of {self.suit} ({self.wilds} wilds)"
        
    def checkRun(self,length=0):
        wildsCount=0
        natCount=0
        tuples = []
        string = ''
        #Sorting Cards
        self.cards = sorted(self.cards,key = lambda x:self.valueDict[x.value],reverse=True)
        #Initializing suit
        self.suit = self.cards[0].suit
        #Checking to make sure suits match
        for c in self.cards:
            if c.is_wild():
                wildsCount+=1
            else:
                if c.suit == self.suit:
                    natCount+=1
                    tuples.append((c.value,c.suit))
                else:
                    return False
        #Check Count of nats to wilds
        if natCount < wildsCount or len(tuples) != len(set(tuples)) or len(self.cards) < length: #May need to build in run length here
            return False
        #Checking the distance in card values compared to the number of cards
        if len(self.cards) >= self.valueDict[self.cards[0].value] - self.valueDict[self.cards[len(self.cards)-wildsCount-1].value] + 1:
            for c in self.cards:
                if c.is_wild() != True:
                    string += c.value
            self.str = string
            self.wilds = wildsCount
            return True
        else:
            return False
        
    def addCard(self,card):
        self.newsuit=card.suit
        self.newvalue=card.value
        self.cards.append(card)
        if card.is_wild() == True:
            self.wilds+=1
            return True
        elif self.checkRun() == True:
            return True
        else:
            #self.length -= 1
            for ind,c in enumerate(self.cards):
                if c.suit == self.newsuit and c.value == self.newvalue:
                    return self.cards.pop(ind)
        

class Set:

    def __init__(self,cards):
        self.cards = cards
        self.value = 'n/a'
        self.valueDict = {'Joker':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13,'A':14}
        #self.checkSet() #When initialized it will autocheck if the set is valid and return T/F
        
    def __str__(self):
        return f"Set of {self.value}s"
        
    def checkSet(self):
        wildsCount=0
        natCount=0
        #Sorting Cards
        self.cards = sorted(self.cards,key = lambda x:self.valueDict[x.value],reverse=True)
        #Checking to make sure values match
        self.value = self.cards[0].value
        for c in self.cards:
            if c.is_wild():
                wildsCount+=1
            else:
                if c.value == self.value:
                    natCount+=1
                else:
                    return False
        #Check Count of nats to wilds
        if natCount==0 and len(self.cards)>2:
            return True
        elif natCount < wildsCount or len(self.cards) <3:
            return False
        else:
            return True
        
    def addCard(self,card):
        if card.is_wild() or card.value == self.value:
            self.cards.append(card)
            return True
        else:
            return card
            
    
        
class Hand:

    def __init__(self,number_of_sets, number_of_runs, length_of_runs,pListShift): 
        self.status = 'Open'
        self.sets = number_of_sets
        self.runs = number_of_runs
        if number_of_runs != 0:
            self.haveruns = True
        else:
            self.haveruns = False
        self.runlength = length_of_runs
        self.requirements = f"This Hand's Requirements: \n{self.sets} Sets of 3 and {self.runs} Runs of {self.runlength}\n"
        self.pointValues = {'Joker':20,'2':20,'3':5,'4':5,'5':5,'6':5,'7':5,'8':5,'9':5,'T':10,'J':10,'Q':10,'K':10,'A':15}
        self.order = [1,2,3,0]
        self.pListShift = pListShift
        self.stack = []
        self.pile = []
        self.scores = {}
        #Starts playing the hand
        self.playHand()
        
    def deal(self):
        players={}
        #pList=[]
        for i in range(4):
            players['p'+str(i+1)]=[]
        while len(players['p'+str(4)])!= 11:
            for p in players:
                if len(self.stack)==0:
                    break
                else:
                    players[p].append(self.stack.pop())
        #Turning the lists of cards into Player classes
        for p in players:
            players[p] = Player(players[p])
        #Updating variable explorer with the players
        globals().update(players) #locals().update(players)
   
    def playHand(self):
        self.stack = Deck_of_Cards(True,2).cards
        self.deal()
        self.pile.append(self.stack.pop())
        self.pList=['p1','p2','p3','p4']
        for n in range(self.pListShift):
            self.pList = [self.pList[i] for i in self.order]
        # #Show all cards to let people draw in person
        # for p in self.pList:
        #     print(f"\n{p}")
        #     globals()[p].showHand()
        print("\n############################################")
        print('\nStarting Hand!')
            
        #Looping through players until someone has no cards
        while self.status == 'Open':
            print("\n############################################")
            print(f"{self.pList[0]}'s Turn\n")
            self.turn(self.pList[0])
            self.pList = [self.pList[i] for i in self.order]
        
        #When someone goes out
        print("\n############################################")
        print(f"{self.pList[-1]} went out!")
        #Scoring Hands
        for p in self.pList:
            score = 0
            for c in globals()[p].hand:
                score += self.pointValues[c.value]
            self.scores[p] = score
        
    def buying(self):
        for p in self.pList[1:]:
            if globals()[p].buys < 3:
                print("\n############################################")
                print(f"{p}'s Turn to Buy\n")
                print(self.requirements)
                print(globals()[p].status)
                globals()[p].sortHand(self.haveruns)
                globals()[p].showHand()
                i = input(f"{p}: Would you like to buy the discarded {self.pile[-1].returns()}?\n")
                if 'y' in i:
                    globals()[p].hand.append(self.pile.pop())
                    globals()[p].hand.append(self.stack.pop())
                    globals()[p].buys += 1
                    print(f"You drew a {globals()[p].hand[-1].returns()} with your buy")
                    break
                else:
                    pass
            else:
                print(f"##### {p} is out of buys #####")
        print("\n############################################")
        print(f"{self.pList[0]}'s Turn\n")
        print(self.requirements)
        
    def layDown(self,p):
        print('############## Laying Down #################')
        
        #Playing Runs
        if self.runs>0:
            for i in range(self.runs):
                print('')
                globals()[p].showHand()
                print(f"\nRun {i+1}")
                integer = False
                while integer==False: #Loop so non-integers dont break it
                    try:
                        i = list(map(int,input("Please make a list of the indicies for cards you would like to include \n").strip().split(',')))[:]
                        r=[]
                        for x in sorted(i,reverse=True): #Largest to smallest index to not break the pop function
                            r.append(globals()[p].hand.pop(int(x)))
                            integer = True
                    except:
                        print('These are not valid indicies, try again')
                r = Run(r)
                if r.checkRun(self.runlength)==True:
                    globals()[p].table.append(r)
                else:
                    print("RIP. Sucks to be you, pick 'em up\n")
                    l=[]
                    for ind,c in enumerate(r.cards):
                        l.append(ind)
                    for ind in sorted(l,reverse=True):
                        globals()[p].hand.append(r.cards.pop(ind))
                    globals()[p].status = 'Broken'
                    break
                
        #Playing Sets
        if self.sets>0 and globals()[p].status != 'Broken':
            for i in range(self.sets):
                print('')
                globals()[p].showHand()
                print(f"\nSet {i+1}")
                integer = False
                while integer == False: #Loop so non-integers dont break it
                    try:
                        i = list(map(int,input("Please make a list of the indicies for cards you would like to include \n").strip().split(',')))[:]
                        s=[]
                        for x in sorted(i,reverse=True): #Largest to smallest index to not break the pop function
                            s.append(globals()[p].hand.pop(int(x)))
                            integer = True
                    except:
                        print('These are not valid indicies, try again')
                s = Set(s)
                if s.checkSet()==True:
                    globals()[p].table.append(s)
                else:
                    print("RIP. Sucks to be you, pick 'em up\n")
                    l=[]
                    for ind,c in enumerate(s.cards):
                        l.append(ind)
                    for ind in sorted(l,reverse=True):
                        globals()[p].hand.append(s.cards.pop(ind))
                    globals()[p].status = 'Broken'
                    break
                
        #Resetting statuses 
        if globals()[p].status == 'Broken':
            for i in globals()[p].table:
                l=[]
                for ind,c in enumerate(i.cards):
                    l.append(ind)
                for ind in sorted(l,reverse=True):
                    globals()[p].hand.append(i.cards.pop(ind))
            globals()[p].status='Up'
            globals()[p].sortHand(self.haveruns)
        else:
            globals()[p].status='Down'
            if len(globals()[p].hand) == 0:
                globals()[p].status='Out'
            else:
                self.playOnOthers(p)
        #print('')
        #globals()[p].showHand()
        
    def playOnOthers(self,p):
    #     globals()[p].showHand()
    #     #Looks at what every player has laid down
    #     for pers in self.pList:
    #         if globals()[pers].status=='Down':
    #             for m in globals()[pers].table:
    #                 #While loop so that players can play more than one card on a meld
    #                 loop = True
    #                 while loop == True:
    #                     i =input(f"Can you play a card on {pers}'s {m}?\n")
    #                     if 'y' in i:
    #                         i = input('Pick the index number of the card you would like to play\n')
    #                         result = m.addCard(globals()[p].hand.pop(int(i))) #INTEGER
    #                         #Checks the addCard function to see if the card is valid, 
    #                         if result == True:
    #                             if len(globals()[p].hand) == 0:
    #                                 globals()[p].status='Out'
    #                                 break
    #                             print('')
    #                             globals()[p].showHand()
    #                         #If not, card is returned to player
    #                         else:
    #                             print('This Card does not play')
    #                             globals()[p].hand.append(result)
    #                             globals()[p].sortHand(self.haveruns)
    #                     else:
    #                         loop = False
    #                 else:
    #                     continue #only executed if the while loop did NOT break
    #                 break #only executed if the while loop DID break
    #             else:
    #                 continue #only executed if the for loop did NOT break
    #             break #only executed if the for loop DID break
    #     print('')
    
    #def playOnOthers(self,p):
        #globals()[p].showHand()
        #Looks at what every player has laid down
        for pers in self.pList:
            if globals()[pers].status=='Down':
                #for m in globals()[pers].table:
                #While loop so that players can play more than one card on a meld
                loop = True
                while loop == True:
                    print('')
                    globals()[p].showHand()
                    print(f"\n{pers}'s Table:")
                    globals()[pers].showTable()
                    i =input(f"Can you play a card on {pers}'s table?\n")
                    if 'y' in i:
                        #While loop for try/except statement to not break without integers
                        integer=False
                        while integer==False: #Loop so non-integers dont break it
                            try:
                                m,i = [x for x in input("Select the indicies for which meld followed by which card you'ld like to play\n").split(',')]
                                #m = input('Which Meld?     ')
                                #i = input('Pick the index number of the card you would like to play     ')
                                result = globals()[pers].table[int(m)].addCard(globals()[p].hand.pop(int(i)))
                                integer=True
                            except:
                                print('These are not valid indicies, try again')
                        #Checks the addCard function to see if the card is valid, 
                        if result == True:
                            if len(globals()[p].hand) == 0:
                                globals()[p].status='Out'
                                break
                            #print('')
                            #globals()[p].showHand()
                        #If not, card is returned to player
                        else:
                            print('This Card does not play')
                            globals()[p].hand.append(result)
                            globals()[p].sortHand(self.haveruns)
                    else:
                        loop = False
                else:
                    continue #only executed if the while loop did NOT break
                break #only executed if the while loop DID break
        
    def turn(self,p):
        #Drawing
        print(self.requirements)
        print(globals()[p].status)
        globals()[p].sortHand(self.haveruns)
        globals()[p].showHand()
        i = input(f"Would you like to pick up the discarded {self.pile[-1].returns()}?\n")
        if 'y' in i:
            globals()[p].hand.append(self.pile.pop())
            print('')
        else:
            #Buying and Drawing from Stack
            self.buying()
            print(f"You drew a {self.stack[-1].returns()}\n")
            globals()[p].hand.append(self.stack.pop())
        if globals()[p].status=='Up':
            globals()[p].sortHand(self.haveruns)
            globals()[p].showHand()
        else:
             globals()[p].sortHand(self.haveruns)
        
        #Play cards
        if globals()[p].status=='Down':
            print('Playing on others')
            self.playOnOthers(p)
        elif globals()[p].status=='Up':
            i =input("Would you like to lay down?\n")
            if 'y' in i:
                self.layDown(p)
            print('')

        #Discard
        if globals()[p].status != 'Out':
            globals()[p].showHand()
            integer=False
            while integer==False: #Loop so non-integers dont break it           
                i = input('Pick the index number of the card you would like to discard\n')
                try:
                    self.pile.append(globals()[p].hand.pop(int(i)))
                    integer=True
                except:
                    print('This is not a valid index, try again')
                    
            if len(globals()[p].hand) == 0:
                globals()[p].status='Out'
                self.status = 'Closed'
        else:
            self.status = 'Closed'
        #Shuffle discard pile into draw pile if its empty
        if len(self.stack) == 0:
            self.stack = self.pile[:-1]
            random.shuffle(self.stack)
            self.pile = self.pile[-1:]

            
    
class Game:
    
    def __init__(self):
        self.scores = {'p1':0,'p2':0,'p3':0,'p4':0}
        self.shifter = random.randint(0,3)
        h1 = Hand(2,0,0,self.shifter)
        self.scoring(h1.scores)
        h2 = Hand(1,1,4,self.shifter)
        self.scoring(h2.scores)
        h3 = Hand(0,2,4,self.shifter)
        self.scoring(h3.scores,True)
        # h4 = Hand(3,0,0,self.shifter)
        # self.scoring(h4.scores)
        # h5 = Hand(1,1,7,self.shifter)
        # self.scoring(h5.scores)
        # h6 = Hand(2,1,5,self.shifter)
        # self.scoring(h6.scores)
        # h7 = Hand(0,3,4,self.shifter)
        # self.scoring(h7.scores)
        # h8 = Hand(1,1,10,self.shifter)
        # self.scoring(h8.scores)
        # h9 = Hand(3,1,5,self.shifter)
        # self.scoring(h9.scores)
        # h10 = Hand(0,3,5,self.shifter)
        # self.scoring(h10.scores,True)
        
        #Sorting and printing final scores
        self.scores = sorted(self.scores.items(), key=lambda x: x[1],)
        print("\n############################################")
        print("\nHere are the final scores:")
        for ind,p in enumerate(self.scores):
            print(f"{ind+1}: {p[0]} with {p[1]} points")
        print(f'\nCongratulations {self.scores[0][0]}!')

    def scoring(self,hand,last=False):
        scores={}
        for k in self.scores.keys():
            scores[k] = self.scores[k] + hand[k]
        self.scores = scores
        self.shifter += 1
        if last != True:
            print(f"\nCurrent Scores: {self.scores}")
            #ADJUST PRINTING
            #for ind,p in enumerate(self.scores):
            #print(f"{ind+1}: {p[0]} with {p[1]} points")
            
        
# =============================================================================

#settest = Set([Card('2','\u2661'),Card('2','\u2660'),Card('5','\u2660'),Card('5','\u2661'),Card('5','\u2661')])
# r = Run([Card('A','\u2660'),Card('K','\u2660'),Card('Q','\u2660'),Card('2','\u2660'),Card('2','\u2660'),Card('9','\u2660')])
# r.checkRun(7)
# print(r)
# r.addCard(Card('8','\u2660'))
# r.cards






#h1 = Hand(2,0,0)
#h1.playHand()
#h1scores = h1.scores


                
            
Game()











        

    








