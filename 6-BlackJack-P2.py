# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

#    def draw_back(self, canvas, pos):
#        card_loc = (CARD_BACK_CENTER[0] + CARD_BACK_SIZE[0], 
#                    CARD_BACK_CENTER[1] + CARD_BACK_SIZE[1])
#        canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
                
# define hand class
class Hand:
    def __init__(self):
        self.hand_cards = [] # initialize Hand object to empty list of Card objects
    
    # return a string representation of a Hand object in a human-readable form
    def __str__(self):
        ans = "Hand:"
        for card in self.hand_cards:
            ans += " " + str(card)
        return ans

    def add_card(self, card):
        self.hand_cards.append(card) # append a Card object to the list of cards in a Hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        hasAce = False
        
        for card in self.hand_cards:
            value += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                hasAce = True
                
        if hasAce and (value + 10 <= 21):
            value += 10
        return value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
#        for i in range(len(self.hand_cards)):
#            self.hand_cards[i].draw(canvas, [i * CARD_SIZE[0], 300])
        for card in self.hand_cards:
            card.draw(canvas, [pos[0] + (CARD_SIZE[0]+5) * self.hand_cards.index(card), pos[1]])
 
        
# define deck class 
class Deck:
    def __init__(self): # create a deck of cards and shuffle
        self.deck_cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck_cards.append(Card(suit, rank))
        random.shuffle(self.deck_cards)

    def shuffle(self):
        random.shuffle(self.deck_cards)

    def deal_card(self):
        return self.deck_cards.pop()
    
    def __str__(self):
        ans = "Deck: "
        for card in self.deck_cards:
            ans += str(card) + " "
        return ans   



#define event handlers for buttons
def deal():
    global outcome, in_play

    # your code goes here
    global deck, player_hand, dealer_hand, player_busted, dealer_busted, score

    if not in_play:
        player_busted = False
        dealer_busted = False
        
        deck = Deck() # create a new deck
#        print deck
        
        player_hand = Hand()
        dealer_hand = Hand()
        
#        print "................"
#        print "Dealing cards..."
        player_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        
#        print deck
#        print "Player's", player_hand, ", value=", player_hand.get_value()
#        print "Dealer's", dealer_hand, ", value=", dealer_hand.get_value() 
        
        in_play = True
        outcome = "Hit or Stand?"
    else:
        outcome = "You lost the round. New deal?"
        score -= 1
#        print "Score = ", score
        in_play = False

def hit():
    global in_play, outcome, score, player_hand, player_busted
 
    # if the hand is in play, hit the player
    if in_play:
        if player_hand.get_value() <= 21:
#            print "Hit player..."
            player_hand.add_card(deck.deal_card())
#            print "Player's", player_hand, ", value=", player_hand.get_value()
            if player_hand.get_value() > 21:
                player_busted = True
#                print "You have busted"
            elif player_hand.get_value() == 21:
                outcome = "You win. New deal?"
#                print "Player wins BlackJack"
                in_play = False
                score += 1
#                print "Score = ", score
    # if busted, assign a message to outcome, update in_play and score
    if player_busted and in_play:
        outcome = "You have busted. New deal?"
        in_play = False
        score -= 1
#        print "Score = ", score

def stand():
    global in_play, player_hand, dealer_hand, outcome, score, dealer_busted, player_busted

    # If the player has busted, remind the player that they have busted.
    if player_busted:
        outcome = "You have busted. New deal?"
#        print "Reminder: You have busted"     
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    else:
#        print "Player stands..."
        while in_play:
            if dealer_hand.get_value() < 17:
#                print "Hit dealer..."
                dealer_hand.add_card(deck.deal_card())
#                print "Dealer's", dealer_hand, ", value=", dealer_hand.get_value()
                if dealer_hand.get_value() > 21:
                    dealer_busted = True
                    outcome = "You won, dealer busted. New deal?"
#                    print "You won, dealer busted."
                    in_play = False
                    score += 1
            else:
                if player_hand.get_value() <= dealer_hand.get_value():
                    outcome = "Dealer wins. New deal?"
#                    print "Dealer wins"
                    in_play = False
                    score -= 1
                else:
                    outcome = "You win. New deal?"
#                    print "Player wins"
                    in_play = False
                    score += 1
        
#        print "Score = ", score
    # assign a message to outcome, update in_play and score
    

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
#    card = Card("S", "A")
#    card.draw(canvas, [300, 300])
    global in_play, score
    canvas.draw_text("Blackjack", [40, 55], 40, 'Aqua', 'sans-serif')
    canvas.draw_text("Score = "+str(score), [410, 50], 30, 'Yellow', 'monospace')
    
    canvas.draw_text("Dealer", [10, 200], 30, 'Black', 'monospace')
    dealer_hand.draw(canvas, [10, 220])
    
    canvas.draw_text("Player", [10, 380], 30, 'Black', 'monospace')
    player_hand.draw(canvas, [10, 400])
    
    canvas.draw_text(outcome, [10, 540], 30, 'Orange', 'monospace')
 
    # if in play, draw image of back of a card over the dealer's first (hole) card to hide it
    if in_play:
        card_loc = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1])   
        canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, [10 + CARD_BACK_CENTER[0], 220 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric