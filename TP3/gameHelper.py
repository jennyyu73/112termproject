###########3
## Helper functions for Game Mode (there were too many so I put them on a separate file)
#########3

from tkinter import *
from random import *
from Character import *
import Locations
from Bush import *
from Grass import *
from Trap import *

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

def isInObject(mouseX, mouseY, data): 
    #makes sure it's not in an object that you can interact with
    isInWater(mouseX, mouseY, data)
    isInBerries(mouseX, mouseY, data)
    isInGrass(mouseX, mouseY, data)
    isInTrap(mouseX, mouseY, data)
    isInWood(mouseX, mouseY, data)
    isInCave(mouseX, mouseY, data)

def deleteIcons(data):
    #if you click outside of the object, then the icon location is deleted
    if 'berries' in data.locations.gameIcons and data.isInBerries == False:
        del data.locations.gameIcons['berries']
    if 'water' in data.locations.gameIcons:
        del data.locations.gameIcons['water']
    if 'trap' in data.locations.gameIcons:
        del data.locations.gameIcons['trap']
    if 'wood' in data.locations.gameIcons:
        del data.locations.gameIcons['wood']
    if 'grass' in data.locations.gameIcons:
        del data.locations.gameIcons['grass']
    if 'cave' in data.locations.gameIcons:
        del data.locations.gameIcons['cave']
    
def isInCollectIcon(mouseX, mouseY, data):
    #checks which collect icon it's in and performs specific collect actions
    for icon in data.locations.gameIcons:
        if mouseX > data.locations.gameIcons[icon][0] and mouseX < data.locations.gameIcons[icon][0]+100\
                and mouseY > data.locations.gameIcons[icon][1] and mouseY < data.locations.gameIcons[icon][1]+40:
            if icon == 'fish':
                data.hookMoving, data.hookY, data.hookDY=False, 40, -15
                data.timerCounter=0
                data.player.hunger -= 4
                data.player.thirst -= 5
                data.mode='fish'
            elif data.isInWater == True and data.player.inventory['Water Bottle (% full)'] != 100:
                data.player.collect('water')
                data.collectedItem='water'
                data.collectPopUp=True
            elif data.isInWater == True and data.player.inventory['Water Bottle (% full)'] == 100:
                data.cannotCollectPopUp=True
            elif data.isInBerries == True and data.berryBushes[data.numBush].berries != 0:
                data.berryBushes[data.numBush].collect(data)
                data.collectedItem='berries'
                data.collectPopUp=True
            elif data.isInBerries == True and data.berryBushes[data.numBush].berries == 0:
                data.cannotCollectPopUp=True
            elif data.isInWood == True:
                data.player.collect('wood')
                data.collectedItem='wood'
                data.collectPopUp=True
            elif icon == 'grass' and data.grasses[data.numGrass].hasGrass:
                data.grasses[data.numGrass].collect(data)
                data.collectedItem='grass'
                data.collectPopUp=True
            elif icon == 'grass' and not data.grasses[data.numGrass].hasGrass:
                data.cannotCollectPopUp=True

def isInCheckTrapIcon(mouseX, mouseY, data):
    if 'trap' in data.locations.gameIcons:
        if mouseX > data.locations.gameIcons['trap'][0] and mouseX < data.locations.gameIcons['trap'][0]+100\
                and mouseY > data.locations.gameIcons['trap'][1] and mouseY < data.locations.gameIcons['trap'][1]+40:
            if data.isInTrap == True and data.placedTraps[data.locations.gameIcons['trap'][2]].caughtPrey:
                data.placedTraps[data.locations.gameIcons['trap'][2]].collect(data)
                data.caughtPreyPopUp=True
            else:
                data.didNotCatchPreyPopUp=True

def isInEnterCaveIcon(mouseX, mouseY, data):
    if 'cave' in data.locations.gameIcons:
        if mouseX > data.locations.gameIcons['cave'][0] and mouseX < data.locations.gameIcons['cave'][0]+100\
                and mouseY > data.locations.gameIcons['cave'][1] and mouseY < data.locations.gameIcons['cave'][1]+40:
            if data.isInCave == True:
                data.enterCavePopUp=True

def closeCollectPopUp(mouseX, mouseY, data):
    if mouseX > data.width/2-50 and mouseX < data.width/2+50 and \
            mouseY > data.height/2+110 and mouseY < data.height/2+150:
        if data.collectPopUp == True: data.collectPopUp=False
        elif data.cannotCollectPopUp == True: data.cannotCollectPopUp=False
        elif data.caughtPreyPopUp == True: data.caughtPreyPopUp=False
        elif data.didNotCatchPreyPopUp == True: data.didNotCatchPreyPopUp=False
        elif data.enterCavePopUp == True: data.enterCavePopUp=False
    elif data.enterCavePopUp == True and mouseX > data.width/2-50 and mouseX < data.width/2+50 and\
    mouseY > data.height//2+60 and mouseY < data.height//2+100:
        if data.player.inventory['Torch'] == 0:
            writeFile('save.txt', '0')
            data.noTorch=True
            data.mode='lose'
        else: data.mode='caveInstructions'

def isInWater(mouseX, mouseY, data):
    waterX, waterY=data.locations.water(data)
    if mouseX < waterX and mouseY > waterY:
        data.isInWater=True
    else:
        data.isInWater=False

def isInBerries(mouseX, mouseY, data):
    for i in range(len(data.berryBushes)):
        if mouseX > data.berryBushes[i].x-75 and mouseX < data.berryBushes[i].x+75\
        and mouseY < data.berryBushes[i].y+100 and mouseY > data.berryBushes[i].y-100:
            data.isInBerries=True
            data.numBush=i
            break
        else:
            data.isInBerries=False

def isInGrass(mouseX, mouseY, data):
    for i in range(len(data.grasses)):
        if mouseX > data.grasses[i].x-25 and mouseX < data.grasses[i].x+25 and \
        mouseY > data.grasses[i].y-25 and mouseY < data.grasses[i].y+25:
            data.isInGrass=True
            data.numGrass=i
            break
        else:
            data.isInGrass=False

def isInTrap(mouseX, mouseY, data):
    for i in range(len(data.placedTraps)):
        if mouseX > data.placedTraps[i].x-25 and mouseX < data.placedTraps[i].x+25\
        and mouseY > data.placedTraps[i].y-25 and mouseY < data.placedTraps[i].y+25:
            data.isInTrap=True
            data.numTrap=i
            break
        else:
            data.isInTrap=False

def isInWood(mouseX, mouseY, data):
    for i in range(len(data.locations.wood)):
        if mouseX > data.locations.wood[i][0] and mouseX < data.locations.wood[i][2]\
        and mouseY > data.locations.wood[i][1] and mouseY < data.locations.wood[i][3]:
            data.isInWood=True
            data.numWood=i
            break
        else:
            data.isInWood=False

def isInCave(mouseX, mouseY, data):
    caveX, caveY, caveWidth, caveHeight=data.locations.cave(data)
    if mouseX > caveX and mouseX < caveX+caveWidth and mouseY > caveY and\
    mouseY < caveY+caveHeight:
        data.isInCave=True
    else:
        data.isInCave=False

def adjustMovement(data):
    if abs(data.deltaX) <= 10:
        data.isMoving = False
    #background staying still but the char moves if char is not centered
    if data.isMoving == True:
        if (data.player.x < 200 and data.deltaX < 0) or (data.player.x > 850 and data.deltaX > 0):
            data.isMoving=False
        elif data.player.x < data.width//2 and data.forest1X == 0 and data.deltaX > 0:
            data.player.x += 10
            data.deltaX -= 10
        elif data.player.x >= data.width//2 and data.forest1X == 0 and data.deltaX > 0:
            data.player.x += 10
            data.deltaX -= 10
            data.forest1X -= 10
            data.forest2X -= 10
        elif data.player.x > data.width//2 and data.forest2X == -2000 and data.deltaX < 0:
            data.player.x -= 10
            data.deltaX += 10
        elif data.player.x <= data.width//2 and data.forest2X == -2000 and data.deltaX < 0:
            data.player.x -= 10
            data.deltaX += 10
            data.forest1X += 10
            data.forest2X += 10
    #background moving to the right and left, player is centered
        elif data.forest1X != 0 and data.forest2X != -2000:
            if data.deltaX < 0:
                data.forest1X += 10
                data.forest2X += 10
                data.deltaX += 10
            else:
                data.forest1X -= 10
                data.forest2X -= 10
                data.deltaX -= 10
    #char moving right and left if at the border of the background 
        else: #elif data.forest1X == 0 or data.forest2X == -2000
            if data.deltaX < 0 and data.player.x > 50: #closest to edge of screen the char can be is 20 pixels
                data.player.x -= 10
                data.deltaX += 10
            elif data.deltaX > 0 and data.player.x < data.width-50:
                data.player.x += 10
                data.deltaX -= 10

def isGameOver(data):
    if data.player.health == 0 or data.player.thirst == 0 or data.player.hunger == 0:
        writeFile('save.txt', '0')
        data.mode='lose'

def changeBodyStatus(data): 
    if data.isMoving == True and data.timerCounter % 50 == 0:
        data.player.thirst -= 1
    elif data.timerCounter % 100 == 0: 
        data.player.thirst -= 1
    if data.isMoving == True and data.timerCounter % 200 == 0:
        data.player.hunger -= 1
    elif data.timerCounter % 300 == 0:
        data.player.hunger -= 1
    if (data.player.thirst < 50 or data.player.hunger < 50) and data.timerCounter % 50 == 0:
        data.player.health -= 1

def isInMenu(mouseX, mouseY, data):
    if mouseX > data.width-110 and mouseX < data.width-10 and mouseY > data.height-50 and\
    mouseY < data.height-10:
        data.menu=True
    elif mouseX < 300 or mouseX > data.width-300 or mouseY < 100 or mouseY > data.height-100:
        data.menu=False

###### Game Mode Draw Functions

def drawInventoryIcon(canvas, data):
    canvas.create_image(950, 10, anchor=NW, image=data.inventoryImage)

def drawBuildIcon(canvas, data):
    canvas.create_image(950, 60, anchor=NW, image=data.buildImage)

def drawStatusBars(canvas, data):
    status=[data.player.health, data.player.hunger, data.player.thirst]
    colors=['red', 'yellow', 'blue']
    for i in range(3):
        canvas.create_rectangle(50, 40*i+10, 50+status[i], 40*(i+1)-10, fill=colors[i], width=0)
    for i in range(3):
        canvas.create_rectangle(50, 40*i+10, 150, 40*(i+1)-10, fill=None)
    for i in range(len(data.statusImages)):
        canvas.create_image(0, 40*i, anchor=NW, image=data.statusImages[i])

def drawCollectWater(canvas, data):
    #fishing icon
    canvas.create_rectangle(data.forest1X+10, data.height-100, data.forest1X+110, 
        data.height-60, fill=None, outline='white', width=3)
    canvas.create_text(data.forest1X+60, data.height-80, text='fish', 
        font='System 20', fill='white')
    data.locations.gameIcons['fish']=(data.forest1X+10, data.height-100)
    #collect water icon
    canvas.create_rectangle(data.forest1X+10, data.height-50, data.forest1X+110, 
        data.height-10, fill=None, outline='white', width=3)
    canvas.create_text(data.forest1X+60, data.height-30, text='collect', 
        font='System 20', fill='white')
    data.locations.gameIcons['water']=(data.forest1X+10, data.height-50)

def drawCollectBerries(canvas, data):
    iconX=data.berryBushes[data.numBush].x-50
    iconY=data.berryBushes[data.numBush].y-20
    canvas.create_rectangle(iconX, iconY, iconX+100, iconY+40, fill=None, outline='white',
        width=3)
    canvas.create_text(iconX+50, iconY+20, text='collect', font='System 20', fill='white')
    data.locations.gameIcons['berries']=[iconX, iconY]

def drawCheckTrap(canvas, data):
    iconX=data.placedTraps[data.numTrap].x-50
    iconY=data.placedTraps[data.numTrap].y-20
    canvas.create_rectangle(iconX, iconY, iconX+100, iconY+40, fill=None, outline='white',
        width=3)
    canvas.create_text(iconX+50, iconY+20, text='check', font='System 20', fill='white')
    data.locations.gameIcons['trap']=[iconX, iconY, data.numTrap]

def drawCollectGrass(canvas, data):
    iconX=data.grasses[data.numGrass].x-50
    iconY=data.grasses[data.numGrass].y-20
    canvas.create_rectangle(iconX, iconY, iconX+100, iconY+40, fill=None, outline='white',
        width=3)
    canvas.create_text(iconX+50, iconY+20, text='collect', font='System 20', fill='white')
    data.locations.gameIcons['grass']=[iconX, iconY]

def drawEnterCave(canvas, data):
    caveX, caveY, caveWidth, caveHeight=data.locations.cave(data)
    iconX=(2*caveX+caveWidth)//2-50
    iconY=(2*caveY+caveHeight)//2-20
    canvas.create_rectangle(iconX, iconY, iconX+100, iconY+40, fill=None, outline='white',
        width=3)
    canvas.create_text(iconX+50, iconY+20, text='enter', font='System 20', fill='white')
    data.locations.gameIcons['cave']=[iconX, iconY]

def drawMenuButton(canvas, data):
    canvas.create_rectangle(data.width-110, data.height-50, data.width-10, data.height-10,
        fill=None, width=3, outline='white')
    canvas.create_text(data.width-60, data.height-30, text='menu', font='System 23',
        fill='white')

def drawCollectWood(canvas, data):
    iconX=(data.locations.wood[data.numWood][0]+data.locations.wood[data.numWood][2])//2-50
    iconY=(data.locations.wood[data.numWood][1]+data.locations.wood[data.numWood][3])//2-20
    canvas.create_rectangle(iconX, iconY, iconX+100, iconY+40, fill=None, outline='white',
        width=3)
    canvas.create_text(iconX+50, iconY+20, text='collect', font='System 20', fill='white')
    data.locations.gameIcons['wood']=[iconX, iconY, data.numWood]

def drawMenuPopUp(canvas, data):
    canvas.create_rectangle(300, 100, data.width-300, data.height-100, fill='#DCF4F6', outline='#2d6e84', width=3)
    canvas.create_text(data.width/2, data.height/2-130, text='MENU', fill="#2d6e84", font='System 35')
    canvas.create_rectangle(data.width/2-50, data.height/2-70, data.width/2+50, data.height/2-30,
        width=3, fill=None, outline='#2d6e84')
    canvas.create_text(data.width/2, data.height/2-50, text='restart', font='System 20',
        fill='#2d6e84')
    canvas.create_rectangle(data.width/2-50, data.height/2-20, data.width/2+50, data.height/2+20,
        width=3, fill=None, outline='#2d6e84')
    canvas.create_text(data.width/2, data.height/2, text='quit', font='System 20',
        fill='#2d6e84')
    canvas.create_rectangle(data.width/2-50, data.height/2+30, data.width/2+50, data.height/2+70,
        width=3, fill=None, outline='#2d6e84')
    canvas.create_text(data.width/2, data.height/2+50, text='save', font='System 20',
        fill='#2d6e84')

def drawCaughtPreyPopUp(canvas, data):
    message='You have successfully\ncaught some prey! It has\nbeen added to your inventory.'
    canvas.create_rectangle(200, 100, data.width-200, data.height-100, fill='#DCF4F6', outline='#2d6e84', width=3) 
    canvas.create_text(data.width/2, data.height/2-20, 
        text=message, font='System 25', fill='#2d6e84') 
    canvas.create_rectangle(data.width/2-50, data.height/2+110, data.width/2+50, 
        data.height/2+150, fill=None, outline='#2d6e84', width=3)
    canvas.create_text(data.width/2, data.height/2+130, text='close', font='System 20', 
        fill='#2d6e84')

def drawCollectPopUp(canvas, data):
    canvas.create_rectangle(200, 100, data.width-200, data.height-100, fill='#DCF4F6', outline='#2d6e84', width=3) 
    canvas.create_text(data.width/2, data.height/2-20, 
        text='You have successfully\ncollected some %s! It has\nbeen added to your inventory.' % data.collectedItem,
        font='System 25', fill='#2d6e84') 
    canvas.create_rectangle(data.width/2-50, data.height/2+110, data.width/2+50, 
        data.height/2+150, fill=None, outline='#2d6e84', width=3)
    canvas.create_text(data.width/2, data.height/2+130, text='close', font='System 20', 
        fill='#2d6e84')

def drawCannotCollectPopUp(canvas, data):
    canvas.create_rectangle(200, 100, data.width-200, data.height-100, fill='#DCF4F6', outline='#2d6e84', width=3) 
    canvas.create_text(data.width/2, data.height/2-20, 
        text='Sorry! You cannot collect\n any more of this resource!',
        font='System 25', fill='#2d6e84') 
    canvas.create_rectangle(data.width/2-50, data.height/2+110, data.width/2+50, 
        data.height/2+150, fill=None, outline='#2d6e84', width=3)
    canvas.create_text(data.width/2, data.height/2+130, text='close', font='System 20', 
        fill='#2d6e84')

def drawDidNotCatchPreyPopUp(canvas, data):
    message='Sorry! No prey has been\nhas been caught by this trap yet.'
    canvas.create_rectangle(200, 100, data.width-200, data.height-100, fill='#DCF4F6', outline='#2d6e84', width=3) 
    canvas.create_text(data.width/2, data.height/2-20, 
        text=message, font='System 25', fill='#2d6e84') 
    canvas.create_rectangle(data.width/2-50, data.height/2+110, data.width/2+50, 
        data.height/2+150, fill=None, outline='#2d6e84', width=3)
    canvas.create_text(data.width/2, data.height/2+130, text='close', font='System 20', 
        fill='#2d6e84')

def drawEnterCavePopUp(canvas, data):
    message='Are you sure you want to enter\nthis cave? Make sure to stock up\non supplies, because danger awaits.' 
    canvas.create_rectangle(200, 100, data.width-200, data.height-100, fill='#DCF4F6', outline='#2d6e84', width=3) 
    canvas.create_text(data.width/2, data.height/2-50, 
        text=message,font='System 25', fill='#2d6e84') 
    canvas.create_rectangle(data.width/2-50, data.height/2+110, data.width/2+50, 
        data.height/2+150, fill=None, outline='#2d6e84', width=3)
    canvas.create_rectangle(data.width/2-50, data.height/2+60, data.width/2+50,           # enter cave icon located data.width/2-50, data.height/2+60
        data.height/2+100, fill=None, outline='#2d6e84', width=3)
    canvas.create_text(data.width/2, data.height/2+80, text='enter', font='System 20',
        fill='#2d6e84')
    canvas.create_text(data.width/2, data.height/2+130, text='cancel', font='System 20', 
        fill='#2d6e84')