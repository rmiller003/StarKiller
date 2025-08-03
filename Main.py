import pygame
import random
import math

from pygame import mixer

# intialize the pygame
pygame.init()

# create a screen
screen = pygame.display.set_mode((800, 600))

# Game Background
background = pygame.image.load('StarBK.png')

# Background Sound
mixer.music.load('00_Race_Gamer_Soundtrack_136BPM.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Star Killers")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('starship.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 33)
textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 50)
restart_font = pygame.font.Font('freesansbold.ttf', 20)

game_state = "playing"

def reset_game():
    global playerX, playerY, score_value, bullet_state
    playerX = 370
    playerY = 480
    score_value = 0
    bullet_state = "ready"
    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, 735)
        enemyY[i] = random.randint(50, 150)

def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER LOSER!!!", True, (0, 255, 0))
    restart_text = restart_font.render("Press R to Restart", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    screen.blit(restart_text, (300, 320))


def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Initialize enemies
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# Game Loop
running = True
while running:
    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_state == "playing":
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletX = playerX
                        fire_bullet(playerX, playerY)
            if game_state == "game_over":
                if event.key == pygame.K_r:
                    reset_game()
                    game_state = "playing"

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    if game_state == "playing":
        # Player Movement
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy Movement
        for i in range(num_of_enemies):
            if enemyY[i] > 440:
                game_state = "game_over"
                break

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
                explosion_Sound = mixer.Sound('explosion.wav')
                explosion_Sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        # Bullet Movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"
            bullet_Sound = mixer.Sound('laser.wav')
            bullet_Sound.play()
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, textY)

    elif game_state == "game_over":
        game_over_text()

    pygame.display.update()
