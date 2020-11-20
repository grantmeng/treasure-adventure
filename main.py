#!/usr/bin/python3

import pygame
import pygame_widgets as pw
import random
from boardgame import Board
from player import Player
from config import *

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE + SCORE_HEIGHT))
pygame.display.set_caption("Treasure Search Adventure")

# Set font/text for coins
font = pygame.font.SysFont('arial', 20)
def updateCoins(coins=0):
    text = font.render('Coins: {}'.format(coins), True, BLACK)
    screen.blit(text, [10, (GRID_SIZE+GRID_MARGIN) * GRID_NUM + GRID_MARGIN * 2, BOARD_SIZE, SCORE_HEIGHT])
def updateResult(msg):
    text = font.render(msg, True, BLACK)
    screen.blit(text, [10, (GRID_SIZE+GRID_MARGIN) * GRID_NUM + GRID_MARGIN * 10, BOARD_SIZE, SCORE_HEIGHT])

# Restart button
restart = pw.Button(
        screen, GRID_SIZE * (GRID_NUM-2), (GRID_SIZE+GRID_MARGIN) * GRID_NUM + GRID_MARGIN * 4, 90, 30, text='Restart',
        fontSize=20, margin=10, inactiveColour=GREEN, pressedColour=BLUE, radius=5,
        onClick=lambda: start())

def start():
    # Create board and players
    board = Board(GRID_NUM, RATIO)
    searcher = Player("Searcher", 0, 0,"./searcher.png",0,0)
    monster = Player("Monster", GRID_NUM-1, GRID_NUM-1,"./monster.jpg",BOARD_SIZE-50,BOARD_SIZE-50)
    board.board[searcher.row][searcher.col].players.append(searcher.name)
    board.board[monster.row][monster.col].players.append(monster.name)
    players = [searcher,monster]

    # Create board view
    boardview = [ [GOLD if board.board[row][col].coins == 1 else WHITE for col in range(GRID_NUM)] for row in range(GRID_NUM) ]
    scoreview = pygame.Rect(GRID_MARGIN, (GRID_SIZE+GRID_MARGIN) * GRID_NUM + GRID_MARGIN, BOARD_SIZE, SCORE_HEIGHT)
    searcher.collectCoin(board,boardview)

    def distanceToMonster(player):
        return abs(player.row - monster.row) + abs(player.col - monster.col)

    def monsterRandomMove():
        rand = random.randint(0, 3)
        if rand == 0: monster.moveUp(board)
        elif rand == 1: monster.moveDown(board)
        elif rand == 2: monster.moveLeft(board)
        elif rand == 3: monster.moveRight(board)

    def monsterSmartMove(player):
        if abs(monster.row - player.row) > abs(monster.col - player.col): # monster move on x axis
            if monster.row < player.row: monster.moveDown(board)
            else: monster.moveUp(board)
        else: # monster move on y axis
            if monster.col < player.col: monster.moveRight(board)
            else: monster.moveLeft(board)

    def moveInput(player):
        m = event.key
        if player.move(m,board): 
            player.collectCoin(board,boardview)
            if distanceToMonster(player) <= GRID_NUM * 2 // 4:
                monsterSmartMove(player)
            else: monsterRandomMove()
        else: print("Invalid Move")

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    done = False
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:
                done = True
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                col = pos[0] // (GRID_SIZE + GRID_MARGIN)
                row = pos[1] // (GRID_SIZE + GRID_MARGIN)
                print("Click ", pos, "Grid coordinates: ", row, col)
            elif event.type == pygame.KEYDOWN:
                ### player is moving
                moveInput(searcher)

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

        # Draw score board 
        pygame.draw.rect(screen, WHITE, scoreview)
        updateCoins(searcher.coins)

        ### player meets monster
        if searcher.row == monster.row and searcher.col == monster.col:
            updateResult('You lose!')
            restart.draw()
        ### player collected all the coins
        elif searcher.coins == int(GRID_NUM * GRID_NUM * RATIO):
            updateResult('You win!')
            restart.draw()

        restart.listen(pygame.event.get())

        # Draw searcher and monster
        searcher.draw(screen)
        monster.draw(screen)

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

# Start the game
start()

# Be IDLE friendly. If you forget this line, the program will 'hang' on exit.
pygame.quit()
