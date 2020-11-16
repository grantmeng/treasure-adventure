import random
from pandas import *

class Room:
    def __init__(self,row,col):
        self.row = row
        self.col = col
        self.coins = 0
        self.players = []
        self.show = False

    def __str__(self):
        players = ",".join(p for p in self.players)
        if self.show:
            return '{},{}'.format(self.coins,players)
        return '[{}]'.format(players)

class Board:
    def __init__(self,size,ratio):
        self.size = size
        self.board = [[Room(i,j) for i in range(size)] for j in range(size)]
        self.ratio = ratio
        for c in random.sample([i for i in range(size*size)], int(size*size*ratio)):
            row,col = divmod(c,size)
            self.board[row][col].coins += 1
        
    def __str__(self):
        return str(DataFrame(self.board))

        


    
        
