import pygame
from gameObject import *
from pygame.locals import *
import time

pygame.init()


class Game:

    def __init__(self, screen, imageTable, font) -> None:
        self.imageTable = imageTable
        self.running = True 
        self.screen = screen
        self.imageTable = imageTable

        self.counter = 0 
        # create player object 
        self.player = Player(400, 300, imageTable["playerImg"])

        # create list of zombies
        self.zombies = []

        self.life = gameObject(760, 0, imageTable["heartImg"])

        self.font = font

        # create bullet 
        self.bullets = []
        self.bullet = Bullet(0,0, imageTable["bulletImg"])

        # create array of game items
        self.gameItems = []

        # set to true if we are in a round
        self.playing = False
        self.round = 1
        self.numZombies = 0
        self.maxZombies = 5
        self.zombieHealth = 2
            
    # end game
    def quit(self) -> None:
        self.running = False

    def init(self):
        pass

    # respond to all the events in a given cycle
    def runEvents(self, event):
        # check for quit
        if event.type == QUIT:
            self.quit()
        # if a key is pressed 
        elif event.type == KEYDOWN:
            # left arrow
            if event.key == K_LEFT:
                self.player.xLeft = True
            # right arrow 
            elif event.key == K_RIGHT:
                self.player.xRight = True
            # up arrow
            elif event.key == K_UP:
                self.player.yUp = True
            # down arrow
            elif event.key == K_DOWN:
                self.player.yDown = True
            # space 
        elif event.type == MOUSEBUTTONDOWN and event.button == 1 and self.player.hasBullets():
            bullet = Bullet(0,0,self.imageTable["bulletImg"])
            self.bullets.append(bullet)
            self.player.fire(bullet)
            
        # if a key is released 
        elif event.type == KEYUP:
            # left arrow
            if event.key == K_LEFT:
                self.player.xLeft = False
            # right arrow 
            if event.key == K_RIGHT:
                self.player.xRight = False            # up arrow
            if event.key == K_UP:
                self.player.yUp = False
            if event.key == K_DOWN:
                self.player.yDown = False

    # update and draw each object after running through events 
    def runFinal(self):
        if self.player.lives <= 0:
            self.running = False
        self.counter += 1
        # player  
        self.player.updateState()
        self.player.draw(self.screen)
        self.player.drawLives(self.life, self.screen)
        self.player.drawBullets(self.screen, self.font)
        # zombies
        if self.counter % 1000 == 0 and len(self.zombies) <= self.maxZombies and self.numZombies > 0:
            z = Zombie(0,0,self.imageTable["zombieImg"])
            z.setHealth(self.zombieHealth)
            self.zombies.append(z)
            self.numZombies -= 1
        for zombie in self.zombies:
            zombie.draw(self.screen)
            zombie.updateState(self.player)
        # bullet
        for bullet in self.bullets:
            bullet.updateState(self.zombies)
            if bullet.fired:
                bullet.draw(self.screen)
            else:
                self.bullets.remove(bullet)
        # game items
        if self.counter % 5000 == 0 and len(self.gameItems) <= 2:
            # if player does not have ammo, only generate ammo items, else, generate anything
            if not self.player.hasBullets():
                generatedGameItem = generateAmmoItem(self.imageTable)
            else:
                generatedGameItem = generateGameItem(self.imageTable)
            if generatedGameItem != None:
                self.gameItems.append(generatedGameItem)
            self.counter = 0 
        for gameItem in self.gameItems:
            gameItem.draw(self.screen)
            self.player.hitGameItem(gameItem, self.gameItems)
        # check for end of round
        if self.numZombies == 0 and len(self.zombies) == 0:
            self.playing = False
            self.counter = 0
            self.increaseRound()

    # displays the screen for in between a round and will set game data based on round number
    def displayRoundScreen(self):
        self.counter += 1
        if self.counter == 8000:
            self.numZombies, self.maxZombies, self.zombieHealth = self.getRoundData()
            self.counter = 0
            self.startRound()
        message = "Round {}!".format(self.round)
        rendMsg = self.font.render(message, True, (0,0,0))
        self.screen.blit(rendMsg, (328, 260))
        self.player.drawLives(self.life, self.screen)
        self.player.drawBullets(self.screen, self.font)
        
    def increaseRound(self):
        self.round += 1
        
   
    # returns the num of zombies, max num of zombies, and zombie health for each round
    def getRoundData(self):
        nZ = (self.round) * 5
        if self.round % 5 == 0:
            mZ = self.maxZombies + 5
        else:
            mZ = self.maxZombies
        if self.round % 10 == 0:
            zH = self.zombieHealth + 1
        else:
            zH = self.zombieHealth
        return nZ, mZ, zH

    def startRound(self):
        self.player.wipeEffect()
        self.player.center()
        self.player.stopMovement()
        self.bullets.clear()
        self.playing = True


        

        

        
         