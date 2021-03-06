# imports
import pygame
from math import sqrt, floor
from random import choice
from time import sleep
# comments in this file are focused on collisions, not game loop

# some variables and constants
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALLS_SIZE = 35
NUMBER_OF_BALLS = 10
BALLS_SPEED = 1
STOP_TIME = 1000
PINK = (255, 0, 0)
PINK_LAUNCH_TIME = 1
PINK_SPEED = 5
PLAYER_SIZE = 20
COLLISION_HELPER = 2


# ball class
class Ball:

    def __init__(self, x, y, x_speed, y_speed, radius, color):
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.radius = radius
        self.color = color

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius + COLLISION_HELPER)


def collision_check(ball1, ball2):
    # finds distance between two centres of the balls and sum of their radiates
    center_distance = sqrt((ball1.x - ball2.x) ** 2 + (ball1.y - ball2.y) ** 2)
    two_radiates_sum = ball1.radius + ball2.radius
    # returns True when collision and False otherwise
    if center_distance <= two_radiates_sum:
        return True
    else:
        return False


def collision(ball1, ball2):
    # collision calculation
    # 1
    # unit normal vector
    un = [ball1.x - ball2.x, ball1.y - ball2.y]
    # unit tangent vector
    ut = [-un[1], un[0]]
    # 2
    # velocity vector for ball1
    v1 = [ball1.x_speed, ball1.y_speed]
    # velocity vector for ball2
    v2 = [ball2.x_speed, ball2.y_speed]
    # 3
    # vectors to plain numbers
    if un[0] * un[0] + un[1] * un[1] == 0:
        v1n = 0
    else:
        v1n = (v1[0] * un[0] + v1[1] * un[1]) / (un[0] * un[0] + un[1] * un[1])
    if ut[0] * ut[0] + ut[1] * ut[1] == 0:
        v1t = 0
    else:
        v1t = (v1[0] * ut[0] + v1[1] * ut[1]) / (ut[0] * ut[0] + ut[1] * ut[1])
    if un[0] * un[0] + un[1] * un[1] == 0:
        v2n = 0
    else:
        v2n = (v2[0] * un[0] + v2[1] * un[1]) / (un[0] * un[0] + un[1] * un[1])
    if ut[0] * ut[0] + ut[1] * ut[1] == 0:
        v2t = 0
    else:
        v2t = (v2[0] * ut[0] + v2[1] * ut[1]) / (ut[0] * ut[0] + ut[1] * ut[1])
    # 4
    # new tangent velocities
    # there is no friction so this step is not necessary
    # 5
    # new normal velocities
    # there are masses in original formulas, so they are left ones as placeholders
    # but because masses are the same it means v1n, v2n = v2n, v1n
    v1n, v2n = (v1n * (1 - 1) + 2 * 1 * v2n) / (1 + 1), (v2n * (1 - 1) + 2 * 1 * v1n) / (1 + 1)
    # 6
    # scalar values to vectors for ball1
    v1n = [v1n * un[0], v1n * un[1]]
    v1t = [v1t * ut[0], v1t * ut[1]]
    # scalar values to vectors for ball2
    v2n = [v2n * un[0], v2n * un[1]]
    v2t = [v2t * ut[0], v2t * ut[1]]
    # 7
    # new velocity vectors
    v1[0] = v1n[0] + v1t[0]
    v1[1] = v1n[1] + v1t[1]
    v2[0] = v2n[0] + v2t[0]
    v2[1] = v2n[1] + v2t[1]
    # assigment to balls
    ball1.x_speed = v1[0]
    ball1.y_speed = v1[1]
    ball2.x_speed = v2[0]
    ball2.y_speed = v2[1]
    # end of collision calculation

    # moving ball1 and ball2 a litte so they dont stuck into each other
    # point of collision
    cx = (ball1.x + ball2.x) / 2
    cy = (ball1.y + ball2.y) / 2
    # distance from collision point to ball1 centre (a bit smaller than radius)
    d = sqrt((ball1.x - cx) ** 2 + (ball1.y - cy) ** 2)
    # distance between point of the collision to ball1 center point in both axes divided by d
    if d == 0:
        x_speed = 0
        dy = 0
    else:
        x_speed = (ball1.x - cx) / d
        dy = (ball1.y - cy) / d
    # ball1 move to point of collision + radius time ex or ey
    ball1.x = cx + x_speed * ball1.radius
    ball1.y = cy + dy * ball1.radius
    # ball2 move in opposite direction
    x_speed = -x_speed
    dy = -dy
    ball2.x = cx + x_speed * ball2.radius
    ball2.y = cy + dy * ball2.radius
    return ball1, ball2


def move(ball):
    # moving ball
    ball.x = ball.x + ball.x_speed
    ball.y = ball.y + ball.y_speed
    # checking for wall collision
    if ball.x >= SCREEN_WIDTH - BALLS_SIZE:
        ball.x_speed = -ball.x_speed
        ball.x = SCREEN_WIDTH - BALLS_SIZE - 1
    if ball.x <= BALLS_SIZE:
        ball.x_speed = -ball.x_speed
        ball.x = BALLS_SIZE + 1
    if ball.y >= SCREEN_HEIGHT - BALLS_SIZE:
        ball.y_speed = -ball.y_speed
        ball.y = SCREEN_HEIGHT - BALLS_SIZE - 1
    if ball.y <= BALLS_SIZE:
        ball.y_speed = -ball.y_speed
        ball.y = BALLS_SIZE + 1
    return ball


