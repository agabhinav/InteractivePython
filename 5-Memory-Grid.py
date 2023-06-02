import simplegui
import random

LAYOUT = (8, 2)
COLS = LAYOUT[0]
ROWS = LAYOUT[1]
TILE_WIDTH = 50
TILE_HEIGHT = 100
HALF_TILE_WIDTH = TILE_WIDTH // 2
HALF_TILE_HEIGHT = TILE_HEIGHT // 2
FONT_SIZE = TILE_WIDTH // 2

WIDTH = TILE_WIDTH * COLS
HEIGHT = TILE_HEIGHT * ROWS

num_tiles = ROWS * COLS

# helper function to check if a number if odd
def is_odd(num):
    if num % 2 != 0:
        return True
    return False

# start new game
def new_game():
    global num_tiles, tiles, matrix, matrix, state, exposed, turn, pairs, paired
    state = 0
    tiles = []
    turn = 0		        
    pairs = 0
    label.set_text("Turns = " + str(turn))
    label_pairs.set_text("Pairs = " + str(pairs))
    tiles += range(num_tiles // 2) + range(num_tiles // 2)
    
    random.shuffle(tiles)
    
    exposed = [False] * len(tiles) # initialize exposed to False for all tiles
    paired = [False] * len(tiles)
    
    # if number of tiles is odd, append 'X' at the end of tiles[] and True at the end of exposed[]
    # this is done so that 'X' is always visible in last spot in case of odd number of tiles
    if is_odd(num_tiles):        
        tiles.append("X")
        exposed.append(True)
        paired.append(True)
    print "Tiles List = ", tiles    
    
    # (x,y) matrix for each tile in tiles[]
    matrix = []
    for i in range(len(tiles)):
        matrix += [[i//COLS, i % COLS]] # index // cols = row, index % cols = column
    
    print "Matrix = ", matrix

# define event handlers
def mouseclick(pos):
    global matrix, state, exposed, turn, tiles, index1, index2, pairs, paired
    
    click_coord = [pos[1] // TILE_HEIGHT, pos[0] // TILE_WIDTH]
    tile_index = matrix.index(click_coord)
    print "Mouse clicked at position ", pos, "and click coordinate = ",click_coord," tile index =", tile_index
    
    if state == 0: # new game
        state = 1
        exposed[tile_index] = True
        index1 = tile_index # store index of 1st tile clicked in a variable index1
    elif state == 1 and not exposed[tile_index]: # State 1 corresponds to a single exposed unpaired tile
        state = 2
        exposed[tile_index] = True
        index2 = tile_index # store index of 2nd tile clicked, in a given turn, in a variable index2
        turn += 1
        label.set_text("Turns = " + str(turn))
        
        if tiles[index1] == tiles[index2]:
            pairs += 1
            label_pairs.set_text("Pairs = " + str(pairs))
            paired[index1] = True
            paired[index2] = True
    else:
        if not exposed[tile_index]:
            if tiles[index1] != tiles[index2]: # turn over the previous two unpaired cards
                exposed[index1] = False
                exposed[index2] = False

            exposed[tile_index] = True # expose the card just clicked
            state = 1
            index1 = tile_index # store index of 1st tile clicked, in subsequent turn, in a variable index1
    
def draw(canvas):
    global tiles
    for i in range(len(tiles)):
        if exposed[i] and not paired[i]:          
            canvas.draw_text(str(tiles[i]), [(HALF_TILE_WIDTH + TILE_WIDTH * (i % COLS)) - frame.get_canvas_textwidth(str(tiles[i]), FONT_SIZE)//2, 
                                             HALF_TILE_HEIGHT + TILE_HEIGHT * (i // COLS)], FONT_SIZE, "White")
        elif exposed[i] and paired[i]:
            canvas.draw_polygon([[TILE_WIDTH * (i % COLS), TILE_HEIGHT * (i // COLS)], 
                                 [TILE_WIDTH * (i % COLS) + TILE_WIDTH, TILE_HEIGHT * (i // COLS)], 
                                 [TILE_WIDTH * (i % COLS) + TILE_WIDTH, TILE_HEIGHT * (i // COLS) + TILE_HEIGHT], 
                                 [TILE_WIDTH * (i % COLS), TILE_HEIGHT * (i // COLS) + TILE_HEIGHT]], 
                                1, "White", "Grey")
            canvas.draw_text(str(tiles[i]), [(HALF_TILE_WIDTH + TILE_WIDTH * (i % COLS)) - frame.get_canvas_textwidth(str(tiles[i]), FONT_SIZE)//2, 
                                             HALF_TILE_HEIGHT + TILE_HEIGHT * (i // COLS)], FONT_SIZE, "White")
            
        else:
            canvas.draw_polygon([[TILE_WIDTH * (i % COLS), TILE_HEIGHT * (i // COLS)], 
                                 [TILE_WIDTH * (i % COLS) + TILE_WIDTH, TILE_HEIGHT * (i // COLS)], 
                                 [TILE_WIDTH * (i % COLS) + TILE_WIDTH, TILE_HEIGHT * (i // COLS) + TILE_HEIGHT], 
                                 [TILE_WIDTH * (i % COLS), TILE_HEIGHT * (i // COLS) + TILE_HEIGHT]], 
                                1, "White", "Green")
        
        canvas.draw_line([TILE_WIDTH * i, 0], [TILE_WIDTH * i, HEIGHT], 1, "White")
        canvas.draw_line([0, TILE_HEIGHT * i], [WIDTH, TILE_HEIGHT * i], 1, "White")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")
label_pairs = frame.add_label("Pairs = 0")
# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start() 