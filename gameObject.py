import pygame
import math
import random


# generic game object 
class gameObject:
    def __init__(self, x : int, y : int, imageFile) -> None:
        self.x = x
        self.y = y
        self.image = imageFile

    def draw(self, screen) -> None:
        screen.blit(self.image, (self.x, self.y))

# class for main player
class Player(gameObject):
    score = 0
    speed = .2
    xChange = 0
    yChange = 0
    xLeft = False
    xRight = False
    yUp = False
    yDown = False
    numBullets = 50
    vulnerable = True
    lives = 3
    lifeProtectionCoutner = 0 
    currGameItem = None
    effectStatus = False
    effectObj = None
    internalClock = 0
    effectDuration = 7500

    # gets the direction the player will move
    def getVelocity(self):
        return int(self.xRight) - int(self.xLeft), int(self.yDown) - int(self.yUp)

    # changes position and keeps in boundry
    def updateState(self):
        
        xVel, yVel = self.getVelocity()
        xSpeed, ySpeed = norm(xVel, yVel)
        self.x += xSpeed * self.speed
        self.y += ySpeed * self.speed
        self.keepInBoundry()
        self.protect()
        if self.currGameItem != None:
            self.currGameItem.use(self)
        if self.effectObj != None:
            if self.internalClock < self.effectDuration:
                self.internalClock += 1
            else:
                self.internalClock = 0
                self.effectObj.remove(self)
        

    
    # keeps object in window boundry 
    def keepInBoundry(self):
        if self.x > 768:
            self.x = 768
        elif self.x < 0:
            self.x = 0
        
        if self.y > 568:
            self.y = 568
        elif self.y < 0:
            self.y = 0

    # keeps track of whether the player is vulnerable to a zombie hit
    def protect(self):
        if not self.vulnerable and self.lifeProtectionCoutner < 1000:
            self.lifeProtectionCoutner += 1
        elif self.lifeProtectionCoutner >= 1000:
            self.vulnerable = True
            self.lifeProtectionCoutner = 0
    # creates a bullet object with proper starting and movement coordinates and rotates the bullet icon properly
    def fire(self, bullet):
        if self.hasBullets():
            mx, my = pygame.mouse.get_pos()
            bullet.xChange = mx - self.x
            bullet.yChange = my - self.y
            bullet.xChange, bullet.yChange = norm(bullet.xChange, bullet.yChange)
            bullet.xChange *= bullet.speed
            bullet.yChange *= bullet.speed
            bullet.angle = math.degrees(math.acos(bullet.xChange)) - 90
            if bullet.yChange > 0:
                bullet.angle = 90 + (90 - bullet.angle)
            bullet.image = pygame.transform.rotate(bullet.image, bullet.angle)
            bullet.x = self.x
            bullet.y = self.y
            bullet.fired = True
            self.numBullets -= 1

    # returns true if player has bullets      
    def hasBullets(self):
        return self.numBullets > 0

    # draws the correct number of lives to the screen
    def drawLives(self, lifeObj, screen):
        startX = lifeObj.x
        for i in range(self.lives):
            lifeObj.draw(screen)
            lifeObj.x -= 28
        lifeObj.x = startX
    # draw the number of bullets the player has
    def drawBullets(self, screen, font):
        rendTxt = font.render("x{}".format(self.numBullets), True, (0,0,0))
        screen.blit(rendTxt, (10, 10))
    # for a game item, increase its lifespan, if it reached lifespan remove from list, if player collides with it give item to player
    def hitGameItem(self, item, list):
        item.lifeSpan += 1
        if item.lifeSpan > 20000:
            list.remove(item)
        if isCollision(self, item):
            self.currGameItem = item
            list.remove(item)
    def wipeEffect(self):
        self.effectObj = None
        self.effectStatus = False
        self.effectDuration = 0
    def center(self):
        self.x = 400
        self.y = 300
    def stopMovement(self):
        self.xLeft, self.xRight = False, False
        self.yUp, self.yDown = False, False


