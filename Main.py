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
shield_duration = 101 # Shield duration in frames

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
speed_increase_timer = 600 # 10 seconds at 60 FPS

# Super Alien
super_alienImg = pygame.transform.scale(pygame.image.load('ufo.png'), (128, 128))
super_alien_active = False
super_alien_timer = random.randint(500, 1000) # Time until first appearance
super_alienX = 0
super_alienY = 20
super_alienX_change = 2

# Nuke
nukeImg = pygame.transform.scale(pygame.image.load('bullet.png'), (32, 32))
nukes = []
nukeY_change = 1 # Slower drop speed

# Explosions
nuke_explosion_active = False
nuke_explosion_timer = 0
nuke_explosion_radius = 10
nuke_explosion_x = 0
nuke_explosion_y = 0

player_explosion_active = False
player_explosion_timer = 0
player_explosion_radius = 10
player_explosion_x = 0
player_explosion_y = 0

super_alien_explosion_active = False
super_alien_explosion_timer = 0
super_alien_explosion_radius = 10
super_alien_explosion_x = 0
super_alien_explosion_y = 0


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
next_shield_score = 20
next_life_score = 1000
font = pygame.font.Font('freesansbold.ttf', 33)
ui_font = pygame.font.Font('freesansbold.ttf', 24)
textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 50)
restart_font = pygame.font.Font('freesansbold.ttf', 20)

game_state = "playing"

def reset_game():
    global playerX, playerY, score_value, player_bullets, enemy_bullets, shield_charges, shield_active, shield_timer, player_lives, next_shield_score, super_alien_active, super_alien_timer, nuke_explosion_active, speed_increase_timer, next_life_score
    playerX = (screen_width - player_width) / 2
    playerY = screen_height - 100
    score_value = 0
    player_bullets = []
    enemy_bullets = []
    shield_charges = 3
    shield_active = False
    shield_timer = 0
    player_lives = 4
    next_shield_score = 20
    next_life_score = 1000
    super_alien_active = False
    super_alien_timer = random.randint(500, 1000)
    nuke_explosion_active = False
    speed_increase_timer = 600
    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, screen_width - 64)
        enemyY[i] = random.randint(50, 150)
        enemyX_change[i] = 2.8812

def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))

def show_shield_charges(x, y):
    shields_text = ui_font.render("Shields: " + str(shield_charges), True, (0, 255, 255))
    screen.blit(shields_text, (x, y))

def show_lives(x, y):
    lives_text = ui_font.render("Lives: " + str(player_lives), True, (255, 255, 255))
    screen.blit(lives_text, (x, y))

def game_over_screen():
    global nuke_explosion_active, nuke_explosion_timer, nuke_explosion_radius, nuke_explosion_x, nuke_explosion_y
    if nuke_explosion_active:
        if nuke_explosion_timer > 0:
            pygame.draw.circle(screen, (255, 165, 0), (nuke_explosion_x, nuke_explosion_y), nuke_explosion_radius)
            nuke_explosion_radius += 5
            nuke_explosion_timer -= 1
        else:
            nuke_explosion_active = False
    else:
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

