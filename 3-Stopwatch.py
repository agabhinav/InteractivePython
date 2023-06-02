# template for "Stopwatch: The Game"

import simplegui
import time

# define global variables
timer_interval = 100 #timer with an associated interval of 0.1 seconds
counter = 0
A=0
B=0
C=0
D=0

stops_successful = 0
stops_total = 0

is_running = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global A, B, C, D
    
    A = t // 600 # t//10 gives seconds, divide that by 60 to get mins
    tmp_sec = (t//10) % 60 # t//10 gives whole seconds, % 60 to get seconds less than 1 min
    B = tmp_sec // 10 # get tens digit
    C = tmp_sec % 10 # get ones digit
    D = t % 10
            
    result = str(A) + ":" + str(B) + str(C) + "." + str(D)
    
    return result
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global is_running    
    if is_running == False:
        timer.start()
        is_running = True

def stop():
    global counter, stops_successful, stops_total, is_running
    
    if is_running == True:
        timer.stop()
        
        stops_total = stops_total + 1
        # update_score()
        if (counter % 10) == 0:
            stops_successful = stops_successful + 1
        
        is_running = False

# stop the timer and reset the current time to zero    
def reset():
    global counter, stops_successful, stops_total, is_running
    timer.stop()
    is_running = False
    counter = 0
    stops_successful = 0
    stops_total = 0    

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global counter
    if counter == 5999: # reset to 0 after 9:59.9
        counter = 0
    else:
        counter = counter + 1
    #print counter

# define draw handler
def draw(canvas):
    global counter, stops_successful, stops_total
    #result = format(counter)
    #print frame.get_canvas_textwidth(result, 50)
    
    canvas.draw_text(format(counter), [137,170], 55, "White")
    
    score = str(stops_successful) + "/" + str(stops_total)
    canvas.draw_text("Success/Attempts", [250, 30], 20, "Orange")
    canvas.draw_text(score, [300, 65], 35, "Aqua")
    
# create frame
frame = simplegui.create_frame("Stopwatch", 400, 300)

# register event handlers
timer = simplegui.create_timer(timer_interval, timer_handler)
frame.set_draw_handler(draw)
button_start = frame.add_button("Start", start, 100)
button_stop = frame.add_button("Stop", stop, 100)
button_reset = frame.add_button("Reset", reset, 100)

# start frame
frame.start()

# Please remember to review the grading rubric
