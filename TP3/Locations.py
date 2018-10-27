### Class for Locations of Interactive Objects

class Locations(object):
    def __init__(self):
        #all icons are 100 across and 40 down 
        self.inventoryIcons={} #just y value of button
        self.gameIcons={} #x and y value of button
        self.buildIcons={} #just y value of button
        self.woodMargins=[[580, 50, 630, 300], [1650, 80, 1700, 430],
                            [2480, 50, 2550, 350], [3300, 150, 3400, 450],
                            [4850, 0, 5150, 450], [5300, 250, 5350, 450]] #[x0, y0, x1, y1]
        self.wood=[[580, 50, 630, 300], [1650, 80, 1700, 430],
                            [2480, 50, 2550, 350], [3300, 150, 3400, 450],
                            [4850, 0, 5150, 450], [5300, 250, 5350, 450]]
        self.body=[9000, 370] #9000 is good
        self.map=[540, 410, 570, 430]
        self.compass=[350, 270, 410, 360]
        
    def water(self, data):
        waterX=data.forest1X+100
        waterY=470
        return waterX, waterY
    
    def cave(self, data):
        caveX=data.forest1X+5750
        caveY=300
        caveWidth=200
        caveHeight=175
        return caveX, caveY, caveWidth, caveHeight
    
    def timerFired(self, data):
        if 'berries' in self.gameIcons:
            self.gameIcons['berries'][0]=data.forest1X+data.berryBushes[data.numBush].margin-50
        for i in range(len(self.wood)):
            for j in range(0, 4, 2):
                self.wood[i][j]=data.forest1X+self.woodMargins[i][j]
                