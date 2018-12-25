import math


class PathFinder:
    def __init__(self, radius):
        self.gridsize = radius
        self.map = dict()
        self.permanentMap = dict()
        
    def griddify(self, position):
        return (int(math.floor(position[0]/self.gridsize)), int(math.ceil(position[1]/self.gridsize)))


    def griddifyTL(self, position):
        return (int(math.ceil(position[0]/self.gridsize)), int(math.ceil(position[1]/self.gridsize)))

    def griddifyBR(self, position):
        return (int(math.floor(position[0]/self.gridsize)), int(math.floor(position[1]/self.gridsize)))
            
    def addObstacle(self, position, radius, permanent=False):
        topleft = self.griddifyTL((position[0]-radius, position[1]-radius))
        bottomright = self.griddifyBR((position[0]+radius, position[1]+radius))
        
        for x in range(topleft[0]-1, bottomright[0]+2):
            for y in range(topleft[1]-1, bottomright[1]+2):            
                self.map[(x,y)] = True
                if permanent:
                    self.permanentMap[(x,y)] = True

    def clearUp(self):
        self.map = self.permanentMap.copy()

    def heuristic(self, fromPos, toPos):
        return abs(toPos[0] - fromPos[0]) + abs(toPos[1] - fromPos[1])

    def calcPath(self, startPos, endPos):
        originalEnd = endPos
        originalStart = startPos
        
        openList = []
        closedList = []
        data = dict()
        startPos = self.griddify(startPos)
        endPos = self.griddify(endPos)
        
        data[startPos] = (0,self.heuristic(startPos, endPos), None)    #data is stored as [cost, fitness, parent]
        closedList.append(startPos)
        currentNode = startPos
        running = True
        while running:        
            for x in range(currentNode[0]-1, currentNode[0]+2):
                for y in range(currentNode[1]-1, currentNode[1]+2):
                    #print x, y
                    
                    if (x,y) in self.map:   #make sure we can access that grid
                        continue
                        
                    if (x,y) in closedList: #make sure it's not closed
                        continue        
                    

                    dist = self.heuristic(currentNode, (x,y))
                    
                    if dist == 0:       #make sure we're not looking at our own square
                        continue
                        
                    if  dist == 1:
                        cost = data[currentNode][0]+10  #calling it 10 to go sideways
                    else:
                        cost = data[currentNode][0]+14  #and 14 to go diagonally
                        
                    h = self.heuristic((x,y), endPos)
                    f = h + cost
                      
                    if (x,y) in data:
                        if data[(x,y)][0] > cost:
                            data[(x,y)] = (cost, f, currentNode)
                    else:
                        data[(x,y)] = (cost, f, currentNode)
                        
                    if (x,y) not in openList and (x,y) not in closedList:
                        openList.append((x,y))


            if len(openList) > 0:
                currentNode = openList[0]
                for item in openList:
                    if data[item][1] < data[currentNode][1]:
                        currentNode = item
                openList.remove(currentNode)
                closedList.append(currentNode)
                if currentNode == endPos:
                    running = False
                    route = [originalEnd]
            else:
                running = False
                route = []
        
            
        
        currentNode = data[currentNode][2]  #skip the last one (we already added it at the start, or earlier if we didn't quite make it to the end)
        if currentNode != None:             #this will be none if destination is in same grid as startpos
            while data[currentNode][2] != None:
                route.append((currentNode[0]*self.gridsize, currentNode[1]*self.gridsize))
                currentNode = data[currentNode][2]
            


#        route.append(originalStart)
        
        return route


if __name__ == '__main__':
    finder = PathFinder(20)
    finder.addObstacle((100,100),50)
    finder.calcPath((200,0),(0,200))