def move_player(ball):
    # checking for wall collision
    if ball.x >= SCREEN_WIDTH - PLAYER_SIZE - COLLISION_HELPER:
        ball.x = SCREEN_WIDTH - PLAYER_SIZE - COLLISION_HELPER - 1
    if ball.x <= PLAYER_SIZE + COLLISION_HELPER:
        ball.x = PLAYER_SIZE + COLLISION_HELPER + 1
    if ball.y >= SCREEN_HEIGHT - PLAYER_SIZE - 4:
        ball.y = SCREEN_HEIGHT - PLAYER_SIZE - COLLISION_HELPER - 1
    if ball.y <= PLAYER_SIZE + COLLISION_HELPER:
        ball.y = PLAYER_SIZE + COLLISION_HELPER + 1
    # moving player
    ball.x += ball.x_speed
    ball.y += ball.y_speed


def game(best_score):
    was_w = False
    was_s = False
    was_a = False
    was_d = False
    end = False
    balls = []
    count = 0
    while count < NUMBER_OF_BALLS:
        for i in range(floor(SCREEN_HEIGHT / (2.5 * BALLS_SIZE))):
            for j in range(floor(SCREEN_WIDTH / (2.5 * BALLS_SIZE))):
                balls.append(Ball(2.5 * BALLS_SIZE + j * 2.5 * BALLS_SIZE, 2.5 * BALLS_SIZE + i * 2.5 * BALLS_SIZE, choice([-BALLS_SPEED, BALLS_SPEED]), choice([-BALLS_SPEED, BALLS_SPEED]), BALLS_SIZE, BLACK))
                count += 1
                if count == NUMBER_OF_BALLS:
                    break
            if count == NUMBER_OF_BALLS:
                break
    score = 0
    player = Ball(SCREEN_WIDTH/2, SCREEN_HEIGHT - 3 * BALLS_SIZE, 0, 0, PLAYER_SIZE, PINK)
    player.x_speed = 0
    player.y_speed = 0
    while True:
        score += 1
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and score != 1:
                if event.key == pygame.K_r:
                    game(best_score)
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    player.y_speed -= PINK_SPEED
                    was_w = True
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    player.y_speed += PINK_SPEED
                    was_s = True
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    player.x_speed -= PINK_SPEED
                    was_a = True
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    player.x_speed += PINK_SPEED
                    was_d = True
            elif event.type == pygame.KEYUP and score != 1:
                if (event.key == pygame.K_w or event.key == pygame.K_UP) and was_w:
                    player.y_speed += PINK_SPEED
                elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and was_s:
                    player.y_speed -= PINK_SPEED
                elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and was_a:
                    player.x_speed += PINK_SPEED
                elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and was_d:
                    player.x_speed -= PINK_SPEED
            elif event.type == pygame.QUIT:
                print('Thanks for playing!')
                best_score_file_write = open('best_score.txt', 'w')
                best_score_file_write.write(str(best_score))
                best_score_file_write.close()
                exit(0)
        move_player(player)
        for element in balls:
            move(element)
        for ball1_index in range(0, len(balls)):
            if collision_check(balls[ball1_index], player) and not end:
                screen.fill(BLACK)
                pygame.display.flip()
                if score > best_score:
                    caption = 'Falcon and Asteroids    Current score: ' + str(score) + '     Best score: ' + str(score) + '     ~~GAME OVER~~     Press R to restart.'
                else:
                    caption = 'Falcon and Asteroids    Current score: ' + str(score) + '     Best score: ' + str(best_score) + '     ~~GAME OVER~~     Press R to restart.'
                pygame.display.set_caption(caption)
                print('~~GAME OVER~~\nYour score:', score)
                if score > best_score:
                    best_score = score
                    print('Congratulations! Its your new best score!')
                print('Press R to restart.\n')
                end = True
            for ball2_index in range(ball1_index + 1, len(balls)):
                if collision_check(balls[ball1_index], balls[ball2_index]):
                    balls[ball1_index], balls[ball2_index] = collision(balls[ball1_index], balls[ball2_index])
                    break
        if not end:
            screen.fill(BLACK)
            screen.blit(background_sprite, (0, 0))
            for element in balls:
                element.draw()
                screen.blit(enemy_sprite, (element.x - BALLS_SIZE - COLLISION_HELPER, element.y - BALLS_SIZE - COLLISION_HELPER))
            player.draw()
            screen.blit(player_sprite, (player.x - PLAYER_SIZE - COLLISION_HELPER, player.y - PLAYER_SIZE - COLLISION_HELPER))
            pygame.display.flip()
            if score > best_score:
                caption = 'Falcon and Asteroids    Current score: ' + str(score) + '     Best score: ' + str(score)
            else:
                caption = 'Falcon and Asteroids    Current score: ' + str(score) + '     Best score: ' + str(best_score)
            pygame.display.set_caption(caption)
            clock.tick(FPS)
            for ball in balls:
                if ball.x_speed > 0:
                    ball.x_speed += 0.005
                else:
                    ball.x_speed -= 0.005
                if ball.y_speed > 0:
                    ball.y_speed += 0.005
                else:
                    ball.y_speed -= 0.005


print('\nHello! This program is simple game with perfect elastic ball collisions.')
print('\nAll collision formulas based on article by Chad Berchek "2-Dimensional Elastic Collisions without Trigonometry".')
print('http://www.vobarian.com/collisions/')
# On one time unit every ball travels thought as many pixels as their speed says
# It is possible to add masses to this simulation, there is placeholder for it in formulas

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.font.init()
player_sprite = pygame.image.load('player_sprite.png')
background_sprite = pygame.image.load('background_sprite.png')
enemy_sprite = pygame.image.load('enemy_sprite.png')
best_score_file_read = open('best_score.txt', 'r')
start_score = int(best_score_file_read.read())
best_score_file_read.close()

print('\nGame starts in:')
print('3')
sleep(1)
print('2')
sleep(1)
print('1\n')
sleep(1)
game(start_score)
