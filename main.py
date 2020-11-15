import pygame
from boardgame import Board
from player import Player


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define board/grid size
GRID_NUM = 10 # each row/colum
GRID_SIZE = 50
GRID_MARGIN = 3
BOARD_SIZE = GRID_NUM * GRID_SIZE + GRID_NUM * GRID_MARGIN
RATIO = 1/3

board = Board(GRID_NUM, RATIO)
searcher = Player("Searcher", 0, 0)
monster = Player("Monster", GRID_NUM-1, GRID_NUM-1)
board.board[searcher.row][searcher.col].players.append(searcher.name)
board.board[monster.row][monster.col].players.append(monster.name)
searcher.collectCoin(board)

# Create a 2 dimensional array. A two dimensional
boardview = [ [GREEN if board.board[row][col].coins == 1 else WHITE for col in range(GRID_NUM)] for row in range(GRID_NUM) ]
for row in boardview: print(row)
boardview[searcher.row][searcher.col] = BLUE
boardview[monster.row][monster.col] = RED

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
pygame.display.set_caption("Treasure Search Adventure")

# Set font/text
font = pygame.font.SysFont('arial', 20)
text = font.render('Hello', True, BLACK)
#rect = text.get_rect()
#screen.blit(text, ((GRID_MARGIN + GRID_SIZE) * col + GRID_MARGIN, (GRID_MARGIN + GRID_SIZE) * row + GRID_MARGIN))

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

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
            ### searcher is moving
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                boardview[searcher.row][searcher.col] = WHITE
                if event.key == pygame.K_UP:
                    searcher.moveUp(board)
                elif event.key == pygame.K_DOWN:
                    searcher.moveDown(board)
                elif event.key == pygame.K_LEFT:
                    searcher.moveLeft(board)
                elif event.key == pygame.K_RIGHT:
                    searcher.moveRight(board)
                boardview[searcher.row][searcher.col] = BLUE
            elif event.key in (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d):
                boardview[monster.row][monster.col] = WHITE
                if event.key == pygame.K_w:
                    monster.moveUp(board)
                elif event.key == pygame.K_s:
                    monster.moveDown(board)
                elif event.key == pygame.K_a:
                    monster.moveLeft(board)
                elif event.key == pygame.K_d:
                    monster.moveRight(board)
                boardview[monster.row][monster.col] = RED


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

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang' on exit.
pygame.quit()
