import pygame
import time
import numpy as np
from checker import main_checker 
from backtrack_solver import valid,empty_cell
from new_boards import *

pygame.init()

display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("SUDOKU")
clock = pygame.time.Clock()


# defining colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
i_red = (210, 0, 0)
green = (0, 255, 0)
i_green = (0, 210, 0)

background = (255, 255, 255)
highlight = (242, 240, 104)

new_color = (3, 252, 248)
i_new_color = (3, 215, 252)
reset_color = (252, 3, 169)
i_reset_color = (239, 142, 250)
solve_color = (250, 155, 2)
i_solve_color = (245, 177, 88)
hint_color = (3, 44, 252)
i_hint_color = (90, 117, 250)
quit_color = (252, 0, 0)
i_quit_color = (210, 0, 0)


box_size = 50
button_width = 100
button_height = 50
top_margin = (display_height - 9*box_size)/2 # top - bottom margin
side_margin = (display_width - 9*box_size - 2*button_width)/4 # left - right margin
button_y = (display_height - 3*button_height)/4
button_x = 9*box_size + 2*side_margin

checker_asked = False
board_solved = False


ques_board = [
    [4,8,0,0,0,0,2,0,0],
    [5,3,7,2,1,0,0,0,4],
    [0,0,0,0,0,0,0,3,0],
    [0,0,2,0,7,0,1,0,3],
    [0,0,0,6,0,1,0,0,0],
    [9,0,8,0,3,0,5,0,0],
    [0,2,0,0,0,0,0,0,0],
    [7,0,0,0,2,8,6,9,1],
    [0,0,9,0,0,0,0,2,8]
]

curr_board = [
    [4,8,0,0,0,0,2,0,0],
    [5,3,7,2,1,0,0,0,4],
    [0,0,0,0,0,0,0,3,0],
    [0,0,2,0,7,0,1,0,3],
    [0,0,0,6,0,1,0,0,0],
    [9,0,8,0,3,0,5,0,0],
    [0,2,0,0,0,0,0,0,0],
    [7,0,0,0,2,8,6,9,1],
    [0,0,9,0,0,0,0,2,8]
]


def text_objects(msg, font, color):
	textSurf = font.render(msg, True, color)
	return textSurf, textSurf.get_rect()


def button(msg,x,y,w,h,inactive_c,active_c,text_color,action=None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	if x+w>mouse[0]>x and y+h>mouse[1]>y:
		pygame.draw.rect(gameDisplay, active_c, (x,y,w,h))
		if click[0]==1 and action!=None:
			action()
	else:
		pygame.draw.rect(gameDisplay, inactive_c, (x,y,w,h))

	smalltext = pygame.font.SysFont("comicsansms",20)
	textSurf, textRect = text_objects(msg,smalltext, text_color)
	textRect.center = (x+(w/2), y+(h/2) )
	gameDisplay.blit(textSurf, textRect)


def quit_game():
	pygame.quit()
	quit()


def draw_board(board):

	pygame.draw.rect(gameDisplay, white, (side_margin-5, top_margin-5, 9*box_size+10, 9*box_size+10))
	# TABLE INTERFACE
	largeText = pygame.font.SysFont('comicsansms', 40)

	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] != 0:
				if board[i][j] == ques_board[i][j]:
					pygame.draw.rect(gameDisplay, highlight, (side_margin+j*box_size, top_margin+i*box_size, box_size, box_size))

				TextSurf, TextRect = text_objects(str(board[i][j]), largeText, black)
				TextRect.center = (side_margin+j*box_size+box_size/2, top_margin+i*box_size+box_size/2)
				gameDisplay.blit(TextSurf, TextRect)	
			pygame.draw.rect(gameDisplay, black, (side_margin+j*box_size, top_margin+i*box_size, box_size, box_size), 1)

	# BOUNDARIES
	for i in range(3):
		for j in range(3):
			pygame.draw.rect(gameDisplay, black, (side_margin+3*j*box_size, top_margin+3*i*box_size, 3*box_size, 3*box_size), 4)	

	time.sleep(0.01)
	pygame.display.update()


# requires better copying syntax
def reset_board():
	global curr_board
	global board_solved
	global checker_asked
	curr_board = np.copy(np.array(list(ques_board)))
	checker_asked = False
	board_solved = False


def check_board():
	global checker_asked
	global board_solved

	checker_asked = True
	if main_checker(curr_board):
		board_solved = True
	else:
		board_solved = False


def modified_solver(board):
	if empty_cell(board) is None:
		curr_board = np.array(list(board))
		return True

	cell = empty_cell(board)
	r, c = cell
	t = valid(board, cell)
	np.random.shuffle(t)

	for i in t:
		board[r][c] = i

		draw_board(board)
	
		if modified_solver(board):
			return True

		draw_board(board)

		board[r][c] = 0

	return False


def board_solver():
	global curr_board
	curr_board = np.copy(ques_board)
	modified_solver(curr_board)


# def generate_new_puzzle():
# 	pass


# def generate_hint():
# 	pass


def main():
	global curr_board

	while True:
		mouse = pygame.mouse.get_pos()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit_game()
			if side_margin+9*box_size>mouse[0]>side_margin and top_margin+9*box_size>mouse[1]>top_margin:
				j = int((mouse[0]-side_margin)//box_size)
				i = int((mouse[1]-top_margin)//box_size)
				if event.type == pygame.KEYDOWN and ques_board[i][j] == 0:
					if event.key == pygame.K_BACKSPACE or event.key == pygame.K_0:
						curr_board[i][j] = 0
					elif event.key == pygame.K_1:
						curr_board[i][j] = 1
					elif event.key == pygame.K_2:
						curr_board[i][j] = 2
					elif event.key == pygame.K_3:
						curr_board[i][j] = 3
					elif event.key == pygame.K_4:
						curr_board[i][j] = 4
					elif event.key == pygame.K_5:
						curr_board[i][j] = 5
					elif event.key == pygame.K_6:
						curr_board[i][j] = 6
					elif event.key == pygame.K_7:
						curr_board[i][j] = 7
					elif event.key == pygame.K_8:
						curr_board[i][j] = 8
					elif event.key == pygame.K_9:
						curr_board[i][j] = 9

		# BUTTONS INTERFACE
		gameDisplay.fill(background)
		button("NEW",button_x, button_y, button_width, button_height, i_new_color, new_color, black, generate_new_puzzle)
		button("RESET",(button_x+button_width+side_margin), button_y, button_width, button_height, i_reset_color, reset_color, black, reset_board)		
		button("HINT",button_x, (3*button_y+2*button_height), button_width, button_height, i_hint_color, hint_color, black, generate_hint)
		button("QUIT",(button_x+button_width+side_margin), (3*button_y+2*button_height), button_width, button_height, i_quit_color, quit_color, black, quit_game)

		if checker_asked:
			if board_solved:
				button("CORRECT",button_x, (2*button_y+button_height), button_width, button_height, i_green, green, black, check_board)
			else:
				button("WRONG",button_x, (2*button_y+button_height), button_width, button_height, i_red, red, black, check_board)
		else:
			button("CHECK",button_x, (2*button_y+button_height), button_width, button_height, i_green, green, black, check_board)

		button("SOLVE",(button_x+button_width+side_margin), (2*button_y+button_height), button_width, button_height, i_solve_color, solve_color, black, board_solver)	
		draw_board(curr_board)
		
		clock.tick(60)

main()