def super_alien(x,y):
    screen.blit(super_alienImg, (x,y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_player_bullet(x, y):
    player_bullets.append({'x': x, 'y': y})

def fire_enemy_bullet(x, y):
    enemy_bullets.append({'x': x, 'y': y})

def fire_nuke(x,y):
    nukes.append({'x':x, 'y':y})

def isCollision(obj1X, obj1Y, obj2X, obj2Y, size=27):
    distance = math.sqrt((math.pow(obj1X - obj2X, 2)) + (math.pow(obj1Y - obj2Y, 2)))
    if distance < size:
        return True
    else:
        return False

# Initialize enemies
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, screen_width - 64))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2.8812)
    enemyY_change.append(0.05) # Downward trend

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
                if event.key == pygame.K_r and not nuke_explosion_active:
                    reset_game()
                    game_state = "playing"

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    if game_state == "playing":
        # Player Movement
        if not player_explosion_active:
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

        # Speed Increase Timer
        speed_increase_timer -= 1
        if speed_increase_timer <= 0:
            for i in range(num_of_enemies):
                if enemyX_change[i] > 0:
                    enemyX_change[i] += 0.5
                else:
                    enemyX_change[i] -= 0.5
            speed_increase_timer = 600

        # Score-based rewards
        if score_value >= next_shield_score:
            shield_charges += 1
            next_shield_score += 20
        if score_value >= next_life_score:
            player_lives += 1
            next_life_score += 1000

        # Super Alien Logic
        if not super_alien_active:
            super_alien_timer -= 1
            if super_alien_timer <= 0:
                super_alien_active = True
                super_alienX = 0
        else:
            super_alienX += super_alienX_change
            if super_alienX <= 0:
                super_alienX_change = 2
            elif super_alienX >= screen_width - 128:
                super_alienX_change = -2

            super_alien(super_alienX, super_alienY)
            if random.randint(0, 100) < 1:
                fire_nuke(super_alienX, super_alienY)

        # Enemy Movement and Firing
        for i in range(num_of_enemies):
            enemyY[i] += enemyY_change[i] # Downward trend
            if enemyY[i] > screen_height - 120:
                player_lives = 0
                game_state = "game_over"
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = abs(enemyX_change[i])
            elif enemyX[i] >= screen_width - 64:
                enemyX_change[i] = -abs(enemyX_change[i])

            if random.randint(0, 200) < 1:
                fire_enemy_bullet(enemyX[i], enemyY[i])

            enemy(enemyX[i], enemyY[i], i)

        # Player Bullet Movement and Collision
        for bullet in player_bullets[:]:
            screen.blit(playerBulletImg, (bullet['x'] + 16, bullet['y'] + 10))
            bullet['y'] -= player_bulletY_change

            # Super Alien Collision
            if super_alien_active and isCollision(super_alienX + 64, super_alienY + 64, bullet['x'], bullet['y'], size=64):
                super_alien_explosion_x = int(super_alienX + 64)
                super_alien_explosion_y = int(super_alienY + 64)
                super_alien_explosion_active = True
                super_alien_explosion_timer = 40
                super_alien_explosion_radius = 20
                explosion_Sound = mixer.Sound('explosion.wav')
                explosion_Sound.play()
                player_bullets.remove(bullet)
                score_value += 100
                super_alien_active = False
                super_alien_timer = random.randint(1000, 2000)
                continue

            # Nuke Collision
            for nuke in nukes[:]:
                if isCollision(nuke['x'], nuke['y'], bullet['x'], bullet['y'], size=32):
                    explosion_Sound = mixer.Sound('explosion.wav')
                    explosion_Sound.play()
                    player_bullets.remove(bullet)
                    nukes.remove(nuke)
                    score_value += 50
                    break

            # Enemy Collision
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
                        player_explosion_x = int(playerX + player_width/2)
                        player_explosion_y = int(playerY + player_width/2)
                        player_explosion_active = True
                        player_explosion_timer = 20
                        player_explosion_radius = 10
                        playerX = -2000 # Move player off screen during explosion
                break

            if bullet['y'] > screen_height:
                try:
                    enemy_bullets.remove(bullet)
                except ValueError:
                    pass

        # Nuke Movement and Collision
        for nuke in nukes[:]:
            screen.blit(nukeImg, (nuke['x'] + 16, nuke['y'] + 10))
            nuke['y'] += nukeY_change
            if isCollision(playerX, playerY, nuke['x'], nuke['y'], size=35):
                nuke_explosion_x = int(playerX + player_width/2)
                nuke_explosion_y = int(playerY + player_width/2)
                nuke_explosion_active = True
                nuke_explosion_timer = 30
                nuke_explosion_radius = 10
                game_state = "game_over"
                break
            if nuke['y'] > screen_height:
                try:
                    nukes.remove(nuke)
                except ValueError:
                    pass

        if game_state == "game_over" and not nuke_explosion_active:
            continue

        # Player Explosion
        if player_explosion_active:
            if player_explosion_timer > 0:
                pygame.draw.circle(screen, (255, 0, 0), (player_explosion_x, player_explosion_y), player_explosion_radius)
                player_explosion_radius += 3
                player_explosion_timer -= 1
            else:
                player_explosion_active = False
                playerX = (screen_width - player_width) / 2
                playerY = screen_height - 100
        else:
            player(playerX, playerY)

        # Super Alien Explosion
        if super_alien_explosion_active:
            if super_alien_explosion_timer > 0:
                pygame.draw.circle(screen, (255, 255, 0), (super_alien_explosion_x, super_alien_explosion_y), super_alien_explosion_radius)
                super_alien_explosion_radius += 10
                super_alien_explosion_timer -= 1
            else:
                super_alien_explosion_active = False

        show_score(textX, textY)
        show_shield_charges(textX, textY + 40)
        show_lives(screen_width - 120, textY)

    elif game_state == "game_over":
        game_over_screen()

    pygame.display.update()
