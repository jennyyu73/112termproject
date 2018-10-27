######## Trap class

from random import *
from tkinter import *

class Trap(object):
    def __init__(self, x, data):
        #traps are 50x50 in size
        self.x=x
        self.y=data.height-40
        self.margin=self.x-data.forest1X
        self.probability=0.2
        self.caughtPrey=False
        self.image=PhotoImage(file='images/trap.png')
    
    def timerFired(self, data):
        self.x=data.forest1X+self.margin
        if random() < self.probability and data.timerCounter%500 == 0:
            self.caughtPrey=True
    
    def draw(self, canvas):
        canvas.create_image(self.x, self.y, image=self.image)
    
    def collect(self, data):
        data.player.inventory['Prey Caught'] += 1
        self.caughtPrey=False
        data.player.hunger -= 5
        data.player.thirst -= 5