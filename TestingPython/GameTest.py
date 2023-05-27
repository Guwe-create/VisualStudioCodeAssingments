import pygame
import random

from pygame.locals import *
pygame.init()

pygame.font.init()

font = pygame.font.SysFont('Comic Sans MS', 30)
text = font.render('Score: 0', False, (0,0,0))
score = 0

#Player information
pl = pygame.display.set_mode((50,50))
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

#Making the background screen
screen = pygame.display.set_caption("Liam Game")
screen = pygame.display.set_mode((800,600))
color = (0,0,200)

#The draw function
def Draw(xs,ys):
    #Drawing the player and other objects
    pl.blit(player,(xs,ys))

    #Drawing to screen
    text = font.render('Score: {}'.format(score), False, (0,0,0))
    screen.blit(text,(0,0))

    #Drawing the enemys
    for i in range(0,enemyAmount):
        enemy.blit(enemyImage,(xPos[i],yPos[i]))

    pygame.display.update()
    return xs, ys

# the player controls
def ControlsAndCollision(xs,ys,xp,yp,sc):

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
    

    return xs , ys , xp , yp , sc

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
            
    x,y,xPos,yPos,score = ControlsAndCollision(x,y,xPos,yPos,score)
    x,y = Draw(x,y)
    
