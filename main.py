import pygame
from boardgame import Board
from player import Player
from config import *
# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
pygame.display.set_caption("Treasure Search Adventure")

board = Board(GRID_NUM, RATIO)
searcher = Player("Searcher", 0, 0,"./searcher.png",0,0)
monster = Player("Monster", GRID_NUM-1, GRID_NUM-1,"./monster.jpg",BOARD_SIZE-50,BOARD_SIZE-50)
board.board[searcher.row][searcher.col].players.append(searcher.name)
board.board[monster.row][monster.col].players.append(monster.name)

players = [searcher,monster]
global curPlayer
curPlayer = 0

# Create a 2 dimensional array. A two dimensional
boardview = [ [GOLD if board.board[row][col].coins == 1 else WHITE for col in range(GRID_NUM)] for row in range(GRID_NUM) ]
searcher.collectCoin(board,boardview)

# Set font/text
font = pygame.font.SysFont('arial', 20)
text = font.render('Hello', True, BLACK)
#rect = text.get_rect()
#screen.blit(text, ((GRID_MARGIN + GRID_SIZE) * col + GRID_MARGIN, (GRID_MARGIN + GRID_SIZE) * row + GRID_MARGIN))

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

def moveInput(player):
    global curPlayer
    if players[curPlayer] != player: return
    print("{}'s turn.".format(player.name))
    m = event.key
    if player.move(m,board): 
        player.collectCoin(board,boardview)
        curPlayer = (curPlayer+1) % len(players)
    else: print("Invalid Move")

done = False
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT: done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            col = pos[0] // (GRID_SIZE + GRID_MARGIN)
            row = pos[1] // (GRID_SIZE + GRID_MARGIN)
            print("Click ", pos, "Grid coordinates: ", row, col)
        elif event.type == pygame.KEYDOWN:
            ### player is moving
            moveInput(players[curPlayer])

    # Set the screen background
    screen.fill(BLACK)

    # Draw the board
    for row in range(GRID_NUM):
        for col in range(GRID_NUM):
            color = boardview[row][col]
            pygame.draw.rect(screen,
                             color,
                             [(GRID_MARGIN + GRID_SIZE) * col + GRID_MARGIN,
                              (GRID_MARGIN + GRID_SIZE) * row + GRID_MARGIN,
                              GRID_SIZE,
                              GRID_SIZE])
    searcher.draw(screen)
    monster.draw(screen)
    pygame.display.update()

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang' on exit.
pygame.quit()
