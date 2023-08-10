import pygame
import math
import random
from pygame import mixer
from sys import exit

#fps
fps = pygame.time.Clock()

# intialize the pygame
pygame.init()
        
# create the  screen
screen = pygame.display.set_mode((360, 640))
        
# background
bg = pygame.image.load('background.jpg')
bg = pygame.transform.scale(bg,(360,640))
        
# background music
mixer.music.load('background.wav')
mixer.music.play(-1)
        
# title & icon
pygame.display.set_caption("space_shooter")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)
        
# player
playerimg = pygame.image.load('battleship.png')
playerx = 145
playery = 550
playerx_change = 0
        
# alien
alienimg = []
alienx = []
alieny = []
alienx_change = []
alieny_change = []
num_of_alien = 5
        
for i in range(num_of_alien):
    alienimg.append((pygame.image.load('alien.png')))
    alienx.append(random.randint(0, 295))
    alieny.append(random.randint(50, 300))
    alienx_change.append(0.1)
    alieny_change.append(40)
    
    

# bullet
# ready - you can't see the bullet on screen
# fire  - is bullet currently moving
        
bulletimg = pygame.image.load('bullet.png')
bulletx = 0
bullety = 550
bulletx_change = 0
bullety_change = 0.5
bullet_state = "ready"
        
# score text
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textx = 10
texty = 10

# endgame text

over_font = pygame.font.Font('freesansbold.ttf', 32)

        
def show_score(x, y):
    score = font.render("score:" + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))
    

def show_over_text():
    over_text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (85, 320))
   
    
def player(x, y):
    screen.blit(playerimg, (x, y))
        
        
def alien(x, y, i):
    screen.blit(alienimg[i], (x, y))
        
        
def firebullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg, (x + 16, y + 10))
        
        
def iscollision(alienx, alieny, bulletx, bullety):
    distance = math.sqrt((math.pow(alienx - bulletx, 2)) + (math.pow(alieny - bullety, 2)))
    if distance < 27:
        return True
    else:
        return False
        
# gameloop

while True:

    # RGB; red,green,blue
    screen.fill((0, 0, 0))
    # bg image
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerx_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # get the current cordinate of the spaceship
                    bulletx = playerx
                    firebullet(bulletx, bullety)
            



        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0
           
       
    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    # checking for boundaries of spaceship so it doesn't go out of bounds
    playerx += playerx_change

    if playerx <= 0:
        playerx = 0
    elif playerx >= 295:
        playerx = 295

    # alien movement

    for i in range(num_of_alien):

        # Game Over
        if alieny[i] > 500:
            for j in range(num_of_alien):
                alieny[j] = 2000
            show_over_text()
            break



        alienx[i] += alienx_change[i]
        if alienx[i] <= 0:
            alienx_change[i] = 0.2
            alieny[i] += alieny_change[i]
        elif alienx[i] >= 295:
            alienx_change[i] = -0.2
            alieny[i] += alieny_change[i]



        # collision
        collision = iscollision(alienx[i], alieny[i], bulletx, bullety)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullety = 580
            bullet_state = "ready"
            score_value += 1
            alienx[i] = random.randint(0, 295)
            alieny[i] = random.randint(50, 300)

        alien(alienx[i], alieny[i], i)



    # bullet movement
    if bullety <= 0:
        bullety = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        firebullet(bulletx, bullety)
        bullety -= bullety_change

    player(playerx, playery)
    show_score(textx, texty)
    pygame.display.update()
    fps.tick(500)

