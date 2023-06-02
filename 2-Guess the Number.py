# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random

num_range = 100
allowed_guesses = 7
remaining_guesses = allowed_guesses

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number, num_range, allowed_guesses, remaining_guesses
    secret_number = random.randrange(0,num_range)
    remaining_guesses = allowed_guesses
    print
    print "New game - guess number in range [0-" + str(num_range) + "). Allowed guesses = " + str(allowed_guesses)


# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global num_range, allowed_guesses, remaining_guesses
    num_range = 100
    allowed_guesses = 7
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global num_range, allowed_guesses, remaining_guesses
    num_range = 1000
    allowed_guesses = 10
    new_game()
    
def input_guess(guess):
    # main game logic goes here
    global remaining_guesses
    remaining_guesses -= 1
    print "Remaining guesses: " + str(remaining_guesses)
    guess = int(guess)
    print "Guess was " + str(guess)
    if remaining_guesses == 0:
        print "Out of guesses. Starting new name. Secret number was " + str(secret_number)
        new_game()
    if secret_number > guess:
        print "Higher"
    elif secret_number < guess:
        print "Lower"
    else:
        print "Correct"
        new_game()

    
# create frame
frame = simplegui.create_frame("Guess the Number", 200, 200)


# register event handlers for control elements and start frame
frame.add_button("Range is [0,100)",range100, 120)
frame.add_button("Range is [0,1000)",range1000, 120)
frame.add_input("Enter guess",input_guess,120)
frame.start()

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