# zombie object 
class Zombie(Player):
    xChange = 0
    yChange = 0
    speedBase = .1 
    speed = .1
    lives = 2

    # spawns outside of the frame randomly 
    def spawn(self):
        side = random.randint(0, 3)
        if side == 0:
            self.x = random.randint(-50, 0)
            self.y = random.randint(0, 600)
        elif side == 1:
            self.x = random.randint(0, 800)
            self.y = random.randint(-50, 0)
        elif side == 2:
            self.x = random.randint(800, 850)
            self.y = random.randint(0, 600)
        else:
            self.x = random.randint(0, 800)
            self.y = random.randint(600, 650)
    
    def __init__(self, x: int, y: int, imageFile: str) -> None:
        super().__init__(x, y, imageFile)
        self.spawn()

    # gets the direction to the player
    def directionToPlayer(self, player):
        self.xChange = player.x - self.x
        self.yChange = player.y - self.y 

    # changes the position of the zombie 
    def updateState(self, player):
        self.directionToPlayer(player)
        xVel, yVel = norm(self.xChange, self.yChange)
        self.x += self.speed * (xVel + random.randint(-1, 1)) 
        self.y += self.speed * (yVel + random.randint(-1, 1)) 
        self.hit(player)

    # checks to see if zombie can hit player, if so, it does 
    def hit(self, player):
        if isCollision(self, player) and player.vulnerable:
            player.lives -= 1
            player.vulnerable = False

    def setSpeed(self, n):
        if n == 0:
            return
        self.speed = n * self.speedBase

    def setHealth(self, n):
        self.lives = n
    
    


class Bullet(gameObject):
    speed = 1
    fired = False
    angle = 0
    
    def updateState(self, zombies):
        # not fired, do nothing
        if not self.fired:
            pass
        # if fired check if collided with zombies, if not, continue to move bullet 
        else: 
            if (self.x < 0 or self.x > 800) or (self.y < 0 or self.y > 600):
                self.fired = False
                return
            for zombie in zombies:
                if isCollision(self, zombie):
                    if zombie.lives > 1:
                        zombie.lives -= 1
                    else:
                        zombies.remove(zombie)
                    self.fired = False
                    return
            
            self.x += self.xChange * self.speed
            self.y += self.yChange * self.speed
                   
        
# normailze two values: x and y 
def norm(x, y):
    r = math.sqrt((x**2) + y**2)
    if not r == 0:
        return x / r, y / r
    return x, y

# gets distance between two points 
def distance(x1, y1, x2, y2):
    return math.sqrt((x1- x2)**2 + (y1 - y2)**2)
    

# detects if there is a collision between two game objects 
def isCollision(obj1, obj2):
    d = distance(obj1.x, obj1.y, obj2.x, obj2.y)
    if d < 25:
        return True
    return False 

# an object a player can use to get more ammo
class AmmoObject(gameObject):
    ammoAmount = 40
    lifeSpan = 0

    def use(self, player):
        player.numBullets += self.ammoAmount
        player.currGameItem = None
# an object a player can use to get another life   
class LifeObject(AmmoObject):
    lifeAmount = 1

    def use(self, player):
        player.lives += self.lifeAmount
        player.currGameItem = None
# an object a player can use to double their speed 
class SpeedObject(AmmoObject):
    speedAmount = 2
    def use(self, player):
        player.effectObj = self
        player.speed *= self.speedAmount
        player.effectStatus = True
        player.currGameItem = None

    def remove(self, player):
        player.effectObj = None
        player.speed /= self.speedAmount
        player.effectStatus = False

    def remove(self, player):
        player.effectObj = None
        player.speed /= self.speedAmount
        player.effectStatus = False

# generate any game item with different probabilities
def generateGameItem(table):
    xRandom = random.randint(16, 768)
    yRandom = random.randint(16, 568) 
    p = random.randint(0, 11)
    if p > 2:
        pass
    elif p == 0:
        return LifeObject(xRandom, yRandom, table["heartImg"])
    elif p == 1:
        return SpeedObject(xRandom, yRandom, table["speedImg"])
    elif p == 2:
        return AmmoObject(xRandom, yRandom, table["bulletImg"])

# generate an ammo item with 1/4 chance
def generateAmmoItem(table):
   xRandom = random.randint(16, 768)
   yRandom = random.randint(16, 568) 
   p = random.randint(0, 3)
   if p == 0:
       return AmmoObject(xRandom, yRandom, table["bulletImg"])