import pygame
from pygame import mixer

import random
import math

pygame.init()

screen = pygame.display.set_mode((1280, 720))
background = pygame.image.load('background.png')

mixer.music.load('background.mp3')
mixer.music.play(-1)

pygame.display.set_caption("TiKi Invaders 2")
icon = pygame.image.load('app_icon.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 240
playerY = 580
playerX_change = 0
playerY_change = 0
# Player1
player1Img = pygame.image.load('player1.png')
player1X = 980
player1Y = 580
player1X_change = 0
player1Y_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 3

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 1000))
    enemyY.append(random.randint(0, 250))
    enemyX_change.append(30)
    enemyY_change.append(55)

enemy1Img = []
enemy1X = []
enemy1Y = []
enemy1X_change = []
enemy1Y_change = []
num_of_enemies1 = 3

for i in range(num_of_enemies1):
    enemy1Img.append(pygame.image.load('enemy1.png'))
    enemy1X.append(random.randint(0, 1000))
    enemy1Y.append(random.randint(0, 250))
    enemy1X_change.append(30)
    enemy1Y_change.append(55)

# Bullet
# Ready - you can't see the bullet on the screen
# Fire - the bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 580
bulletX_change = 0
bulletY_change = 150
bullet_state = "ready"

bullet1Img = pygame.image.load('bullet1.png')
bullet1X = 0
bullet1Y = 580
bullet1X_change = 0
bullet1Y_change = 150
bullet1_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 52)
your_font = pygame.font.Font('freesansbold.ttf', 60)

textX = 10
textY = 10

# Game Over TextX
over_font = pygame.font.Font('freesansbold.ttf', 100)


def show_score(x, y):
    score = font.render("SCORE : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (230, 10, 10))
    score = your_font.render("YOUR SCORE : " + str(score_value), True, (0, 255, 255))
    screen.blit(over_text, (440, 350))
    screen.blit(score, (280, 300))


def player(x, y):
    screen.blit(playerImg, (x, y))


def player1(x, y):
    screen.blit(player1Img, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def enemy1(x, y, i):
    screen.blit(enemy1Img[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 35, y + 0))


def fire_bullet1(x, y):
    global bullet1_state
    bullet1_state = 'fire'
    screen.blit(bullet1Img, (x + 35, y + 0))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 100:
        return True
    else:
        return False


def iscollision1(enemy1X, enemy1Y, bullet1X, bullet1Y):
    distance1 = math.sqrt((math.pow(enemy1X - bullet1X, 2)) + (math.pow(enemy1Y - bullet1Y, 2)))
    if distance1 < 100:
        return True
    else:
        return False


running = True
while running:
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Player Controls
            if event.key == pygame.K_LEFT:
                playerX_change = -12
            if event.key == pygame.K_RIGHT:
                playerX_change = 12
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                # Get the current x coordinate of the spaceship
                if bullet_state == "ready":
                    bulletX = playerX
                fire_bullet(bulletX, bulletY)
            # Player1 Controls
            if event.key == pygame.K_a:
                player1X_change = -12
            if event.key == pygame.K_d:
                player1X_change = 12
            if event.key == pygame.K_j:
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                # Get the current x coordinate of the spaceship
                if bullet1_state == "ready":
                    bullet1X = player1X
                fire_bullet1(bullet1X, bullet1Y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0
                player1X_change = 0

    playerX += playerX_change  # Player Movement
    if playerX <= 20:  # Checking for boundaries  for Player, so it doesn't go outside the screen
        playerX = 20
    elif playerX >= 1180:
        playerX = 1180
    player1X += player1X_change
    if player1X <= 20:
        player1X = 20
    elif player1X >= 1180:
        player1X = 1180

    # Game Over
    for i in range(num_of_enemies or num_of_enemies1):
        if enemyY[i] > 500 or enemy1Y[i] > 500:
            for j in range(num_of_enemies or enemy1Y[i] > 500):
                enemyY[j] = 2000
                enemy1Y[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]  # Enemy Movement
        if enemyX[i] <= 20:  # Checking for boundaries  for Enemy, so it doesn't go outside the screen
            enemyX_change[i] = 7
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 1180:
            enemyX_change[i] = -7
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 580
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 1000)
            enemyY[i] = random.randint(0, 250)

        enemy(enemyX[i], enemyY[i], i)

    for i in range(num_of_enemies and num_of_enemies1):
        if enemyY[i] > 500 and enemy1Y[i] > 500:
            for j in range(num_of_enemies and enemy1Y[i] > 500):
                enemyY[j] = 2000
                enemy1Y[j] = 2000
            game_over_text()
            break

        enemy1X[i] += enemy1X_change[i]  # Enemy Movement
        if enemy1X[i] <= 20:  # Checking for boundaries  for Enemy, so it doesn't go outside the screen
            enemy1X_change[i] = 5
            enemy1Y[i] += enemy1Y_change[i]
        elif enemy1X[i] >= 1180:
            enemy1X_change[i] = -5
            enemy1Y[i] += enemy1Y_change[i]

        collision1 = iscollision1(enemy1X[i], enemy1Y[i], bullet1X, bullet1Y)
        if collision1:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bullet1Y = 580
            bullet1_state = "ready"
            score_value += 1
            enemy1X[i] = random.randint(0, 1000)
            enemy1Y[i] = random.randint(0, 250)

        enemy1(enemy1X[i], enemy1Y[i], i)

    # Bullet Movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:
        bulletY = 580
        bullet_state = "ready"

    if bullet1_state == "fire":
        fire_bullet1(bullet1X, bullet1Y)
        bullet1Y -= bullet1Y_change
    if bullet1Y <= 0:
        bullet1Y = 580
        bullet1_state = "ready"

    player1(player1X, player1Y)
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
