###### Grass class

from random import *
from tkinter import *

class Grass(object):
    def __init__(self, data, margin=0):
        #50x50 size
        self.hasGrass=True
        self.probability=0.3
        if margin == 0: self.margin=randrange(3050, 5500, 50)
        else: self.margin=margin
        self.x=data.forest1X+self.margin
        self.y=data.height-70
        self.grassImage=PhotoImage(file='images/hasGrass.png')
        self.noGrassImage=PhotoImage(file='images/noGrass.png')
    
    def timerFired(self, data):
        if random() < self.probability and data.timerCounter%500 == 0 and\
        self.hasGrass == False:
            self.hasGrass=True
        self.x=data.forest1X+self.margin
    
    def draw(self, canvas):
        if self.hasGrass == False:
            canvas.create_image(self.x, self.y, image=self.noGrassImage)
        else:
            canvas.create_image(self.x, self.y, image=self.grassImage)
    
    def __hash__(self):
        return hash(self.margin)
    
    def __eq__(self, other):
        return isinstance(other, Grass) and self.margin == other.margin
    
    def collect(self, data):
        self.hasGrass=False
        data.player.inventory['Grass'] += 1
        data.player.hunger -= 1
        data.player.thirst -= 1
        
    def __repr__(self):
        return 'Grass: %s' %(str(self.hasGrass))