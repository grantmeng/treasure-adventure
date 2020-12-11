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
bg_sound.set_volume(0.2)
bg_sound.play(-1) # infinite play
#bg_sound.fadeout(5000) # fade out in 5 sec
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
    searcher = Player("Searcher", 0, 0,"./searcher.png",3,3)
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
                eat_sound.play()
                return
            player.collectCoin(board)
            if distanceToMonster(player) <= GRID_NUM * 2 // 4:
                monsterSmartMove(player)
            else: monsterRandomMove()
            ### player meets monster
            if player.row == monster.row and player.col == monster.col:
                eat_sound.play()
        else: print("Invalid Move")

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    end = False
    max = 3
    curshow = []
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:
                done = True
                break
            if not end: 
                if event.type == pygame.MOUSEBUTTONDOWN and len(curshow) != max:
                    # User clicks the mouse. Reveal the tile underneath
                    pos = pygame.mouse.get_pos()
                    # Change the x/y screen coordinates to grid coordinates
                    col = pos[0] // (GRID_SIZE + GRID_MARGIN)
                    row = pos[1] // (GRID_SIZE + GRID_MARGIN)
                    if row < GRID_NUM and col < GRID_NUM and [row,col] not in curshow:
                        curshow.append([row,col])   
                        board.board[row][col].show = True
                elif event.type == pygame.KEYDOWN: #and len(curshow) == 3: #may delete second condition for better user experience.
                    ### player is moving
                    moveInput(searcher)
                    for n in curshow:
                        board.board[n[0]][n[1]].show = False
                    curshow = []

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
                if board.board[row][col].show:
                    #If both monster and coin, shows half and half picture
                    if row == monster.row and col == monster.col and board.board[row][col].coins:
                        coin = Coin(row, col, "./monstercoin.jpg", (GRID_MARGIN+GRID_SIZE)*col+GRID_MARGIN, (GRID_MARGIN+GRID_SIZE)*row+GRID_MARGIN)
                        coin.draw(screen)  
                    elif row == monster.row and col == monster.col: 
                        monster.draw(screen)
                    elif board.board[row][col].coins:
                        coin = Coin(row, col, "./coin.jpg", (GRID_MARGIN+GRID_SIZE)*col+GRID_MARGIN, (GRID_MARGIN+GRID_SIZE)*row+GRID_MARGIN)
                        coin.draw(screen)       
        # Draw searcher
        searcher.draw(screen)
        
        # Draw score board and quit button 
        pygame.draw.rect(screen, WHITE, scoreview)
        updateCoins(searcher.coins)
        restart.draw()
        quit.draw()

        ### player collected all the coins
        if searcher.coins >= int(GRID_NUM * GRID_NUM * RATIO * RATIO):
            updateResult('You win!')
            end = True
        ### player meets monster
        elif searcher.row == monster.row and searcher.col == monster.col:
            updateResult('You lose!')
            end = True

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

# Start the game
start()

# Be IDLE friendly. If you forget this line, the program will 'hang' on exit.
pygame.quit()
