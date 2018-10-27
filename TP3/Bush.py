### Berry Bushes class

from random import *
from tkinter import *

class Bush(object):
    def __init__(self, data, margin=0):
        self.berries=randint(0, 5) 
        #150 wide and 200 long
        # starts at 51, 52, 53, 54, 55, 56
        self.images=[PhotoImage(file='images/0berries.png'),
            PhotoImage(file='images/1berry.png'), PhotoImage(file='images/2berries.png'),
            PhotoImage(file='images/3berries.png'), PhotoImage(file='images/4berries.png'),
            PhotoImage(file='images/5berries.png')]
        self.probability=0.4
        if margin == 0: self.margin=randrange(250, 3001, 150)
        else: self.margin=margin
        self.x=data.forest1X+self.margin
        self.y=data.height-140
    
    def collect(self, data):
        data.player.inventory['Berries'] += self.berries
        self.berries=0
        data.player.hunger -= 3
    
    def __repr__(self):
        return 'Bush(%d, %d): %d berries, image:%s' %(self.x, self.y, self.berries, str(self.images[self.berries]))
    
    def timerFired(self, data):
        self.x=data.forest1X+self.margin
        if random() < self.probability and data.timerCounter%500 == 0 and self.berries < 5: 
        #every 20 secs, there's a 40% chance that a bush grows back a berry
        #max 5 berries can grow on a bush
            self.berries += 1
    
    def __hash__(self):
        return hash(self.margin)
    
    def __eq__(self, other):
        return isinstance(other, Bush) and self.margin == other.margin
    
    def draw(self, canvas, data):
        if self.berries == 0:
            canvas.create_image(self.x, self.y, image=self.images[0])
        else:
            canvas.create_image(self.x, self.y, image=self.images[self.berries])
    