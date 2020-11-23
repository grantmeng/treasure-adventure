import pygame
from config import *

class Coin(pygame.sprite.Sprite):
    def __init__(self,row,col,filename,dx,dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(filename),(GRID_SIZE,GRID_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = dx
        self.rect.y = dy
        self.row = row
        self.col = col
    
    def draw(self,screen):
        screen.blit(self.image, self.rect)

    def remove(self,board,boardview):
        boardview[self.row][self.col] = WHITE
        board.board[self.row][self.col].coins = 0
