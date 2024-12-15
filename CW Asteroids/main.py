
import pygame
import math
import random
pygame.init()

screen = pygame.display.set_mode((800,800))
pygame.display.set_caption("Asteroids")

WIDTH = 800
HEIGHT = 800

asteroid50 = pygame.image.load("asteroidPics/asteroid50.png")
asteroid100 = pygame.image.load("asteroidPics/asteroid100.png")
asteroid150 = pygame.image.load("asteroidPics/asteroid150.png")
rocket = pygame.image.load("asteroidPics/spaceRocket.png")
alienShip = pygame.image.load("asteroidPics/alienShip.png")
star = pygame.image.load("asteroidPics/star.png")
bg = pygame.image.load("asteroidPics/starbg.png")

bangLarge = pygame.mixer.Sound("sounds/bangLarge.wav")
bangSmall = pygame.mixer.Sound("sounds/bangSmall.wav")
shootSound = pygame.mixer.Sound("sounds/shoot.wav")

# - changing the volume
bangLarge.set_volume(0.7)
bangSmall.set_volume(1.5)
shootSound.set_volume(0.3)

clock = pygame.time.Clock()
gameover = False
lives = 3
score = 0
rapidfire = False
isSoundOn = True
rfStart = -1
asteroids = []
playerBullets = []
aliens = []
alienBullets = []
run = True
count = 0

class Player():
    def __init__(self):
        self.image = rocket
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.angle = 0
        self.rotatedSurface = pygame.transform.rotate(self.image, self.angle)
        self.rotatedRect = self.rotatedSurface.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def drawPlayer(self, window):
        window.blit(self.rotatedSurface, self.rotatedRect)

    def turnLeft(self):
        self.angle += 5
        self.rotatedSurface = pygame.transform.rotate(self.image, self.angle)
        self.rotatedRect = self.rotatedSurface.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosin  * self.w//2, self.y - self.sine * self.h//2)
    
    def turnRight(self):
        self.angle -= 5
        self.rotatedSurface = pygame.transform.rotate(self.image, self.angle)
        self.rotatedRect = self.rotatedSurface.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosin  * self.w//2, self.y - self.sine * self.h//2)
    
    def moveForward(self):
        self.x += self.cosine * 6
        self.y -= self.sine * 6
        self.rotatedSurface = pygame.transform.rotate(self.image, self.angle)
        self.rotatedRect = self.rotatedSurface.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosin  * self.w//2, self.y - self.sine * self.h//2)

    def update(self):
        if self.x > WIDTH + 50:
            self.x = 0
        elif self.x < 0 - self.w:
            self.x = WIDTH
        elif self.y < -50:
            self.y = HEIGHT
        elif self.y > HEIGHT + 50:
            self.y = 0

class Bullet(object):
    def __init__(self):
        self.point = player.head
        self.x , self.y = self.point
        self.w = 4
        self.h = 4
        self.cosine = player.cosine
        self.sine = player.sine
        self.vx = self.cosine * 10
        self.vy = self.sine * 10
    
    def move(self):
        self.x += self.vx
        self.y += self.vy
    
    def drawBullets(self, window):
        pygame.draw.rect(window, (255,255,255), [self.x, self.y, self.w, self.h])

    def outOfScreen(self):
        if self.x < -50 or self.x > WIDTH or self.y < -50 or self.y > HEIGHT:
            return True

class Asteroid(object):
    def __init__(self, rank): # - rank is which size asteroid is going to be displayed
        self.rank = rank

        if rank == 1:
            self.image = asteroid50
        elif rank == 2:
            self.image = asteroid100
        else:
            self.image = asteroid150
        
        self.width = 50 * rank
        self.height = 50 * rank
        self.randpos = random.choice[(random.randrange(0, WIDTH - self.width), random.choice([-1 * self.height - 5, HEIGHT + 5])), (random.choice([-1 * self.width - 5, WIDTH + 5]), random.randrange(0, HEIGHT - self.height))]
        self.x , self.y = self.randpos

        # - choosing velocity

        if self.x < WIDTH//2:
            self.xdir = 1
        else:
            self.xdir = -1
        
        if self.y < HEIGHT//2:
            self.ydir = 1
        else:
            self.ydir = -1

        self.velx = self.xdir * random.randrange(1,3)
        self.vely = self.ydir * random.randrange(1,3)

    def drawAsteroid(self, window):
        window.blit(self.image, (self.x, self.y))

class Alien(object):
    def __init__(self):
        self.image = alienShip
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.randpos = random.choice[(random.randrange(0, WIDTH - self.width), random.choice([-1 * self.height - 5, HEIGHT + 5])), (random.choice([-1 * self.width - 5, WIDTH + 5]), random.randrange(0, HEIGHT - self.height))]
        self.x , self.y = self.randpos

        if self.x < WIDTH//2:
            self.xdir = 1
        else:
            self.xdir = -1
        
        if self.y < HEIGHT//2:
            self.ydir = 1
        else:
            self.ydir = -1

        self.velx = self.xdir * random.randrange(1,3)
        self.vely = self.ydir * random.randrange(1,3)

    def drawAlien(self, window):
        window.blit(self.image, (self.x, self.y))

class AleinBullet(object):
    def __init__(self, x, y):
        self.width = 4
        self.height = 4
        self.x = x
        self.y = y
        self.dx, self.dy = player.x - self.x, player.y - self.y
        self.distance = math.hypot(self.dx, self.dy) # - gives dis. between 2 points
        self.dx = self.dx//self.distance
        self.dy = self.dy//self.distance
        self.xvel = self.dx * 5
        self.yvel = self.dy * 5
    
    def drawAlienBullet(self, window):
        pygame.draw.rect(window, (255,255,255), [self.x, self.y, self.width, self.height])

def redrawGameWindow():
    screen.blit(bg, (0,0))
    font = pygame.font.SysFont("arial", 30)
    livesT = font.render(f"Lives : {lives}", 1, (255,255,255))
    scoreT = font.render(f"Score : {score}", 1, (255,255,255))
    playAgainT = font.render(f"Press TAB to Play Again!", 1, (255,255,255))

    player.drawPlayer(screen)
    for asteroid in asteroids:
        asteroid.drawAsteroid(screen)
    for alien in aliens:
        alien.drawAlien(screen)
    for alienB in alienBullets:
        alienB.drawAlienBullet(screen)
    for b in playerBullets:
        b.drawBullets(screen)
    
    if rapidfire:
        pygame.draw.rect(screen, (0,0,0), [WIDTH//2 - 51, 19, 102, 22])
        pygame.draw.rect(screen, (255,255,255), [WIDTH//2 - 50, 20, 100 - 100 * (count - rfStart)//500, 20])
    
    if gameover:
        screen.blit(playAgainT, (WIDTH//2 - playAgainT.get_width()//2, HEIGHT//2 - playAgainT.get_height()//2 ))

    screen.blit(scoreT, (WIDTH - scoreT.get_width() - 25, 25))
    screen.blit(livesT, (25,25))

    pygame.display.update()

player = Player()



while run:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)