import simplegui
import random

# flag to check if game is over
gameover = False

score = 0
max_score = 0

# canvas width and height
CANVAS_WIDTH = 700
CANVAS_HEIGHT = 500

# ball initial center point
x_ball = CANVAS_WIDTH/2 # 350
y_ball = CANVAS_HEIGHT/2 # 250

# ball radius
RADIUS_BALL = 15

# GROUND y coordinate
GROUND = CANVAS_HEIGHT - RADIUS_BALL

# initial vertical speed of the ball in pixels
jump_pixels = 0

# obstacle initial parameters
x_obs = CANVAS_WIDTH # 700: canvas width, starting x position of obstacle
y_obs = CANVAS_HEIGHT
obs_width = random.randint(50, 70) # width of obstacle
obs_height = random.randint(50, 250) # length of obstacle
gap = 135 # space between top and bottom obstacles
obs_speed = 3

# helper function to reset game when tap button is pressed after game is over
def reset():
    global x_ball, y_ball, x_obs, y_obs, gameover, jump_pixels, score
    score = 0
    x_ball = CANVAS_WIDTH/2 # 350
    y_ball = CANVAS_HEIGHT/2 # 250
    x_obs = CANVAS_WIDTH
    y_obs = CANVAS_HEIGHT
    jump_pixels = 0    
    gameover = False
    button.set_text('Tap')
    timer.start()   
    
# button event handler
def tap():
    global y_ball, jump_pixels

    if gameover == False:
        jump_pixels = -65
        y_ball = y_ball + jump_pixels
    else:
        reset()

def timer_handler():
    global y_ball, jump_pixels, x_obs, obs_width, obs_height, gameover, score, max_score, button
    
    # ball touches the GROUND
    if y_ball > GROUND:
        timer.stop()
        gameover = True
        button.set_text('Reset')
    # check if ball touches top obstacle
    elif x_ball + 2*RADIUS_BALL > x_obs and x_ball < x_obs + obs_width and y_ball - RADIUS_BALL < obs_height:
        timer.stop()
        gameover = True
        button.set_text('Reset')
    # check if ball touches bottom obstacle
    elif x_ball + 2*RADIUS_BALL > x_obs and x_ball < x_obs + obs_width and y_ball + RADIUS_BALL > obs_height + gap:
        timer.stop()
        gameover = True
        button.set_text('Reset')
    else:
        jump_pixels = 4
        y_ball = y_ball + jump_pixels
        x_obs = x_obs - obs_speed
        if x_ball > x_obs + 20:
            score = score + 1
            if score > max_score:
                max_score = score
            x_obs = CANVAS_WIDTH
            obs_height = random.randint(50, 250) # length of obstacle
            obs_width = random.randint(50, 75)
    
# draw handler
def draw(canvas):
    global y_ball, jump_pixels, x_obs, obs_width, obs_height, gameover
    
    canvas.draw_line([x_obs,0], [x_obs,obs_height], obs_width, "Green") #top obstacle
    canvas.draw_line([x_obs,y_obs], [x_obs,obs_height+gap], obs_width, "Green") #bottom obstacle        
    canvas.draw_circle([x_ball,y_ball], RADIUS_BALL, 1, "White", "White")
    

    if gameover == True:
        canvas.draw_text("Game Over", [CANVAS_WIDTH/2,CANVAS_HEIGHT/2], 50, "Red")    
    
    '''
    if gameover == False:
        canvas.draw_line([x_obs,0], [x_obs,obs_height], obs_width, "Green") #top obstacle
        canvas.draw_line([x_obs,y_obs], [x_obs,obs_height+gap], obs_width, "Green") #bottom obstacle        
        canvas.draw_circle([x_ball,y_ball], RADIUS_BALL, 1, "White", "White")
    else:
        canvas.draw_line([x_obs,0], [x_obs,obs_height], obs_width, "Green") #top obstacle
        canvas.draw_line([x_obs,y_obs], [x_obs,obs_height+gap], obs_width, "Green") #bottom obstacle        
        canvas.draw_circle([x_ball-RADIUS_BALL,GROUND], RADIUS_BALL, 1, "White", "White")
        canvas.draw_text("Game Over", [CANVAS_WIDTH/2,CANVAS_HEIGHT/2], 50, "Red")       
    '''
    
    canvas.draw_text("Max Score = "+str(max_score), [40,30], 25, "Aqua")
    canvas.draw_text("Score = "+str(score), [40,60], 25, "Orange")
    
# create frame
frame = simplegui.create_frame("Test", CANVAS_WIDTH, CANVAS_HEIGHT)

# register event handlers
button = frame.add_button("Tap", tap, 100)

timer = simplegui.create_timer(25, timer_handler)
frame.set_draw_handler(draw)

#start frame and timer
frame.start()
timer.start()