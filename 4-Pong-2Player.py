# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos = [WIDTH / 2, HEIGHT /2]
    
    if direction == RIGHT:
        ball_vel = [round(random.randrange(120, 240)/60.0, 2), - round(random.randrange(60, 180)/60.0, 2)]
        #print "spawn ball vel RIGHT = ", ball_vel
    elif direction == LEFT:
        ball_vel = [- round(random.randrange(120, 240)/60.0, 2), - round(random.randrange(60, 180)/60.0, 2)]
        #print "spawn ball vel LEFT = ", ball_vel
   

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints

    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0

    spawn_ball(random.choice([LEFT, RIGHT]))

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # ball touches top or bottom walls
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
        #print "top/bottom bounce vel =", ball_vel[1]
    
    # ball touches left gutter
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        # ball touches left paddle
        if ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = - round(1.1 * ball_vel[0], 2) # bounce with 10% increased velocity
            #print "left bounce vel =", ball_vel[0]
        else:
            score2 += 1
            spawn_ball(RIGHT) # ball spawns moving towards the player that won the last point

    # ball touches right gutter
    if ball_pos[0] >= (WIDTH - 1) - BALL_RADIUS - PAD_WIDTH:
        # ball touches right paddle
        if ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = - round(1.1 * ball_vel[0], 2) # bounce with 10% increased velocity
            #print "right bounce vel =", ball_vel[0]
        else:
            score1 += 1
            spawn_ball(LEFT) # ball spawns moving towards the player that won the last point
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")

    # update paddle's vertical position, keep paddle on the screen
    # left paddle: paddle1
    if paddle1_pos + paddle1_vel < HALF_PAD_HEIGHT: # check for top boundary
        pass
    elif paddle1_pos + paddle1_vel > HEIGHT - HALF_PAD_HEIGHT: # check for bottom boundary
        pass
    else:
        paddle1_pos += paddle1_vel
    
    # right paddle: paddle2
    if paddle2_pos + paddle2_vel < HALF_PAD_HEIGHT: # check for top boundary
        pass
    elif paddle2_pos + paddle2_vel > HEIGHT - HALF_PAD_HEIGHT: # check for bottom boundary
        pass
    else:
        paddle2_pos += paddle2_vel    
    
    # draw paddles
    # left paddle: paddle1
    canvas.draw_polygon([[0, paddle1_pos - HALF_PAD_HEIGHT],[PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT],
                         [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT],[0, paddle1_pos + HALF_PAD_HEIGHT]], 
                        1, "Black", "White")
    
    # right paddle: paddle2
    canvas.draw_polygon([[WIDTH - 1, paddle2_pos - HALF_PAD_HEIGHT],[WIDTH - 1, paddle2_pos + HALF_PAD_HEIGHT],
                         [WIDTH - 1 -PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT],[WIDTH - 1 - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT]], 
                        1, "Black", "White")
    
    # draw scores
    canvas.draw_text(str(score1), [150,30], 30, "Aqua")
    canvas.draw_text(str(score2), [450,30], 30, "Aqua")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -4
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 4
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -4 
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 4       
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"] :
        paddle2_vel = 0 

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 100)

# start frame
new_game()
frame.start()
