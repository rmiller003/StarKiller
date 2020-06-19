import pygame
import random
import math

# intialize the pygame
pygame.init()

# create a screen
screen = pygame.display.set_mode((800, 600))

# Game Background
background = pygame.image.load('StarBK.png')

# Title and Icon
pygame.display.set_caption("Star Killers")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('starship.png')
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)
    # bullet_state = "ready"

# Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

score = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletY, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    playerX -= 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # iF a keystroke is pressed, check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    # Get the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(playerX, playerY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

        # Checking for boundaries of the space ship so it doesn't go out of bounds
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy Movement
        for i in range(num_of_enemies):
            enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score += 1
            print(score)
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
    bulletY -= bulletY_change

player(playerX, playerY)

pygame.display.update()
