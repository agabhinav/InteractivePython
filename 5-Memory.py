# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global cards, exposed, state, turn
    #exposed = []    
    state = 0 # state 0 corresponds to the start of the game
    turn = 0 # reset turns to 0
    label.set_text("Turns = " + str(turn))
    cards = range(8) + range(8)
    random.shuffle(cards)
    #print cards  
    exposed = [False] * len(cards)
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposed, state, c1index, c2index, cards, turn
    
    card_index = pos[0]//50
    if not all(exposed):
        print "Index of card clicked = ", card_index
    else:
        print "All cards exposed"
    
    if state == 0: # new game
        state = 1
        exposed[card_index] = True
        c1index = card_index # store index of 1st card clicked in a variable c1index        
    elif state == 1 and not exposed[card_index]: # State 1 corresponds to a single exposed unpaired card
        state = 2
        exposed[card_index] = True
        c2index = card_index # store index of 2nd card clicked, in a given turn, in a variable c2index
        turn += 1
        label.set_text("Turns = " + str(turn))        
    else:
        if not exposed[card_index]:
            if cards[c1index] != cards[c2index]:
                exposed[c1index] = False
                exposed[c2index] = False

            exposed[card_index] = True
            state = 1
            c1index = card_index # store index of 1st card clicked, in subsequent turn, in a variable c1index
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global cards
    for idx in range(len(cards)):
        if exposed[idx]:
            canvas.draw_text(str(cards[idx]), [(25 + 50 * idx) - 12, 65], 55, "White")
            canvas.draw_line([50 * idx, 0], [50 * idx, 100], 1, "White")
            canvas.draw_line([50 * (idx + 1), 0], [50 * (idx + 1), 100], 1, "White")
        else:
            canvas.draw_polygon([[50 * idx, 0], [50 * idx + 50, 0], [50 * idx + 50, 100], [50 * idx, 100]], 1, "White", 'Green')

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric