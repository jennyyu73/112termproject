########## Term Project Main File ############
## Jifeng (Jenny) Yu
## AndrewID: jifengy
## section G
#####################

from tkinter import *
from random import *
from Character import *
import Locations
from Bush import *
from Grass import *
from Trap import *
from gameHelper import *


########## Citations
# run, writeFile, and readFile functions are all taken from the 15-112 course website
# MVP model is based off of the 15-112 course materials
# all art done by myself on Paint Tool SAI program

#### To Do List

# make video!!

###### Overall MVP

def init(data):
    data.mode='start'
    data.forest1X, data.forest2X=-data.width, data.width*2
    data.timerCounter, data.isMoving, data.deltaX= 0, False, 0
    data.quote=chooseQuote()
    data.hair, data.gender, data.name='brown', 'female', 'Madeline'
    data.names={'female':{'brown': 'Madeline', 'black': 'Jenny', 'blonde':'Julie'}, 
        'male':{'brown': 'Willis', 'black': 'Jason', 'blonde': 'Leo'}}
    #everything dealing with interactable objects is below 
    data.isInWater=data.isInBerries=data.isInGrass=data.isInTrap=data.isInWood=data.isInCave=False  
    data.consummables=['Water Bottle (% full)', 'Berries', 'Prey Caught', 'Fish']
    data.locations=Locations.Locations()
    data.canConsume, data.cannotConsume, data.consumedItem=False, False, ''
    data.drankWater=data.ateBerries=data.consumedPrey=data.placedTrap=data.ateFish=False
    data.cannotDrinkWater=data.cannotEatBerries=data.cannotConsumePrey=data.cannotPlaceTrap=data.cannotEatFish=False
    data.canBuild=data.cannotBuild=data.menu=False
    data.collectPopUp=data.cannotCollectPopUp=data.caughtPreyPopUp=data.didNotCatchPreyPopUp=data.enterCavePopUp=False
    data.collectedItem, data.noTorch='', False
    initializeBerriesGrass(data)
    initializeBerriesGrass(data)
    data.numBush, data.numTrap, data.numGrass, data.placedTraps, data.numTree, data.numStalagmite=0, 0, 0, [], 0, 0
    initializeImages(data)
    data.stalagmites, data.stalactites, data.fishes=[], [], []
    data.hookX, data.hookY, data.hookDY, data.hookMoving, data.caughtFish=740, 40, -15, False, False
    data.isInBody=data.isInMap=data.isInCompass=data.compassPopUp=data.mapPopUp=data.nothingFound=False
    loadSavedGameState(data)

def loadSavedGameState(data):
    savedText=readFile('save.txt')
    if savedText == '0':
        pass
    else:
        data.mode='game'
        for line in savedText.splitlines():
            words=line.split()
            if words[0] == 'name':
                data.player=Character(words[1], data)
            elif words[0] == 'x': data.player.x=int(words[1])
            elif words[0] == 'y': data.player.y=int(words[1])
            elif words[0] == 'health': data.player.health=int(words[1])
            elif words[0] == 'hunger': data.player.hunger=int(words[1])
            elif words[0] == 'thirst': data.player.thirst=int(words[1])
            elif words[0] == 'water': data.player.inventory['Water Bottle (% full)']=int(words[1])
            elif words[0] == 'berry': data.player.inventory['Berries']=int(words[1])
            elif words[0] == 'grass': data.player.inventory['Grass']=int(words[1])
            elif words[0] == 'rope': data.player.inventory['Rope']=int(words[1])
            elif words[0] == 'trap': data.player.inventory['Traps']=int(words[1])
            elif words[0] == 'prey': data.player.inventory['Prey Caught']=int(words[1])
            elif words[0] == 'wood': data.player.inventory['Wood']=int(words[1])
            elif words[0] == 'torch': data.player.inventory['Torch']=int(words[1])
            elif words[0] == 'fish': data.player.inventory['Fish']=int(words[1])
            elif words[0] == 'forest1': data.forest1X=int(words[1])
            elif words[0] == 'forest2': data.forest2X=int(words[1])

def saveGame(data):
    content="""\
name %s
x %d
y %d
health %d
hunger %d
thirst %d
water %d
berry %d
grass %d
rope %d
trap %d
prey %d
wood %d
torch %d
fish %d
forest1 %d
forest2 %d""" %(data.name, data.player.x, data.player.y, data.player.health, data.player.hunger,
            data.player.thirst, data.player.inventory['Water Bottle (% full)'], data.player.inventory['Berries'],
            data.player.inventory['Grass'], data.player.inventory['Rope'], data.player.inventory['Traps'],
            data.player.inventory['Prey Caught'], data.player.inventory['Wood'], data.player.inventory['Torch'],
            data.player.inventory['Fish'], data.forest1X, data.forest2X)
    writeFile('save.txt', content)

def initializeBerriesGrass(data):
    #this eliminates any repeat bushes (bushes that are on top of each other)
    data.berryBushes, data.grasses= [], []
    for i in range(5):
        newGrass=Grass(data)
        newBush=Bush(data)
        if newBush not in data.berryBushes:
            data.berryBushes.append(newBush)
        if newGrass not in data.grasses:
            data.grasses.append(newGrass)

def initializeImages(data):
    data.forest1=PhotoImage(file='images/forest1.png')
    data.forest2=PhotoImage(file='images/forest2.png')
    data.statusImages=[PhotoImage(file='images/health.png'), PhotoImage(file='images/hunger.png'),
        PhotoImage(file='images/thirst.png')]
    data.inventoryImage, data.buildImage=PhotoImage(file='images/inventory.png'), PhotoImage(file='images/build.png')
    data.caveBackground=PhotoImage(file='images/caveBG.png')
    data.stalagmiteImages=[PhotoImage(file='images/stalagmite1.png'), PhotoImage(file='images/stalagmite2.png'),
        PhotoImage(file='images/stalagmite3.png')]
    data.stalactiteImages=[PhotoImage(file='images/stalactite1.png'), PhotoImage(file='images/stalactite2.png'),
        PhotoImage(file='images/stalactite3.png')]
    data.riverBackground=PhotoImage(file='images/riverBG.png')
    data.hook=PhotoImage(file='images/hook.png')
    data.fishImages={'right': PhotoImage(file='images/fishRight.png'), 'left': PhotoImage(file='images/fishLeft.png')}
    data.bodyImage=PhotoImage(file='images/body.png')
    data.scavengeBackground={'both': PhotoImage(file='images/scavengeBG0.png'), 
        'no compass': PhotoImage(file='images/scavengeBG1.png'),
        'no map': PhotoImage(file='images/scavengeBG2.png')}

def keyPressed(event, data):
    if data.mode == 'start': startKeyPressed(event, data)
    elif data.mode == 'instructions': instructionsKeyPressed(event, data)
    elif data.mode == 'game': gameKeyPressed(event, data)
    elif data.mode == 'cave': caveKeyPressed(event, data)
    elif data.mode == 'caveInstructions': caveInstructionsKeyPressed(event, data)
    elif data.mode == 'lose': loseKeyPressed(event, data)
    elif data.mode == 'win': winKeyPressed(event, data)

def mousePressed(event, data):
    if data.mode == 'game': gameMousePressed(event, data)
    elif data.mode == 'character': characterMousePressed(event, data)
    elif data.mode == 'fish': fishMousePressed(event, data)
    elif data.mode == 'build': buildMousePressed(event, data)
    elif data.mode == 'inventory': inventoryMousePressed(event, data)
    elif data.mode == 'cave': caveMousePressed(event, data)
    elif data.mode == 'scavenge': scavengeMousePressed(event, data)

def timerFired(data):
    if data.mode == 'game': gameTimerFired(data)
    elif data.mode == 'cave': caveTimerFired(data)
    elif data.mode == 'caveInstructions': caveInstructionsTimerFired(data)
    elif data.mode == 'fish': fishTimerFired(data)

def redrawAll(canvas, data):
    if data.mode == 'start': startRedrawAll(canvas, data)
    elif data.mode == 'instructions': instructionsRedrawAll(canvas, data)
    elif data.mode == 'character': characterRedrawAll(canvas, data)
    elif data.mode == 'game': gameRedrawAll(canvas, data)
    elif data.mode == 'fish': fishRedrawAll(canvas, data)
    elif data.mode == 'build': buildRedrawAll(canvas, data)
    elif data.mode == 'inventory': inventoryRedrawAll(canvas, data)
    elif data.mode == 'cave': caveRedrawAll(canvas, data)
    elif data.mode == 'caveInstructions': caveInstructionsRedrawAll(canvas, data)
    elif data.mode == 'lose': loseRedrawAll(canvas, data)
    elif data.mode == 'win': winRedrawAll(canvas, data, data.quote)
    elif data.mode == 'scavenge': scavengeRedrawAll(canvas, data)

#### Start Mode

def startKeyPressed(event, data):
    if event.keysym == 'c':
        data.mode='instructions'

def startRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill='#2d6e84')
    canvas.create_text(data.width/2, data.height/2-20, text='Survive the Wild', 
        font='System 50', fill='white')
    canvas.create_text(data.width/2, data.height/2+30, text="Press \"c\" to continue...", 
        font='System 25', fill='white')
    canvas.create_image(data.width/2, data.height/5, image=data.fishImages['right'])

##### Instructions Mode

def instructionsKeyPressed(event, data):
    if event.keysym == 'p':
        data.mode='character'

def instructionsRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill='#2d6e84')
    canvas.create_text(data.width/2-20, data.height/2, text="""\
        Instructions: Use your mouse to move the character around. 
        Pay attention to your health, hunger ,and thirst status. 
        Collect resources and food to survive for longer!
        Hopefully you can find the way to escape the wild. 
        Most importantly, have fun!
        Press 'p' to play...""", fill='white', font='System 20')

###### Character Customization Mode

def characterMousePressed(event, data):
    mouseX=event.x
    mouseY=event.y
    isInPlayButton(mouseX, mouseY, data)
    isInGenders(mouseX, mouseY, data)
    isInHairColors(mouseX, mouseY, data)

def characterRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill='#2d6e84')
    canvas.create_text(data.width/2, 50, text='Character Customization', fill='white',
        font='System 35')
    canvas.create_text(data.width/2, 90, text='Use your mouse to select.', fill='white',
        font='System 15')
    canvas.create_rectangle(data.width-110, data.height-50, data.width-10, data.height-10,
        width=3, fill=None, outline='white')
    canvas.create_text(data.width-60, data.height-30, text='play!', fill='white',
        font='System 20')
    drawGenders(canvas, data)
    drawHairColors(canvas, data)

#### Character Customization Helper Functions

def drawGenders(canvas, data):
    genders=['female', 'male']
    width=data.width/3
    height=data.height/2-50
    canvas.create_text(10, height, anchor=W, text='Gender:', fill='white',
        font='System 25')
    for i in range(len(genders)):
        if genders[i] == data.gender: color='black'
        else: color='white'
        canvas.create_rectangle((i+1)*width-50, height-20, (i+1)*width+50,
            height+20, fill=None, outline=color, width=3)
        canvas.create_text((i+1)*width, height, text=genders[i], font='System 20',
            fill=color)

def drawHairColors(canvas, data):
    hairColors=['brown', 'black', 'blonde']
    width=data.width/4
    height=data.height/2+50
    canvas.create_text(10, height, anchor=W, text='Hair color:', fill='white',
        font='System 25')
    for i in range(len(hairColors)):
        if data.hair == hairColors[i]: color='black'
        else: color='white'
        canvas.create_rectangle((i+1)*width-50, height-20, (i+1)*width+50,
            height+20, fill=None, outline=color, width=3)
        canvas.create_text((i+1)*width, height, text=hairColors[i], font='System 20',
            fill=color)

def isInGenders(mouseX, mouseY, data):
    genders=['female', 'male']
    width=data.width/3
    height=data.height/2-50
    for i in range(len(genders)):
        if mouseX > (i+1)*width-50 and mouseX < (i+1)*width+50 and mouseY > height-20\
        and mouseY < height+20:
            data.gender=genders[i]
            break

def isInHairColors(mouseX, mouseY, data):
    hairColors=['brown', 'black', 'blonde']
    width=data.width/4
    height=data.height/2+50
    for i in range(len(hairColors)):
        if mouseX > (i+1)*width-50 and mouseX < (i+1)*width+50 and mouseY > height-20\
        and mouseY < height+20:
            data.hair=hairColors[i]
            break
    
def isInPlayButton(mouseX, mouseY, data):
    if mouseX > data.width-110 and mouseX < data.width-10 and mouseY > data.height-50\
    and mouseY < data.height-10:
        data.name=data.names[data.gender][data.hair]
        data.player=Character(data.name, data)
        data.mode='game'

####### Game Mode 

def gameTimerFired(data):
    data.timerCounter += 1
    adjustMovement(data)
    isGameOver(data)
    changeBodyStatus(data) #changes health, thirst, etc
    for bush in data.berryBushes:
        bush.timerFired(data)
    data.locations.timerFired(data)
    for trap in data.placedTraps:
        trap.timerFired(data)
    for grass in data.grasses:
        grass.timerFired(data)

def gameMousePressed(event, data):
    mouseX=event.x
    mouseY=event.y
    isInMenu(mouseX, mouseY, data)
    isInMenuButton(mouseX, mouseY, data)
    if mouseX > 950 and mouseY < 50: data.mode='inventory'
    elif mouseX > 950 and mouseY < 100 and mouseY > 50: data.mode='build'
    isInObject(mouseX, mouseY, data)
    if data.isInBerries == False and data.isInGrass == False and data.isInTrap == False\
    and data.isInWood == False and data.isInCave == False: 
    #for the water, you don't need to adjust movement x because it's on the border of the page
        data.deltaX=(mouseX-data.player.x)
        if mouseX > data.player.x+50 or mouseX < data.player.x-50: data.isMoving = True
    else:
        if mouseX-data.player.x < 0: data.deltaX=(mouseX-data.player.x+85)
        else: data.deltaX=(mouseX-data.player.x-85)
        if mouseX > data.player.x+50 or mouseX < data.player.x-50: data.isMoving = True
    if data.menu == True: data.isMoving=False
    isInCollectIcon(mouseX, mouseY, data)
    isInCheckTrapIcon(mouseX, mouseY, data)
    isInEnterCaveIcon(mouseX, mouseY, data)
    closeCollectPopUp(mouseX, mouseY, data)
    deleteIcons(data)

def gameKeyPressed(event, data):
    if event.keysym == "t":
        data.player.inventory["Torch"] += 1
    elif event.keysym == 'h':
        data.player.hunger = 100
    elif event.keysym == "d":
        data.player.thirst = 100
    elif event.keysym == "b":
        data.player.inventory["Berries"] += 100

def gameRedrawAll(canvas, data):
    canvas.create_image(data.forest1X, 0, anchor=NW, image=data.forest1)
    canvas.create_image(data.forest2X, 0, anchor=NW, image=data.forest2)
    for bush in data.berryBushes:
        bush.draw(canvas, data)
    for grass in data.grasses:
        grass.draw(canvas)
    drawCollectButtons(canvas, data)
    data.player.redrawAll(canvas, data)
    for trap in data.placedTraps:
        trap.draw(canvas)
    if data.isInTrap == True: drawCheckTrap(canvas, data)
    drawPopUps(canvas, data)
    drawStatusBars(canvas, data)
    drawInventoryIcon(canvas, data)
    drawBuildIcon(canvas, data)
    drawMenuButton(canvas, data)

def drawCollectButtons(canvas, data):
    if data.isInWater == True: drawCollectWater(canvas, data)
    if data.isInBerries == True: drawCollectBerries(canvas, data)
    if data.isInGrass == True: drawCollectGrass(canvas, data)
    if data.isInWood == True: drawCollectWood(canvas, data)
    if data.isInCave == True: drawEnterCave(canvas, data)

def drawPopUps(canvas, data):
    if data.collectPopUp == True: drawCollectPopUp(canvas, data)
    elif data.cannotCollectPopUp == True: drawCannotCollectPopUp(canvas, data)
    if data.caughtPreyPopUp == True: drawCaughtPreyPopUp(canvas, data)
    elif data.didNotCatchPreyPopUp == True: drawDidNotCatchPreyPopUp(canvas, data)
    if data.enterCavePopUp == True: drawEnterCavePopUp(canvas, data)
    if data.menu == True: drawMenuPopUp(canvas, data)

def isInMenuButton(mouseX, mouseY, data):
    if data.menu == True:
        if mouseX > data.width/2-50 and mouseX < data.width/2+50:
            if mouseY > data.height/2-70 and mouseY < data.height/2-30:
                writeFile('save.txt', '0')
                init(data)
            elif mouseY > data.height/2-20 and mouseY < data.height/2+20:
                quit()
            elif mouseY > data.height/2+30 and mouseY < data.height/2+70:
                saveGame(data)

###### Fishing Mode

def fishMousePressed(event, data):
    if data.caughtFish == False:
        if event.x > 10 and event.x < 110 and event.y > data.height-50 and event.y < data.height-10:
            del data.fishes[:]
            data.timerCounter=0
            data.hookDY=-15
            data.mode='game'
        if data.hookMoving == False:
            data.hookMoving=True
            if data.hookY < 50: data.hookY += 15
            else: data.hookY -= 15
        data.hookDY=-data.hookDY
    else:
        #closes the fish popup
        if event.x > data.width/2-50 and event.x < data.width/2+50 and event.y > data.height/2+110\
        and event.y < data.height/2+150:
            del data.fishes[:]
            data.caughtFish=False
            data.mode='game'
            data.hookDY=-15

def fishTimerFired(data):
    data.timerCounter += 1
    if data.hookY < 50 or data.hookY > data.height-50:
        data.hookMoving=False
    if data.hookMoving == True and data.hookY >= 50 and data.hookDY > 0:
        data.hookY += data.hookDY
    elif data.hookMoving == True and data.hookY <= data.height-50 and data.hookDY < 0:
        data.hookY += data.hookDY
    addFish(data)
    moveFish(data)
    fishingBodyStatus(data)
    if data.caughtFish == False:
        checkCaughtFish(data)

def fishRedrawAll(canvas, data):
    #have a pop up show up if you caught a fish, exit the minigame if that's the case
    canvas.create_image(0, 0, anchor=NW, image=data.riverBackground)
    canvas.create_line(data.hookX, 24, data.hookX, data.hookY, width=2)
    canvas.create_image(data.hookX, data.hookY, anchor=N, image=data.hook)
    canvas.create_rectangle(10, data.height-50, 110, data.height-10, fill=None,
        width=3, outline='white')
    canvas.create_text(60, data.height-30, text='quit', font='System 20', fill='white')
    drawFishes(canvas, data)
    if data.caughtFish == True and data.timerCounter >= 10:
        drawCaughtFishPopUp(canvas, data)

##### Fishing Mode Helper Functions

def fishingBodyStatus(data):
    if data.timerCounter%50 == 0:
        data.player.thirst -= 2
    if data.timerCounter%100 == 0:
        data.player.hunger -= 2
    if (data.player.thirst < 50 or data.player.hunger < 50) and data.timerCounter % 50 == 0:
        data.player.health -= 1

def addFish(data):
    if data.timerCounter%10 == 0 and random() < 0.5:
        #fish images anchored E
        #[direction of fish, x, y, speed]
        newFish=['right', 0, randint(100, 500), randint(5, 40)]
        data.fishes.append(newFish)

def moveFish(data):
    #changes x coordinates of fishes
    for i in range(len(data.fishes)):
        data.fishes[i][1] += data.fishes[i][3]
    #delete fishes that are offscreen
    for i in range(len(data.fishes)):
        if data.fishes[i][1] < 0 or data.fishes[i][1] > data.width+100:
            data.fishes.pop(i)
            break
    #randomly change direction of fish from right to left only, not left to right
    if len(data.fishes) > 2:
        randomIndex=randint(0, len(data.fishes)-1)
        if random() < 0.05 and data.fishes[randomIndex][0] == 'right' and data.fishes[randomIndex][1] < data.hookX-50:
            data.fishes[randomIndex][0]='left'
            data.fishes[randomIndex][3]=-data.fishes[randomIndex][3]

def checkCaughtFish(data):
    #if you have caught a fish, the speed of that fish goes to 0 for a few seconds, then a pop up shows up saying you caught a fish
    for fish in data.fishes:
        #30 by 30 pixel region to catch a fish
        if data.hookX > fish[1]-20 and data.hookX < fish[1]+10 \
        and data.hookY > fish[2]-15 and data.hookY < fish[2]+15:
            fish[3]=0
            data.timerCounter=0
            data.caughtFish=True
            data.hookDY=0
            data.player.inventory['Fish'] += 1

def drawFishes(canvas, data):
    for fish in data.fishes:
        canvas.create_image(fish[1], fish[2], anchor=E, image=data.fishImages[fish[0]])

def drawCaughtFishPopUp(canvas, data):
    canvas.create_rectangle(200, 100, data.width-200, data.height-100, fill='#DCF4F6', 
        outline='#2d6e84', width=3) 
    canvas.create_text(data.width/2, data.height/2-20, 
        text='You caught a fish!\nIt has been added to your inventory.', font='System 25', 
        fill='#2d6e84') 
    canvas.create_rectangle(data.width/2-50, data.height/2+110, data.width/2+50, 
        data.height/2+150, fill=None, outline='#2d6e84', width=3)
    canvas.create_text(data.width/2, data.height/2+130, text='exit', font='System 20', 
        fill='#2d6e84')

##### Inventory Mode

def inventoryMousePressed(event, data):
    mouseX, mouseY = event.x, event.y
    if mouseX < 110 and mouseX > 10 and mouseY < data.height-10 and mouseY > data.height-50:
        data.isMoving=False
        data.drankWater=data.ateBerries=data.consumedPrey=False
        data.cannotDrinkWater=data.cannotEatBerries=data.cannotConsumePrey=False
        data.mode='game'
    evaluateConsumption(mouseX, mouseY, data)
    closeInventoryPopUp(mouseX, mouseY, data)
    
def inventoryRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill='black')
    canvas.create_rectangle(10, data.height-50, 110, data.height-10, fill=None, outline='white', width=3)
    canvas.create_text(60, data.height-30, text='close', fill='white', font='System 20')
    canvas.create_text(data.width/2, 50, text='Inventory', fill='white', font='System 40')
    drawInventory(canvas, data)
    if data.drankWater == True: drawDrankWater(canvas, data)
    elif data.ateBerries == True: drawAteBerries(canvas, data)
    elif data.ateFish == True: drawAteFish(canvas, data)
    elif data.consumedPrey == True: drawConsumedPrey(canvas, data)
    elif data.cannotDrinkWater == True: drawCannotDrinkWater(canvas, data)
    elif data.cannotEatBerries == True: drawCannotEatBerries(canvas, data)
    elif data.cannotEatFish == True: drawCannotEatFish(canvas, data)
    elif data.cannotConsumePrey == True: drawCannotConsumePrey(canvas, data)
    elif data.placedTrap == True: drawPlacedTrap(canvas, data)
    elif data.cannotPlaceTrap == True: drawCannotPlaceTrap(canvas, data)

##### Inventory Mode Helper functions

def evaluateConsumption(mouseX, mouseY, data):
    for icon in data.locations.inventoryIcons:
        if mouseX > data.width-160 and mouseX < data.width-10 and mouseY > data.locations.inventoryIcons[icon]\
            and mouseY < data.locations.inventoryIcons[icon]+40:
            if waterConsumption(data, icon): break
            if berryConsumption(data, icon): break
            if preyConsumption(data, icon): break
            if trapPlaced(data, icon): break
            if fishConsumption(data, icon): break

def fishConsumption(data, icon):
    if 'Fish' in icon and data.player.inventory['Fish'] > 0 and data.player.hunger < 100:
        data.player.eatFish()
        data.ateFish=True
    elif 'Fish' in icon and (data.player.inventory['Fish'] == 0 or data.player.hunger == 100):
        data.cannotEatFish=True
    return False 

def trapPlaced(data, icon):
    if 'Trap' in icon and data.player.inventory['Traps'] > 0:
        newTrap=Trap(data.player.x-50, data)
        data.placedTraps.append(newTrap)
        data.player.inventory['Traps'] -= 1
        data.placedTrap=True
        return True
    elif 'Trap' in icon and data.player.inventory['Traps'] == 0:
        data.cannotPlaceTrap=True
        return True
    return False 

def waterConsumption(data, icon):
    if 'Water' in icon and data.player.inventory['Water Bottle (% full)'] > 0 and data.player.thirst < 100:
        data.player.drink()
        data.drankWater=True
        return True
    #cannot drink water
    elif 'Water' in icon and (data.player.inventory['Water Bottle (% full)'] == 0 or data.player.thirst == 100):
        data.cannotDrinkWater=True
        return Truer
    return False

def berryConsumption(data, icon):
    if 'Berries' in icon and data.player.inventory['Berries'] > 0 and data.player.hunger < 100:
        data.player.eatBerry()
        data.ateBerries=True
    elif 'Berries' in icon and (data.player.inventory['Berries'] == 0 or data.player.hunger == 100):
        data.cannotEatBerries=True
    return False

def preyConsumption(data, icon):
    if 'Prey' in icon and (data.player.inventory['Prey Caught'] == 0 or data.player.hunger == 100):
        data.cannotConsumePrey=True
        return True
    elif 'Prey' in icon and data.player.inventory['Prey Caught'] > 0 and data.player.hunger < 100:
        data.player.consumePrey()
        data.consumedPrey=True
        return True
    return False

def closeInventoryPopUp(mouseX, mouseY, data):
    if mouseX > data.width/2-50 and mouseX < data.width/2+50 and \
            mouseY > data.height/2+110 and mouseY < data.height/2+150:
        if data.drankWater == True: data.drankWater=False
        elif data.ateBerries == True: data.ateBerries=False
        elif data.consumedPrey == True: data.consumedPrey=False
        elif data.ateFish == True: data.ateFish=False
        elif data.cannotDrinkWater == True: data.cannotDrinkWater=False
        elif data.cannotEatBerries == True: data.cannotEatBerries=False
        elif data.cannotConsumePrey == True: data.cannotConsumePrey=False
        elif data.placedTrap == True: data.placedTrap=False
        elif data.cannotPlaceTrap == True: data.cannotPlaceTrap=False
        elif data.cannotEatFish == True: data.cannotEatFish=False

########### Inventory Draw Functions

def drawInventory(canvas, data):
    i=0
    for item in data.player.inventory:
        canvas.create_text(20, i*40+100, anchor=W, text="%s: %d" % (item, data.player.inventory[item]), 
            font='System 30', fill='white')
        if item in data.consummables:
            #all the icons that are clickable are 150 pixels across and 40 pixels up and down
            canvas.create_rectangle(data.width-160, i*40+80, data.width-10, 
                i*40+120, fill=None, width=3, outline='white')
            canvas.create_text(data.width-85, i*40+100, text='consume', fill='white', 
                font='System 20')
            #x coordinates are the same, only differentiated by their y coordinates
            data.locations.inventoryIcons[item]=(i*40+80) 
        elif item == 'Traps':
            canvas.create_rectangle(data.width-160, i*40+80, data.width-10, 
                i*40+120, fill=None, width=3, outline='white')
            canvas.create_text(data.width-85, i*40+100, text='place', fill='white', 
                font='System 20')
            data.locations.inventoryIcons[item]=(i*40+80) 
        i+=1

def drawDrankWater(canvas, data):
    canvas.create_rectangle(200, 100, data.width-200, data.height-100, fill='black', outline='white', width=3) 
    canvas.create_text(data.width/2, data.height/2-20, 
        text='You have just drank some water!\nYour thirst level has improved :)',
        font='System 25', fill='white') 
    canvas.create_rectangle(data.width/2-50, data.height/2+110, data.width/2+50, 
        data.height/2+150, fill=None, outline='white', width=3)
    canvas.create_text(data.width/2, data.height/2+130, text='close', font='System 20', 
        fill='white')

def drawAteBerries(canvas, data):
    canvas.create_rectangle(200, 100, data.width-200, data.height-100, fill='black', outline='white', width=3) 
    canvas.create_text(data.width/2, data.height/2-20, 
        text='You have just eaten some berries!\nYour hunger level has improved :)',
        font='System 25', fill='white') 
    canvas.create_rectangle(data.width/2-50, data.height/2+110, data.width/2+50, 
        data.height/2+150, fill=None, outline='white', width=3)
    canvas.create_text(data.width/2, data.height/2+130, text='close', font='System 20', 
        fill='white')

def drawConsumedPrey(canvas, data):
    canvas.create_rectangle(200, 100, data.width-200, data.height-100, fill='black', outline='white', width=3) 
    canvas.create_text(data.width/2, data.height/2-20, 
        text='You have just eaten prey you caught!\nYour hunger level has improved :)',
        font='System 25', fill='white') 
    canvas.create_rectangle(data.width/2-50, data.height/2+110, data.width/2+50, 
        data.height/2+150, fill=None, outline='white', width=3)
    canvas.create_text(data.width/2, data.height/2+130, text='close', font='System 20', 
        fill='white')

def drawPlacedTrap(canvas, data):
    canvas.create_rectangle(200, 100, data.width-200, data.height-100, fill='black', outline='white', width=3) 
    canvas.create_text(data.width/2, data.height/2-20, 
        text='You have just placed a trap!\nYou can check it later to\nsee if you have caught prey.',
        font='System 25', fill='white') 
    canvas.create_rectangle(data.width/2-50, data.height/2+110, data.width/2+50, 
        data.height/2+150, fill=None, outline='white', width=3)
    canvas.create_text(data.width/2, data.height/2+130, text='close', font='System 20', 
        fill='white')

def drawAteFish(canvas, data):
    canvas.create_rectangle(200, 100, data.width-200, data.height-100, fill='black', outline='white', width=3) 
    canvas.create_text(data.width/2, data.height/2-20, 
        text='You just ate some fish\nyou caught! Your hunger\nlevel has improved :)',
        font='System 25', fill='white') 
    canvas.create_rectangle(data.width/2-50, data.height/2+110, data.width/2+50, 
        data.height/2+150, fill=None, outline='white', width=3)
    canvas.create_text(data.width/2, data.height/2+130, text='close', font='System 20', 
        fill='white')

def drawCannotEatFish(canvas, data):
    canvas.create_rectangle(200, 100, data.width-200, data.height-100, fill='black', outline='white', width=3) 
    canvas.create_text(data.width/2, data.height/2-20, 
        text='You cannot eat anymore fish!', font='System 25', fill='white') 
    canvas.create_rectangle(data.width/2-50, data.height/2+110, data.width/2+50, 
        data.height/2+150, fill=None, outline='white', width=3)
    canvas.create_text(data.width/2, data.height/2+130, text='close', font='System 20', 
        fill='white')

def drawCannotDrinkWater(canvas, data):
    canvas.create_rectangle(200, 100, data.width-200, data.height-100, fill='black', outline='white', width=3) 
    canvas.create_text(data.width/2, data.height/2-20, 
        text='You cannot drink any more water!', font='System 25', fill='white') 
    canvas.create_rectangle(data.width/2-50, data.height/2+110, data.width/2+50, 
        data.height/2+150, fill=None, outline='white', width=3)
    canvas.create_text(data.width/2, data.height/2+130, text='close', font='System 20', 
        fill='white')

def drawCannotEatBerries(canvas, data):
    canvas.create_rectangle(200, 100, data.width-200, data.height-100, fill='black', outline='white', width=3) 
    canvas.create_text(data.width/2, data.height/2-20, 
        text='You cannot eat anymore berries!',
        font='System 25', fill='white') 
    canvas.create_rectangle(data.width/2-50, data.height/2+110, data.width/2+50, 
        data.height/2+150, fill=None, outline='white', width=3)
    canvas.create_text(data.width/2, data.height/2+130, text='close', font='System 20', 
        fill='white')

def drawCannotConsumePrey(canvas, data):
    canvas.create_rectangle(200, 100, data.width-200, data.height-100, fill='black', outline='white', width=3) 
    canvas.create_text(data.width/2, data.height/2-20, 
        text='You cannot consume any more of \nyour caught prey!',
        font='System 25', fill='white') 
    canvas.create_rectangle(data.width/2-50, data.height/2+110, data.width/2+50, 
        data.height/2+150, fill=None, outline='white', width=3)
    canvas.create_text(data.width/2, data.height/2+130, text='close', font='System 20', 
        fill='white')

def drawCannotPlaceTrap(canvas, data):
    canvas.create_rectangle(200, 100, data.width-200, data.height-100, fill='black', outline='white', width=3) 
    canvas.create_text(data.width/2, data.height/2-20, 
        text='You cannot place any more traps!',
        font='System 25', fill='white') 
    canvas.create_rectangle(data.width/2-50, data.height/2+110, data.width/2+50, 
        data.height/2+150, fill=None, outline='white', width=3)
    canvas.create_text(data.width/2, data.height/2+130, text='close', font='System 20', 
        fill='white')

###### Build Mode

def buildMousePressed(event, data):
    mouseX, mouseY = event.x, event.y
    if mouseX < 110 and mouseX > 10 and mouseY < data.height-10 and mouseY > data.height-50:
        data.isMoving=False
        data.mode='game'
    evaluateBuild(mouseX, mouseY, data)
    closeBuildPopUp(mouseX, mouseY, data)

def buildRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill='#5e4639')
    canvas.create_rectangle(10, data.height-50, 110, data.height-10, fill=None, outline='white', width=3)
    canvas.create_text(60, data.height-30, text='close', fill='white', font='System 20')
    canvas.create_text(data.width/2, 50, text='Build', fill='white', font='System 40')
    drawBuild(canvas, data)
    if data.canBuild == True: drawCanBuild(canvas, data)
    elif data.cannotBuild == True: drawCannotBuild(canvas, data)
    
##### Build Mode Helper Functions

def evaluateBuild(mouseX, mouseY, data):
    for icon in data.locations.buildIcons:
        if mouseX > 10 and mouseX < 110 and mouseY > data.locations.buildIcons[icon]\
                and mouseY < data.locations.buildIcons[icon]+40:
            for material in Character.buildRecipe[icon]:
                if data.player.inventory[material] < Character.buildRecipe[icon][material]:
                    data.cannotBuild=True
                    break
                else:
                    data.player.build(icon)
                    data.canBuild=True
                    break

def drawBuild(canvas, data):
    i=0
    for item in Character.buildRecipe:
        #build button
        canvas.create_rectangle(10, i*40+80, 110, i*40+120, fill=None, width=3, 
            outline='white')
        canvas.create_text(60, i*40+100, text='build', fill='white', 
            font='System 25')
        data.locations.buildIcons[item]=(i*40+80) #y value of the button
        #item text
        canvas.create_text(150, i*40+100, anchor=W, text="%s:" % item, 
            font='System 30', fill='white')
        #recipe text
        for material in Character.buildRecipe[item]:
            canvas.create_text(400, i*40+100, anchor=W, text="%s: %d" % (material, 
                Character.buildRecipe[item][material]), font='System 30', fill='white')
            i+=1

def drawCanBuild(canvas, data):
    canvas.create_rectangle(200, 100, data.width-200, data.height-100, fill='#5e4639', outline='white', width=3) 
    canvas.create_text(data.width/2, data.height/2-20, 
        text='You have successfully\nbuilt this item! It has\nbeen added to your inventory.',
        font='System 25', fill='white') 
    canvas.create_rectangle(data.width/2-50, data.height/2+110, data.width/2+50, 
        data.height/2+150, fill=None, outline='white', width=3)
    canvas.create_text(data.width/2, data.height/2+130, text='close', font='System 20', 
        fill='white')

def drawCannotBuild(canvas, data):
    canvas.create_rectangle(200, 100, data.width-200, data.height-100, fill='#5e4639', outline='white', width=3) 
    canvas.create_text(data.width/2, data.height/2-20, 
        text='Sorry, but you cannot build\nthis item! You do not have\nenough of the needed materials.',
        font='System 25', fill='white') 
    canvas.create_rectangle(data.width/2-50, data.height/2+110, data.width/2+50, 
        data.height/2+150, fill=None, outline='white', width=3)
    canvas.create_text(data.width/2, data.height/2+130, text='close', font='System 20', 
        fill='white')

def closeBuildPopUp(mouseX, mouseY, data):
    if mouseX > data.width/2-50 and mouseX < data.width/2+50 and \
            mouseY > data.height/2+110 and mouseY < data.height/2+150:
        if data.cannotBuild == True: data.cannotBuild=False
        elif data.canBuild == True: data.canBuild=False

####### Cave Instructions Mode

def caveInstructionsKeyPressed(event, data):
    if event.keysym == 's':
        data.timerCounter=0
        data.player.reorient(300, data.height-190)
        data.mode='cave'

def caveInstructionsTimerFired(data):
    data.timerCounter += 1

def caveInstructionsRedrawAll(canvas, data):
    instructions="""\
Watch out for sharp cave stalagmites!
Press the up arrow to jump over them.

If you get hit, your health will deplete.
Press "d" to drink water and "f" to eat
food to replenish thirst, hunger, and health.

There's a treasure waiting for you at the end...
But don't die in the meanwhile..."""
    canvas.create_rectangle(0, 0, data.width, data.height, fill='black')
    canvas.create_text(data.width/2, data.height/2-20, text=instructions, font="System 25", 
        fill='white')
    if data.timerCounter%3 == 0 or (data.timerCounter+1)%3 == 0:
        canvas.create_text(data.width/2, data.height-30, text='press "s" to start', 
            font='System 15', fill='white')
    

##### Cave Mode

def caveTimerFired(data):
    if data.locations.body[0] > 700:
        data.timerCounter += 1
        data.player.timerFired()
        if data.locations.body[0] > 2000:
            addObstacles(data)
        adjustObstacles(data)
        checkCollisions(data)
        if data.player.willCollide == True: loseHealth(data)
        caveBodyStatus(data)
        caveDeath(data)
        moveBody(data)
    else:
        if data.deltaX > 0: 
            adjustCaveMovement(data)
            data.player.timerFired()

def caveKeyPressed(event, data):
    if data.locations.body[0] > 700:
        keyPressed=event.keysym
        if keyPressed == 'Up' and data.player.jump == False:
            data.player.jump=True
            data.player.hunger -= 15
        elif keyPressed == 'd':
            data.player.drink()
        elif keyPressed == 'f':
            eatFood(data)

def caveMousePressed(event, data):
    mouseX=event.x
    mouseY=event.y
    data.deltaX=mouseX-data.player.x
    if data.locations.body[0] <= 700 and data.deltaX > 0:
        data.isMoving=True
        isInScavengeIcon(mouseX, mouseY, data)
        isInBody(mouseX, mouseY, data)
        if data.isInBody == True:
            if data.deltaX < 0: data.deltaX += 50
            else: data.deltaX -= 50
    else:
        data.isMoving=False

def caveRedrawAll(canvas, data):
    canvas.create_image(0, 0, anchor=NW, image=data.caveBackground)
    drawStatusBars(canvas, data)
    drawStalactitesStalagmites(canvas, data)
    data.player.redrawAll(canvas, data)
    drawFoodWater(canvas, data)
    drawBody(canvas, data)
    if data.locations.body[0] <= 1000: drawBody(canvas, data)
    if data.isInBody == True: drawScavengeIcon(canvas, data)

##### Cave Mode Helper Functions

def isInBody(mouseX, mouseY, data):
    if mouseX > data.locations.body[0] and mouseX < data.locations.body[0]+100\
    and mouseY > data.locations.body[1] and mouseY < data.locations.body[0]+40:
        data.isInBody=True
    else:
        data.isInBody=False

def isInScavengeIcon(mouseX, mouseY, data):
    if data.isInBody == True:
        if mouseX > data.locations.body[0] and mouseX < data.locations.body[0]+100\
        and mouseY > data.locations.body[1]-40 and mouseY < data.locations.body[1]:
            data.mode='scavenge'

def moveBody(data):
    data.locations.body[0] -= 15

def adjustCaveMovement(data):
    data.isMoving=True
    if abs(data.deltaX) <= 10 or (data.player.x <=100 and data.deltaX < 0) or\
    (data.player.x >= data.width-100 and data.deltaX > 0):
        data.isMoving = False
    if data.isMoving == True:
        if data.deltaX < 0:
            data.player.x -= 10
            data.deltaX += 10
        else:
            data.player.x += 10
            data.deltaX -= 10

def drawBody(canvas, data):
    canvas.create_image(data.locations.body[0], data.locations.body[1], anchor=NW,
        image=data.bodyImage)

def drawScavengeIcon(canvas, data):
    canvas.create_rectangle(data.locations.body[0], data.locations.body[1]-40, 
        data.locations.body[0]+100, data.locations.body[1], fill=None, outline='white',
        width=3)
    canvas.create_text(data.locations.body[0]+50, data.locations.body[1]-20, text='scavenge',
        fill='white', font='System 17')

def caveDeath(data):
    if data.player.health <= 0 or data.player.thirst <= 0 or data.player.hunger <= 0:
        writeFile('save.txt', '0')
        data.mode='lose'

def checkCollisions(data):
    for i in range(len(data.stalagmites)):
        #stalagmite is anchored by NW, 50x100 or 100x100
        #player is anchored by center, 50x100
        if data.stalagmites[i][0] == 0:
            if data.player.x+25 > data.stalagmites[i][1]+5 and data.player.x-25 < data.stalagmites[i][1]+45:
                if data.player.y+50 > data.stalagmites[i][2]+10 and data.stalagmites[i][3] == False:
                    data.player.willCollide=True
                    data.numStalagmite=i
        elif data.stalagmites[i][0] == 1:
            if data.player.x+25 > data.stalagmites[i][1]+10 and data.player.x-25 < data.stalagmites[i][1]+75:
                if data.player.y+50 > data.stalagmites[i][2]+35 and data.stalagmites[i][3] == False:
                    data.player.willCollide=True
                    data.numStalagmite=i
        elif data.stalagmites[i][0] == 2:
            if data.player.x+25 > data.stalagmites[i][1]+5 and data.player.x-25 < data.stalagmites[i][1]+45:
                if data.player.y+50 > data.stalagmites[i][2]+20 and data.stalagmites[i][3] == False:
                    data.player.willCollide=True
                    data.numStalagmite=i

def loseHealth(data):
    if data.player.jump == False and data.player.willCollide == True and\
    len(data.stalagmites) > 0 and data.stalagmites[data.numStalagmite][3] == False:
        data.player.health -= 35
        data.player.willCollide=False
        data.stalagmites[data.numStalagmite][3]=True

def caveBodyStatus(data):
    if data.timerCounter%30 == 0:
        data.player.thirst -= 3
    if data.timerCounter%50 == 0:
        data.player.hunger -= 3
    if (data.player.hunger < 50 or data.player.thirst < 50) and data.timerCounter%50 == 0:
        data.player.health -= 3

def drawFoodWater(canvas, data):
    canvas.create_text(data.width-5, 5, anchor=NE, 
        text='Water: %d' %(data.player.inventory["Water Bottle (% full)"]),
        fill='white', font='System 20')
    canvas.create_text(data.width-5, 30, anchor=NE,
        text='Berries: %d' %(data.player.inventory['Berries']),
        fill='white', font='System 20')
    canvas.create_text(data.width-5, 55, anchor=NE,
        text='Fish: %d' %(data.player.inventory['Fish']),
        fill='white', font='System 20')
    canvas.create_text(data.width-5, 80, anchor=NE,
        text='Prey: %d' %(data.player.inventory['Prey Caught']),
        fill='white', font='System 20')

def eatFood(data):
    if data.player.inventory['Berries'] != 0:
        data.player.eatBerry()
    elif data.player.inventory['Fish'] != 0:
        data.player.eatFish()
    elif data.player.inventory['Prey Caught'] != 0:
        data.player.consumePrey()

def addObstacles(data):
    if random() < 0.3 and data.timerCounter%5 == 0:
        newStalactite=randint(0, 2) #chooses a random stalactite (refer to by number index)
        #[random stalactite, upper left corner x coordinate, y coordinate]
        data.stalactites.append([newStalactite,data.width, 0]) 
    if random() < 0.4 and data.timerCounter%20 == 0:
        newStalagmite=randint(0, 2)
        #added at the end is to check if health has been deducted once already or not
        data.stalagmites.append([newStalagmite, data.width, data.height-220, False])  #y coordinate here 

def adjustObstacles(data):
    #changes the x coordinates so it looks like they're moving
    for i in range(len(data.stalactites)):
        data.stalactites[i][1] -= 15
    for i in range(len(data.stalagmites)):
        data.stalagmites[i][1] -= 15
    #remove the ones that are off screen from the lists
    for i in range(len(data.stalactites)):
        if data.stalactites[i][1] < -100:
            data.stalactites.pop(i)
            break
    for i in range(len(data.stalagmites)):
        if data.stalagmites[i][1] < -100:
            data.stalagmites.pop(i)
            data.numStalagmite -= 1
            break

def drawStalactitesStalagmites(canvas, data):
    for s in data.stalactites:
        canvas.create_image(s[1], s[2], anchor=NW, image=data.stalactiteImages[s[0]])
    for s in data.stalagmites:
        canvas.create_image(s[1], s[2], anchor=NW, image=data.stalagmiteImages[s[0]])

###### Scavenge Mode

def scavengeMousePressed(event, data):
    mouseX=event.x
    mouseY=event.y
    if mouseX > data.locations.map[0] and mouseX < data.locations.map[2] and\
    mouseY > data.locations.map[1] and mouseY < data.locations.map[3] and data.isInMap == False:
        data.isInMap=True
        data.mapPopUp=True
    elif mouseX > data.locations.compass[0] and mouseX < data.locations.compass[2] and\
    mouseY > data.locations.compass[1] and mouseY < data.locations.compass[3] and data.isInCompass == False:
        data.isInCompass=True
        data.compassPopUp=True
    elif data.mapPopUp == False and data.compassPopUp == False and data.nothingFound == False:
        data.nothingFound=True
    else: closeScavengePopUps(mouseX, mouseY, data)
    if data.isInCompass == True and data.isInMap == True and data.compassPopUp == False\
    and data.mapPopUp == False and data.nothingFound == False:
        writeFile('save.txt', '0')
        data.mode='win'

def scavengeRedrawAll(canvas, data):
    if data.isInMap == False and data.isInCompass == False:
        canvas.create_image(0, 0, anchor=NW, image=data.scavengeBackground['both'])
    elif data.isInMap == True:
        canvas.create_image(0, 0, anchor=NW, image=data.scavengeBackground['no map'])
    else:
        canvas.create_image(0, 0, anchor=NW, image=data.scavengeBackground['no compass'])
    if data.compassPopUp == True: drawCompass(canvas, data)
    if data.mapPopUp == True: drawMap(canvas, data)
    if data.nothingFound == True: drawNothingFound(canvas, data)

##### Scavenge Mode helpers

def drawNothingFound(canvas, data):
    canvas.create_rectangle(200, 100, data.width-200, data.height-100, fill='black', outline='white', width=3) 
    canvas.create_text(data.width/2, data.height/2-20, 
        text='Nothing was found there.',
        font='System 25', fill='white') 
    canvas.create_rectangle(data.width/2-50, data.height/2+110, data.width/2+50, 
        data.height/2+150, fill=None, outline='white', width=3)
    canvas.create_text(data.width/2, data.height/2+130, text='close', font='System 20', 
        fill='white')

def drawCompass(canvas, data):
    canvas.create_rectangle(200, 100, data.width-200, data.height-100, fill='black', outline='white', width=3) 
    canvas.create_text(data.width/2, data.height/2-20, 
        text='You found a compass\non the dead body!',
        font='System 25', fill='white') 
    canvas.create_rectangle(data.width/2-50, data.height/2+110, data.width/2+50, 
        data.height/2+150, fill=None, outline='white', width=3)
    canvas.create_text(data.width/2, data.height/2+130, text='close', font='System 20', 
        fill='white')

def drawMap(canvas, data):
    canvas.create_rectangle(200, 100, data.width-200, data.height-100, fill='black', outline='white', width=3) 
    canvas.create_text(data.width/2, data.height/2-20, 
        text='You found a map\non the dead body!',
        font='System 25', fill='white') 
    canvas.create_rectangle(data.width/2-50, data.height/2+110, data.width/2+50, 
        data.height/2+150, fill=None, outline='white', width=3)
    canvas.create_text(data.width/2, data.height/2+130, text='close', font='System 20', 
        fill='white')

def closeScavengePopUps(mouseX, mouseY, data):
    if mouseX > data.width/2-50 and mouseX < data.width/2+50 and \
            mouseY > data.height/2+110 and mouseY < data.height/2+150:
        if data.mapPopUp == True: data.mapPopUp=False
        elif data.compassPopUp == True: data.compassPopUp=False
        elif data.nothingFound == True: data.nothingFound=False

##### Lose Mode

def loseKeyPressed(event, data):
    if event.keysym == 'p':
        writeFile('save.txt', '0')
        init(data)

def loseRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill='black')
    if data.noTorch == False:
        canvas.create_text(data.width/2, data.height/4, text="YOU DIED!", 
            font='System 40', fill='white')
        canvas.create_text(data.width/2, data.height/2, text='better luck next time :(', 
            font='System 30', fill='white')
    else:
        canvas.create_text(data.width/2, data.height/4, text="You didn't have a torch!", 
            font='System 40', fill='white')
        canvas.create_text(data.width/2, data.height/2, text='You were not able to see and\ngot attacked by cave animals!', 
            font='System 30', fill='white')
    canvas.create_text(data.width/2, data.height*3/4, text='press "p" to play again',
        font='System 20', fill='white')

#### Win Mode

def chooseQuote():
    wildernessQuotes=["""\
"Wildness is the preservation 
of the World." 
    -Henry David Thoreau""", """\
"The cave you fear to enter
holds the treasure you seek."
    -Joseph Campbell""", """\
"Are stars born in these black caves 
that house bated breaths and unspoken words?"
    -Kamand Kojouri""", """\
"The clearest way into the Universe 
is through a forest wilderness." 
    -John Muir"""]
    quote=wildernessQuotes[randint(0, len(wildernessQuotes)-1)]
    return quote

def winKeyPressed(event, data):
    if event.keysym == 'p':
        writeFile('save.txt', '0')
        init(data)

def winRedrawAll(canvas, data, quote):
    #consider scrolling text like star wars
    canvas.create_rectangle(0, 0, data.width, data.height, fill='#2d6e84')
    canvas.create_text(data.width/2, data.height/2-230, 
        text='YOU WIN!',
        font='System 45', fill='white')
    canvas.create_text(data.width/2, data.height/2-100, 
        text='You used the compass and map\nto escape the wild!',
        font='System 25', fill='white')
    canvas.create_text(data.width/2, data.height/2+50, text=quote, font='System 20', fill='white')
    canvas.create_text(data.width/2, data.height/2+200, text='press "p" to play again', 
        font='System 30', fill='white')

#####
# Run function, quit function, and file IO functions
#####

def quit():
    global root
    root.destroy()

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

root=Tk()

def run(width=1000, height=550):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 50 # milliseconds
    init(data)
    # create the root and the canvas
    #root = Toplevel()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run()