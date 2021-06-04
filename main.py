import pygame 
from game import Game

# begin pygame 
pygame.init()
pygame.display.set_caption("Zombie Hunter")

# create screen
screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))

playerImg = pygame.image.load("user.png").convert_alpha()
zombieImg = pygame.image.load("zombie.png").convert_alpha()
heartImg = pygame.image.load("heart.png").convert_alpha()
bulletImg = pygame.image.load("bullet.png").convert_alpha()
speedImg = pygame.image.load("speed.png").convert_alpha()

imageTable = {"playerImg" : playerImg, "zombieImg" : zombieImg, "heartImg" : heartImg, "bulletImg" : bulletImg, "speedImg" : speedImg}

font = pygame.font.Font('freesansbold.ttf', 32)

# create game object 
game = Game(screen, imageTable, font)
game.init()

# run the game 
while game.running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        game.runEvents(event)
    if game.playing:
        game.runFinal()
    else:
        game.displayRoundScreen()
    pygame.display.update()

