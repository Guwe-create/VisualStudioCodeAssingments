#The imports
import pygame
import random

#Adding in pygame
from pygame.locals import *
pygame.init()

#Adding in fonts
pygame.font.init()

#Font
font = pygame.font.SysFont('Comic Sans MS', 30)
text = font.render('Score: 0', False, (0,0,0))
score = 0

#Spawn Amount
#SpawnSpeed = font.render('Speed: 0', False, (0,0,0))

#Gamestates
GameStates = 1

#Player Health
Health = [pygame.display.set_mode((100,100)),pygame.display.set_mode((100,100)),pygame.display.set_mode((100,100))]
healthX = [200, 250, 300]
healthNumber = 3
healthImage = pygame.image.load('Crystal.png')
healthImage = pygame.transform.scale(healthImage,(100,100))

#Player information
pl = pygame.display.set_mode((100,100))
player = pygame.image.load('f1.png.png')
x = 50
y = 50
playerSpeed = .25

#Enemies
enemy = pygame.display.set_mode((50,50))
yPos = [random.randint(1,570),random.randint(1,570),random.randint(1,570),random.randint(1,570)]
enemyImage = pygame.image.load('Idle Animation.gif')
enemyImage = pygame.transform.scale(enemyImage,(50,50))
xPos = [770,770,770,770]
enemySpeed = [.2,.1,.5,.15]
enemyAmount = 4
enemySpawnSpeed = 0
spawnTime = 600

#Making the buttons
startButton = pygame.display.set_mode((300,200))
exitButton = pygame.display.set_mode((300,200))
playButton = pygame.display.set_mode((300,200))
start = pygame.image.load('StartButton.png')
exit = pygame.image.load('EscapeButton.png')
playAgain = pygame.image.load('ReplayButton.png')

#Making the background screen
screen = pygame.display.set_caption("Slime Dodge")
backgroundImage = pygame.image.load('Background.png')
backgroundImage = pygame.transform.scale(backgroundImage,(800,600))
screen = pygame.display.set_mode((800,600))
color = (0,0,200)

#Draw exit menu
def DrawExitMenu(gm,eAmount,h,sT,sC):
    #Buttons
    screen.blit(backgroundImage,(0,0))
    playButton.blit(playAgain,(200,100))
    exitButton.blit(exit,(200,300))

    #Restarting the inputs
    if keyboard[pygame.K_SPACE]:
        eAmount = 4
        h = 3
        sT = 0
        sC = 0
        gm = 1
    #Allowing for the exit of the game
    if keyboard[pygame.K_ESCAPE]:
        event.type = pygame.QUIT
    
    #Running the program
    pygame.display.update()
    return gm,eAmount,h,sT,sC

#Drawing the main menu
def DrawMainMenu(gm):
    #Button
    screen.blit(backgroundImage,(0,0))
    startButton.blit(start,(200,100))
    exitButton.blit(exit,(200,300))

    #If the player starts the game
    if keyboard[pygame.K_SPACE]:
        gm = 0
    if keyboard[pygame.K_ESCAPE]:
        event.type = pygame.QUIT
        
    #Running the program
    pygame.display.update()
    return gm


#The draw function
def Draw(xs,ys):
    screen.blit(backgroundImage,(0,0))
    #Drawing the player and other objects
    pl.blit(player,(xs,ys))

    #Drawing the enemys
    for i in range(0,enemyAmount):
        enemy.blit(enemyImage,(xPos[i],yPos[i]))

    #Drawing to screen
    text = font.render('Score: {}'.format(score), False, (0,0,0))
    screen.blit(text,(0,0))

    #Drawing players health
    for i in range(0,healthNumber):
        Health[i].blit(healthImage,(healthX[i],-20))

    pygame.display.update()
    return xs, ys

# Enemy Spawn Speed
def SpawnEnemy(speed,eAmount,x,y,s,sT):
    x = xPos
    y = yPos
    s = enemySpeed
    #Respawning the enemy
    speed += .1
    if speed > sT:
        eAmount += 1
        x.append(770) 
        y.append(random.randint(1,570))
        s.append(random.uniform(.1,.7))
        sT += 600
        speed = 0

    return speed,eAmount,x,y,s,sT


# the player controls
def ControlsAndCollision(xs,ys,xp,yp,sc,hNum,gm):
     #The controls
    if keyboard[pygame.K_d]:
        xs += playerSpeed
    if keyboard[pygame.K_a]:
        xs -= playerSpeed
    if keyboard[pygame.K_w]:
        ys -= playerSpeed
    if keyboard[pygame.K_s]:
        ys += playerSpeed

    #The boundaries for the player
    if xs > screen.get_width() - 30:
        xs = screen.get_width() - 30
    if xs < 0:
        xs = 0
    if ys > screen.get_height() - 30:
        ys = screen.get_height() - 30
    if ys < 0:
        ys = 0

    #Enemy boundary and collision
    for i in range(0,enemyAmount):
        #Collision 
        if xs > xp[i] - 10 and xs < xp[i] + 10 and ys > yp[i] - 10 and ys < yp[i] + 10:
            xs = 0
            ys = 0
            hNum -= 1

        #Respawning 
        if xp[i] < 0:
            xp[i] = 770
            yp[i] = random.randint(0,570)

    #Enemy Speed Loop
    for i in range(0,enemyAmount):
        xp[i] -= enemySpeed[i]
    
    for i in range(0,enemyAmount):
        if xs != xp[i] and ys > yp[i] - 3 and ys < yp[i] + 3:
            sc += 1
    
    if hNum <= 0:
        gm = 2
        #event.type = pygame.QUIT

    return xs , ys , xp , yp , sc , hNum , gm

# the gameloop
while True:
    screen.fill(color)

    #Recieving keyboard inputs
    keyboard = pygame.key.get_pressed()
    for event in pygame.event.get():
        #Allowing the player to leave the game
        if keyboard[pygame.K_ESCAPE]:
            event.type = pygame.QUIT

        #The end game sequence
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    #Drawing the update sequence
    if GameStates == 0:
        #Running the program
        enemySpawnSpeed,enemyAmount,xPos,yPos,enemySpeed,spawnTime = SpawnEnemy(enemySpawnSpeed,enemyAmount,xPos,yPos,enemySpeed,spawnTime)
        x,y,xPos,yPos,score,healthNumber,GameStates = ControlsAndCollision(x,y,xPos,yPos,score,healthNumber,GameStates)
        x,y = Draw(x,y)

    #Drawing the main menu
    if GameStates == 1:
        GameStates = DrawMainMenu(GameStates)

    #Drawing the exit menu
    if GameStates == 2:
        GameStates,enemyAmount,healthNumber,spawnTime,score = DrawExitMenu(GameStates,enemyAmount,healthNumber,spawnTime,score)
    #d
    

    
