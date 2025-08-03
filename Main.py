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
laser_sound = mixer.Sound('laser.wav')

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
shield_duration = 202 # Shield duration in frames
player_double_shot_unlocked = False

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
num_of_enemies = 6
speed_increase_timer = 600 # 10 seconds at 60 FPS
speed_increases = 0
horizontal_passes = 0
alien_double_shot_unlocked = False

# Super Alien
super_alienImg = pygame.transform.scale(pygame.image.load('ufo.png'), (128, 128))
super_alien_active = False
super_alien_timer = random.randint(500, 1000) # Time until first appearance
super_alienX = 0
super_alienY = 20
super_alienX_change = 2

# Nuke
nuke_base_img = pygame.image.load('bullet.png')
nuke_red_img = pygame.Surface(nuke_base_img.get_size()).convert_alpha()
nuke_red_img.fill((255,0,0, 255))
nuke_img_final = nuke_base_img.copy()
nuke_img_final.blit(nuke_red_img, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
nukeImg = pygame.transform.scale(nuke_img_final, (32, 32))
nukes = []
nukeY_change = 1 # Slower drop speed

# Explosions
explosions = [] # General list for all explosions

# Player Bullet
playerBulletImg = pygame.image.load('bullet.png')
player_bullets = [] # List to store multiple bullets
player_bulletY_change = 5

# Enemy Bullet
enemy_bullet_base_img = pygame.image.load('bullet.png').convert_alpha()
enemy_bullet_blue_img = pygame.Surface(enemy_bullet_base_img.get_size()).convert_alpha()
enemy_bullet_blue_img.fill((0,0,255, 255))
enemy_bullet_img_final = enemy_bullet_base_img.copy()
enemy_bullet_img_final.blit(enemy_bullet_blue_img, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
enemyBulletImg = pygame.transform.flip(enemy_bullet_img_final, False, True)
enemy_bullets = []
enemy_bulletY_change = 4

# Score
score_value = 0
next_shield_score = 20
next_life_score = 1000
next_500_point_reward = 500
next_1000_point_reward = 1000
font = pygame.font.Font('freesansbold.ttf', 33)
ui_font = pygame.font.Font('freesansbold.ttf', 24)
textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 50)
restart_font = pygame.font.Font('freesansbold.ttf', 20)

game_state = "playing"

def reset_game():
    global playerX, playerY, score_value, player_bullets, enemy_bullets, shield_charges, shield_active, shield_timer, player_lives, next_shield_score, super_alien_active, super_alien_timer, speed_increase_timer, next_life_score, explosions, horizontal_passes, player_double_shot_unlocked, next_500_point_reward, speed_increases, alien_double_shot_unlocked, next_1000_point_reward
    playerX = (screen_width - player_width) / 2
    playerY = screen_height - 100
    score_value = 0
    player_bullets = []
    enemy_bullets = []
    explosions = []
    shield_charges = 3
    shield_active = False
    shield_timer = 0
    player_lives = 4
    next_shield_score = 20
    next_life_score = 1000
    next_500_point_reward = 500
    next_1000_point_reward = 1000
    player_double_shot_unlocked = False
    alien_double_shot_unlocked = False
    super_alien_active = False
    super_alien_timer = random.randint(500, 1000)
    speed_increase_timer = 600
    speed_increases = 0
    horizontal_passes = 0
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

def game_over_screen(final_score):
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    score_text = font.render("Final Score: " + str(final_score), True, (255, 255, 255))
    restart_text = restart_font.render("Press R to Restart", True, (255, 255, 255))

    over_text_rect = over_text.get_rect(center=(screen_width/2, screen_height/2 - 100))
    score_text_rect = score_text.get_rect(center=(screen_width/2, screen_height/2))
    restart_text_rect = restart_text.get_rect(center=(screen_width/2, screen_height/2 + 50))

    screen.blit(over_text, over_text_rect)
    screen.blit(score_text, score_text_rect)
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
    if player_double_shot_unlocked:
        player_bullets.append({'x': x - 15, 'y': y})
        player_bullets.append({'x': x + 15, 'y': y})
    else:
        player_bullets.append({'x': x, 'y': y})


def fire_enemy_bullet(x, y):
    if alien_double_shot_unlocked:
        enemy_bullets.append({'x': x - 15, 'y': y})
        enemy_bullets.append({'x': x + 15, 'y': y})
    else:
        enemy_bullets.append({'x': x, 'y': y})

def fire_nuke(x,y):
    nukes.append({'x':x, 'y':y})

def start_explosion(x, y, radius, duration, color):
    explosions.append({'x': x, 'y': y, 'radius': radius, 'timer': duration, 'color': color})

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
                        laser_sound.play()
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

        # Speed Increase Timer
        speed_increase_timer -= 1
        if speed_increase_timer <= 0 and speed_increases < 4:
            for i in range(num_of_enemies):
                if enemyX_change[i] > 0:
                    enemyX_change[i] += 0.5
                else:
                    enemyX_change[i] -= 0.5
            speed_increase_timer = 600
            speed_increases += 1

        # Score-based rewards
        if score_value >= next_shield_score:
            shield_charges += 1
            next_shield_score += 20
        if score_value >= next_life_score:
            player_lives += 1
            next_life_score += 1000
        if score_value >= next_500_point_reward:
            player_lives += 2
            alien_double_shot_unlocked = True
            next_500_point_reward += 500
        if score_value >= next_1000_point_reward:
            player_double_shot_unlocked = True
            next_1000_point_reward += 1000


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
            if enemyY[i] > screen_height:
                player_lives -= 1
                if player_lives <= 0:
                    game_state = "game_over"
                else:
                    enemyX[i] = random.randint(0, screen_width - 64)
                    enemyY[i] = random.randint(50, 150)
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0 or enemyX[i] >= screen_width - 64:
                enemyX_change[i] *= -1
                horizontal_passes += 1
                if horizontal_passes % 2 == 0:
                    for j in range(num_of_enemies):
                        enemyY[j] += 40

            if random.randint(0, 200) < 1:
                fire_enemy_bullet(enemyX[i], enemyY[i])

            enemy(enemyX[i], enemyY[i], i)

        # Player Bullet Movement and Collision
        for bullet in player_bullets[:]:
            screen.blit(playerBulletImg, (bullet['x'], bullet['y']))
            bullet['y'] -= player_bulletY_change

            # Super Alien Collision
            if super_alien_active and isCollision(super_alienX + 64, super_alienY + 64, bullet['x'], bullet['y'], size=64):
                start_explosion(super_alienX + 64, super_alienY + 64, 40, 40, (255, 255, 0))
                explosion_Sound = mixer.Sound('explosion.wav')
                explosion_Sound.play()
                player_bullets.remove(bullet)
                score_value += 100
                super_alien_active = False
                super_alien_timer = random.randint(1000, 2000)
                continue

            # Nuke Collision
            for nuke in nukes[:]:
                if bullet in player_bullets and isCollision(nuke['x'], nuke['y'], bullet['x'], bullet['y'], size=32):
                    start_explosion(nuke['x'], nuke['y'], 30, 30, (255, 165, 0))
                    explosion_Sound = mixer.Sound('explosion.wav')
                    explosion_Sound.play()
                    player_bullets.remove(bullet)
                    nukes.remove(nuke)
                    score_value += 50
                    break

            # Enemy Collision
            if bullet in player_bullets:
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
                    start_explosion(playerX + player_width/2, playerY + player_width/2, 20, 20, (255, 0, 0))
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

        # Nuke Movement and Collision
        for nuke in nukes[:]:
            screen.blit(nukeImg, (nuke['x'] + 16, nuke['y'] + 10))
            nuke['y'] += nukeY_change
            if isCollision(playerX, playerY, nuke['x'], nuke['y'], size=35):
                start_explosion(playerX + player_width/2, playerY + player_width/2, 50, 50, (255, 165, 0))
                game_state = "game_over"
                break
            if nuke['y'] > screen_height:
                start_explosion(nuke['x'], screen_height, 40, 40, (255, 165, 0))
                explosion_Sound = mixer.Sound('explosion.wav')
                explosion_Sound.play()
                score_value -= 100
                try:
                    nukes.remove(nuke)
                except ValueError:
                    pass

        if game_state == "game_over":
            continue

        player(playerX, playerY)

        # Draw Explosions
        for explosion in explosions[:]:
            pygame.draw.circle(screen, explosion['color'], (int(explosion['x']), int(explosion['y'])), int(explosion['radius']))
            explosion['radius'] += 5
            explosion['timer'] -= 1
            if explosion['timer'] <= 0:
                explosions.remove(explosion)

        show_score(textX, textY)
        show_shield_charges(textX, textY + 40)
        show_lives(screen_width - 120, textY)

    elif game_state == "game_over":
        game_over_screen(score_value)

    pygame.display.update()
