### Class for playable character

from tkinter import *

class Character(object):
    buildRecipe={'Rope':{'Grass':5}, 'Trap':{'Rope': 10, 'Grass': 5, 'Wood': 1}, 
        'Torch':{'Rope': 2, 'Wood': 1}}
    
    def __init__(self, name, data):
        self.name=name
        self.health=100
        self.thirst=100
        self.hunger=100
        self.images={'standingR':PhotoImage(file='images/%s/standingR.png' % self.name), 
                    'standingL': PhotoImage(file='images/%s/standingL.png' % self.name),
                    'jump': PhotoImage(file='images/jump.png')} #add
        self.walkAnimation=[PhotoImage(file='images/cave1.png'), PhotoImage(file='images/cave2.png'),
                            PhotoImage(file='images/cave3.png'), PhotoImage(file='images/cave4.png')]
        self.walk=0
        self.dY=-30
        self.caveHeight=data.height-190
        self.jump, self.jumpMax=False, self.caveHeight-150 #up is subtracting
        if data.mode == 'cave':
            self.x, self.y=300, data.height-190
        else:
            self.x=data.width//2
            self.y=data.height-120
        self.inventory={'Water Bottle (% full)': 80, 'Berries': 0, 'Grass': 0, 'Rope': 0, 
            'Traps': 0, 'Prey Caught': 0, 'Wood':0, 'Torch': 0, 'Fish': 0}
        self.willCollide=False
    
    def __repr__(self):
        return self.name
    
    def draw(self, canvas, data):
        canvas.create_image(data.width/2, data.height/5, image=self.images['standingR'])
    
    def redrawAll(self, canvas, data):
        if data.deltaX >= 0 and data.mode == 'game':
            canvas.create_image(self.x, self.y, image=self.images['standingR'])
        elif data.deltaX < 0 and data.mode == 'game':
            canvas.create_image(self.x, self.y, image=self.images['standingL'])
        elif data.mode == 'cave' and self.jump == True:
            canvas.create_image(self.x, self.y, image=self.images['jump'])
        elif data.mode == 'cave' and data.locations.body[0] > 700:
            canvas.create_image(self.x, self.y, image=self.walkAnimation[self.walk])
        elif data.mode == 'cave' and data.locations.body[0] <= 700 and data.isMoving == False:
            canvas.create_image(self.x, self.y, image=self.images['jump'])
        else:
            canvas.create_image(self.x, self.y, image=self.walkAnimation[self.walk])
    
    def drink(self):
        waterLeft=self.inventory['Water Bottle (% full)']
        currentThirst=100-self.thirst
        quenchableThirst=waterLeft//2
        #more water left than needed
        if quenchableThirst > currentThirst:
            self.thirst=100
            self.inventory['Water Bottle (% full)'] -= currentThirst*2
        #just enough water left to reach 100
        elif quenchableThirst == currentThirst:
            self.thirst=100
            self.inventory['Water Bottle (% full)']=0
        #less water than needed to reach full thirst
        else:
            self.thirst+=quenchableThirst
            self.inventory['Water Bottle (% full)']=0
        #drinking also increases health by a little 
        if self.health <= 98:
            self.health += 2
        else:
            self.health=100
    
    def eatBerry(self):
        berriesLeft=self.inventory['Berries']
        currentHunger=100-self.hunger
        satiableHunger=berriesLeft*5
        #there's more than enough berries to be full
        if satiableHunger > currentHunger:
            self.hunger=100
            self.inventory['Berries'] -= (currentHunger//5+1)
        #just enough berries to be full
        elif satiableHunger == currentHunger:
            self.hunger=100
            self.inventory['Berries']=0
        #there's not enough berries to be full 
        else:
            self.hunger += satiableHunger
            self.inventory['Berries']=0
        #eating also improves health
        if self.health <= 97:
            self.health += 3
        else:
            self.health=100
    
    def consumePrey(self):
        if self.hunger <= 80:
            self.inventory['Prey Caught'] -= 1
            self.hunger += 20
        else:
            self.hunger=100
            self.inventory['Prey Caught'] -= 1
        if self.health <= 95:
            self.health+=5
        else:
            self.health=100
    
    def eatFish(self):
        if self.hunger <= 80:
            self.inventory['Fish'] -= 1
            self.hunger += 15
        else:
            self.hunger=100
            self.inventory['Fish'] -= 1
        if self.health <= 93:
            self.health+=7
        else:
            self.health=100
    
    def build(self, item):
        for material in Character.buildRecipe[item]:
            self.inventory[material] -= Character.buildRecipe[item][material]
        self.inventory[item] += 1
        self.hunger -= 5
    
    def collect(self, item):
        if item == 'water':
            self.inventory['Water Bottle (% full)']=100
            self.hunger -= 1
        elif item == 'wood':
            self.inventory['Wood'] += 1
            self.hunger -= 3
            self.thirst -= 5
        #add all the other stuff as well
    
    def reorient(self, x, y):
        self.x=x
        self.y=y
    
    def timerFired(self):
        self.walk=(self.walk+1)%4
        if self.jump == True:
            self.caveJump()
    
    def caveJump(self):
        self.y += self.dY
        if self.dY < 0: self.dY += 3
        else: self.dY -= 3
        if self.y <= self.jumpMax:
            self.dY = 30
        if self.y >= self.caveHeight:
            self.jump=False
            self.dY=-30
    