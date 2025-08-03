import pygame
import random
import math

from pygame import mixer

# intialize the pygame
pygame.init()

# create a screen
screen_width = 1024
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height))

# Game Background
background = pygame.image.load('StarBK.png')
background = pygame.transform.scale(background, (screen_width, screen_height))

# Background Sound
mixer.music.load('00_Race_Gamer_Soundtrack_136BPM.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Star Killers")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('starship.png')
player_width = 64
playerX = (screen_width - player_width) / 2
playerY = screen_height - 100
playerX_change = 0
player_lives = 4
shield_charges = 3
shield_active = False
shield_timer = 0
shield_duration = 100 # Shield duration in frames

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# Player Bullet
playerBulletImg = pygame.image.load('bullet.png')
player_bullets = [] # List to store multiple bullets
player_bulletY_change = 5

# Enemy Bullet
enemyBulletImg = pygame.transform.flip(playerBulletImg, False, True)
enemy_bullets = []
enemy_bulletY_change = 4

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 33)
ui_font = pygame.font.Font('freesansbold.ttf', 24)
textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 50)
restart_font = pygame.font.Font('freesansbold.ttf', 20)

game_state = "playing"

def reset_game():
    global playerX, playerY, score_value, player_bullets, enemy_bullets, shield_charges, shield_active, shield_timer, player_lives
    playerX = (screen_width - player_width) / 2
    playerY = screen_height - 100
    score_value = 0
    player_bullets = []
    enemy_bullets = []
    shield_charges = 3
    shield_active = False
    shield_timer = 0
    player_lives = 4
    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, screen_width - 64)
        enemyY[i] = random.randint(50, 150)

def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))

def show_shield_charges(x, y):
    shields_text = ui_font.render("Shields: " + str(shield_charges), True, (0, 255, 255))
    screen.blit(shields_text, (x, y))

def show_lives(x, y):
    lives_text = ui_font.render("Lives: " + str(player_lives), True, (255, 255, 255))
    screen.blit(lives_text, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER LOSER!!!", True, (0, 255, 0))
    restart_text = restart_font.render("Press R to Restart", True, (255, 255, 255))
    over_text_rect = over_text.get_rect(center=(screen_width/2, screen_height/2 - 50))
    restart_text_rect = restart_text.get_rect(center=(screen_width/2, screen_height/2))
    screen.blit(over_text, over_text_rect)
    screen.blit(restart_text, restart_text_rect)

def player(x, y):
    screen.blit(playerImg, (x, y))
    if shield_active:
        pygame.draw.circle(screen, (0, 255, 255, 100), (int(x + player_width/2), int(y + player_width/2)), 40, 2)


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_player_bullet(x, y):
    player_bullets.append({'x': x, 'y': y})

def fire_enemy_bullet(x, y):
    enemy_bullets.append({'x': x, 'y': y})

def isCollision(obj1X, obj1Y, obj2X, obj2Y):
    distance = math.sqrt((math.pow(obj1X - obj2X, 2)) + (math.pow(obj1Y - obj2Y, 2)))
    if distance < 27:
        return True
    else:
        return False

# Initialize enemies
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, screen_width - 64))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2.8812)
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
                    fire_player_bullet(playerX, playerY)
                if event.key == pygame.K_UP:
                    if shield_charges > 0 and not shield_active:
                        shield_active = True
                        shield_timer = shield_duration
                        shield_charges -= 1
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
        elif playerX >= screen_width - player_width:
            playerX = screen_width - player_width

        # Shield Timer
        if shield_active:
            shield_timer -= 1
            if shield_timer <= 0:
                shield_active = False

        # Enemy Movement and Firing
        for i in range(num_of_enemies):
            if enemyY[i] > screen_height - 120:
                player_lives = 0 # Game over if enemies reach the bottom
                game_state = "game_over"
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 2.8812
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= screen_width - 64:
                enemyX_change[i] = -2.8812
                enemyY[i] += enemyY_change[i]

            # Enemy Firing
            if random.randint(0, 200) < 1:
                fire_enemy_bullet(enemyX[i], enemyY[i])

            enemy(enemyX[i], enemyY[i], i)

        # Player Bullet Movement and Collision
        for bullet in player_bullets[:]:
            screen.blit(playerBulletImg, (bullet['x'] + 16, bullet['y'] + 10))
            bullet['y'] -= player_bulletY_change

            for i in range(num_of_enemies):
                if isCollision(enemyX[i], enemyY[i], bullet['x'], bullet['y']):
                    explosion_Sound = mixer.Sound('explosion.wav')
                    explosion_Sound.play()
                    player_bullets.remove(bullet)
                    score_value += 1
                    enemyX[i] = random.randint(0, screen_width - 64)
                    enemyY[i] = random.randint(50, 150)
                    break

            if bullet['y'] <= 0:
                try:
                    player_bullets.remove(bullet)
                except ValueError:
                    pass

        # Enemy Bullet Movement and Collision
        for bullet in enemy_bullets[:]:
            screen.blit(enemyBulletImg, (bullet['x'] + 16, bullet['y'] + 10))
            bullet['y'] += enemy_bulletY_change

            # Player Collision
            if isCollision(playerX, playerY, bullet['x'], bullet['y']):
                if shield_active:
                    enemy_bullets.remove(bullet)
                else:
                    explosion_Sound = mixer.Sound('explosion.wav')
                    explosion_Sound.play()
                    player_lives -= 1
                    enemy_bullets.remove(bullet)
                    if player_lives <= 0:
                        game_state = "game_over"
                    else:
                        playerX = (screen_width - player_width) / 2
                        playerY = screen_height - 100
                break

            if bullet['y'] > screen_height:
                try:
                    enemy_bullets.remove(bullet)
                except ValueError:
                    pass

        if game_state == "game_over": # break out of player/enemy updates
            continue

        player(playerX, playerY)
        show_score(textX, textY)
        show_shield_charges(textX, textY + 40)
        show_lives(screen_width - 120, textY)

    elif game_state == "game_over":
        game_over_text()

    pygame.display.update()
