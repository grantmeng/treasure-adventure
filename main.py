#!/usr/bin/python3

import pygame
import pygame_widgets as pw
import os
import random
from boardgame import Board
from player import Player
from coin import Coin
from config import *

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE + SCORE_HEIGHT))
pygame.display.set_caption("Treasure Search Adventure")

# Sounds
pygame.mixer.init()
bg_sound = pygame.mixer.Sound('bg.ogg')
#bg_sound.play()
eat_sound = pygame.mixer.Sound('eat.ogg')
win_sound = pygame.mixer.Sound('win.ogg')

# Set font/text for coins
font = pygame.font.SysFont('arial', 20)
def updateCoins(coins=0):
    text = font.render('Coins: {}'.format(coins), True, BLACK)
    screen.blit(text, [10, (GRID_SIZE+GRID_MARGIN) * GRID_NUM + GRID_MARGIN * 2, BOARD_SIZE, SCORE_HEIGHT])
def updateResult(msg):
    text = font.render(msg, True, BLACK)
    screen.blit(text, [10, (GRID_SIZE+GRID_MARGIN) * GRID_NUM + GRID_MARGIN * 10, BOARD_SIZE, SCORE_HEIGHT])
def drawCoin(rect):
    coin = pygame.transform.scale(pygame.image.load('./coin.jpg'),(GRID_SIZE,GRID_SIZE))
    screen.blit(coin, rect)

# Restart button
restart = pw.Button(
        screen, GRID_SIZE * (GRID_NUM-3), (GRID_SIZE+GRID_MARGIN) * GRID_NUM + GRID_MARGIN * 4, 90, 30, text='Restart',
        fontSize=20, margin=10, inactiveColour=GREEN, pressedColour=BLUE, radius=5,
        onClick=lambda: start())
# Quit button
quit = pw.Button(
        screen, GRID_SIZE * (GRID_NUM-1), (GRID_SIZE+GRID_MARGIN) * GRID_NUM + GRID_MARGIN * 4, 50, 30, text='Quit',
        fontSize=20, margin=10, inactiveColour=GREEN, pressedColour=BLUE, radius=5,
        onClick=lambda: exit())


def start():
    # Create board and players
    board = Board(GRID_NUM, RATIO)
    searcher = Player("Searcher", 0, 0,"./searcher.png",2,0)
    monster = Player("Monster", GRID_NUM-1, GRID_NUM-1,"./monster.jpg",BOARD_SIZE-50,BOARD_SIZE-50)
    board.board[searcher.row][searcher.col].players.append(searcher.name)
    board.board[monster.row][monster.col].players.append(monster.name)
    players = [searcher,monster]
    done = False

    # Create board view
    boardview = [ [WHITE for col in range(GRID_NUM)] for row in range(GRID_NUM) ]
    scoreview = pygame.Rect(GRID_MARGIN, (GRID_SIZE+GRID_MARGIN) * GRID_NUM + GRID_MARGIN, BOARD_SIZE, SCORE_HEIGHT)
    searcher.collectCoin(board)

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
            ### player meets monster
            if player.row == monster.row and player.col == monster.col:
                monsterEatPlayer(player)
                return
            player.collectCoin(board)
            ### player collected all the coins
            if searcher.coins >= int(GRID_NUM * GRID_NUM * RATIO):
                win_sound.play()
                updateResult('You win!')
                restart.draw()
                return
            if distanceToMonster(player) <= GRID_NUM * 2 // 4:
                monsterSmartMove(player)
            else: monsterRandomMove()
            ### player meets monster
            if player.row == monster.row and player.col == monster.col:
                monsterEatPlayer(player)
        else: print("Invalid Move")

    def monsterEatPlayer(player):
        eat_sound.play()
        updateResult('You lose!')
        restart.draw()

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

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

        # Restart listener
        restart.listen(pygame.event.get())
        # Quit listener
        quit.listen(pygame.event.get())

        # Draw the board
        for row in range(GRID_NUM):
            for col in range(GRID_NUM):
                pygame.draw.rect(screen,
                                 WHITE,
                                 [(GRID_MARGIN + GRID_SIZE) * col + GRID_MARGIN,
                                  (GRID_MARGIN + GRID_SIZE) * row + GRID_MARGIN,
                                  GRID_SIZE,
                                  GRID_SIZE])
                if board.board[row][col].coins:
                    coin = Coin(row, col, "./coin.jpg", (GRID_MARGIN+GRID_SIZE)*col+GRID_MARGIN, (GRID_MARGIN+GRID_SIZE)*row+GRID_MARGIN)
                    coin.draw(screen)

        # Draw searcher and monster
        searcher.draw(screen)
        monster.draw(screen)

        # Draw score board and quit button 
        pygame.draw.rect(screen, WHITE, scoreview)
        updateCoins(searcher.coins)
        quit.draw()

        ### player meets monster
        if searcher.row == monster.row and searcher.col == monster.col:
            updateResult('You lose!')
            restart.draw()
        ### player collected all the coins
        elif searcher.coins >= int(GRID_NUM * GRID_NUM * RATIO):
            updateResult('You win!')
            restart.draw()

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

# Start the game
start()

# Be IDLE friendly. If you forget this line, the program will 'hang' on exit.
pygame.quit()
