import pygame
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self,name,row,col,filename,dx,dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(filename),(GRID_SIZE,GRID_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = dx
        self.rect.y = dy
        self.name = name
        self.row = row
        self.col = col
        self.coins = 0
    
    def draw(self,screen):
        screen.blit(self.image, self.rect)

    def moveUp(self,board):
        if self.row == 0: return False
        board.board[self.row][self.col].players.remove(self.name)
        self.row -= 1
        self.rect.y -= GRID_SIZE+GRID_MARGIN
        board.board[self.row][self.col].players.append(self.name)
        return True

    def moveDown(self,board):
        if self.row == board.size-1: return False
        board.board[self.row][self.col].players.remove(self.name)
        self.row += 1
        self.rect.y += GRID_SIZE+GRID_MARGIN
        board.board[self.row][self.col].players.append(self.name)
        return True

    def moveRight(self,board):
        if self.col == board.size-1: return False
        board.board[self.row][self.col].players.remove(self.name)
        self.col += 1
        self.rect.x += GRID_SIZE+GRID_MARGIN
        board.board[self.row][self.col].players.append(self.name)
        return True

    def moveLeft(self,board):
        if self.col == 0: return False
        board.board[self.row][self.col].players.remove(self.name)
        self.col -= 1
        self.rect.x -= GRID_SIZE+GRID_MARGIN
        board.board[self.row][self.col].players.append(self.name)
        return True

    def move(self,m,board): 
        if m == pygame.K_UP:
            return self.moveUp(board)
        elif m == pygame.K_DOWN:
            return self.moveDown(board)
        elif m == pygame.K_LEFT:
            return self.moveLeft(board)
        elif m == pygame.K_RIGHT:
            return self.moveRight(board)
        return False

    def collectCoin(self,board,boardview):
        if self.name == "Searcher":
            self.coins += board.board[self.row][self.col].coins
            boardview[self.row][self.col] = WHITE
            board.board[self.row][self.col].coins = 0

    def __str__(self):
        return '{}: {}'.format(self.name,self.coins)