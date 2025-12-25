import pygame as pg
import numpy as np

import numpy as np

board = np.zeros((15,15), dtype=int)
board[np.triu_indices(15, k=1)] = 5
board = np.flipud(board)

print(board)


####################################################################################################################
w_size = 720          # window size
pad = 36              # padding size
tri_span = 15         # number of lines on each side

####################################################################################################################
# Hex of different color
color_line = [153, 153, 153]
color_board = [241, 196, 15]
color_black = [0, 0, 0]
color_dark_gray = [75, 75, 75]
color_white = [255, 255, 255]
color_light_gray = [235, 235, 235]
color_red = [255, 0, 0]
color_green= [0, 255, 0]

####################################################################################################################
# create the initial empty chess board in the game window
def draw_board():
    
    global center, sep_x, sep_y, pad_x, pad_y, piece_radius

    sep_x = (w_size - 2*pad)/(tri_span-1)                     # horizontal separation between lines
    sep_y = sep_x*np.sqrt(3)/2                                # vertical separation between lines
    pad_x = pad
    pad_y = w_size/2 - (w_size - 2*pad)*np.sqrt(3)/4
    piece_radius = sep_x*0.3                                  # size of a chess piece

    surface = pg.display.set_mode((w_size, w_size))
    pg.display.set_caption("Gomuku (a.k.a Five-in-a-Row)")
    surface.fill(color_board)

        
    for i in range(tri_span-1):
        pg.draw.line(surface, color_line, (pad+i*sep_x/2, pad_y+i*sep_y),
                     (w_size-pad-i*sep_x/2, pad_y+i*sep_y), 3)
        
        pg.draw.line(surface, color_line, (pad_x+i*sep_x, pad_y),
                     (w_size-pad-(tri_span-i-1)*sep_x/2, pad_y+(tri_span-i-1)*sep_y), 3)
        
        pg.draw.line(surface, color_line, (w_size-pad_x-i*sep_x, pad_y),
                     (pad+(tri_span-i-1)*sep_x/2, pad_y+(tri_span-i-1)*sep_y), 3)

    pg.display.update()
    
    return surface


####################################################################################################################
# translate clicking position on the window to rectangular board indices (u, v)
# pos = (x,y) is a tuple returned by pygame, telling where an event (i.e. player click) occurs on the game window
def click2index(pos):
    
    # check if the clicked position is on the grid
    if ((pos[1]>pad_y-piece_radius) and 
        (pos[0]-pad_x)>(pos[1]-pad_y-piece_radius)/np.sqrt(3) and 
        (pos[0]-w_size+pad_x)<(pad_y+piece_radius-pos[1])/np.sqrt(3)):    

        # return the closest corresponding indices (u,v) on the rectangular representation
        u = round((pos[1]-pad_y)/sep_y)
        v = round((pos[0]-pad_x-u*sep_x/2)/sep_x)
        return (u,v) 
    
    return False    # return False if the clicked position is outside the grid
        
        
        
####################################################################################################################
# Draw the stones on the board at pos = [u, v]
# u and v are the indices on the 15x15 board array (under rectangular grid representation)
# Draw a black circle at pos if color = 1, and white circle at pos if color =  -1

def draw_stone(surface, pos, color=0):
    
    # translate (u, v) indices to xy coordinate on the game window
    x = pad_x+pos[0]*sep_x/2+pos[1]*sep_x
    y = pad_y+pos[0]*sep_y

    if color==1:
        pg.draw.circle(surface, color_black, [x, y], piece_radius, 0)
        pg.draw.circle(surface, color_dark_gray, [x, y], piece_radius, 2)
                
    elif color==-1:
        pg.draw.circle(surface, color_white, [x, y], piece_radius, 0)
        pg.draw.circle(surface, color_light_gray, [x, y], piece_radius, 2)
        
    pg.display.update()


def draw_highlighted_stone(surface, pos, color=0):
    
    # translate (u, v) indices to xy coordinate on the game window
    x = pad_x+pos[0]*sep_x/2+pos[1]*sep_x
    y = pad_y+pos[0]*sep_y
    
    if color==1:
        pg.draw.circle(surface, color_black, [x, y], piece_radius, 0)
        pg.draw.circle(surface, color_red, [x, y], piece_radius, 3)
                
    elif color==-1:
        pg.draw.circle(surface, color_white, [x, y], piece_radius, 0)
        pg.draw.circle(surface, color_red, [x, y], piece_radius, 3)
        
    elif color==2:
        pg.draw.circle(surface, color_black, [x, y], piece_radius, 0)
        pg.draw.circle(surface, color_green, [x, y], piece_radius, 3)
                
    elif color==-2:
        pg.draw.circle(surface, color_white, [x, y], piece_radius, 0)
        pg.draw.circle(surface, color_green, [x, y], piece_radius, 3)
        
    pg.display.update()
    

####################################################################################################################
# print text on upper left corner
def print_text(surface, msg, color=color_line):
    
    # erase any previous text by covering the area with a rectangle with the same colour as the background
    pg.draw.rect(surface, color_board, pg.Rect(0,0,w_size, pad_y-piece_radius-5), 0)
    
    font = pg.font.Font('freesansbold.ttf', 32)
    text = font.render(msg, True, color)
    textRect = text.get_rect()
    textRect.topleft = (0, 0)
    surface.blit(text, textRect)
    pg.display.update()


def print_winner(surface, winner=0):
    if winner == 2:
        msg = "Draw! So White wins"
        color = color_line
    elif winner == 1:
        msg = "Black wins!"
        color = color_black
    elif winner == -1:
        msg = 'White wins!'
        color = color_white
    else:
        return

    print_text(surface, msg, color)


# display whose current turn is
def print_turn(surface, turn=0):
    
    if turn == 1:
        msg = "Black's turn"
        color = color_black
    elif turn == -1:
        msg = "White's turn"
        color = color_white
    else:
        return
    
    print_text(surface, msg, color)


####################################################################################################################
# a dummy check winner function
def check_winner(board):
    return 0

# a fancier check winner function which also hightlight the winning chain
def hightlight_winner(surface, board, gameover):
    pass 

####################################################################################################################
# a random move generator
def random_move(board, color):
    
    while True:
        indx = (np.random.randint(15), np.random.randint(15))
        if board[indx] == 0:
            return indx


