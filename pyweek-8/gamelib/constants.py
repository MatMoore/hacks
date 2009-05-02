SCREENSIZE = 800,600
FILLCOLOR = 0,0,0   
BACKGROUNDIMAGE = "background.jpg"

GAMESTATE_TITLE = 0
GAMESTATE_RUN = 1
GAMESTATE_QUIT = 2
GAMESTATE_PAUSE = 3
GAMESTATE_WIN = 4
GAMESTATE_LOSE = 5

SCROLLSPEED = 200 #100 pixels per second
SCROLLWIDTH = 30 #width of border that makes it scroll
FRAMERATE = 10  #frame rate of all animations
DRAGDISTANCE = 4 #distance required to move mouse before it becomes a drag instead of a click
DRAGRECTCOLOR = 0,0,255
TURNSPEED = 90 #degrees per second
MOVESPEED = 50 #pixels per second basic move speed
HEALTHBARGAP = 15 #vertical position of health bar relative to the units rect
HEALTHBARSIZE = (60,5)
GRIDSIZE = 200  #size of a grid... this should never be below the sight distance, because a unit gets passed all units in the grid locations around itself but nothing further
BUTTONSPACING = 5 #space between GUI buttons
AVOIDDISTANCE = 50 # distance to begin avoid move at(in addition to the radiuses of each unit)
MINIMAPWIDTH = 200
MINIMAPHEIGHT = 200
MINIMAPSCALEX = 5
MINIMAPSCALEY = 5
MINIMAPDOTSIZE = 0

RANDOMTARGETMAXANGLE = 45
RANDOMTARGETMAX = 50
RANDOMTARGETMIN = 10

LASERCOLOR = 255,0,0

MAXAIDISTANCE = 6000
MINAIDISTANCE = 5000
SEPERATION = 300    #distance leaves must be from any other leaves
NUMBEROFLEAVES = 100

FRIENDLYCOLOR = (0,0,255)
ENEMYCOLOR = (255,0,0)
