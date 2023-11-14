import pygame
import random
import time
import sys

pygame.init()

# Hình ảnh
m = 20
Imgbody = pygame.transform.scale(pygame.image.load('image/snakebody.png'), (m, m))
Imghead = pygame.transform.scale(pygame.image.load('image/snakehead.png'), (25, 25))
Imgfood = pygame.transform.scale(pygame.image.load('image/apple.png'), (m, m))

# Tạo cửa sổ
gameSurface = pygame.display.set_mode((735, 475))
pygame.display.set_caption('Fat Snake Game')

# Màu sắc
red = pygame.Color(255, 0, 0)
blue = pygame.Color(65, 105, 255)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
gray = pygame.Color(128, 128, 128)

# Khai báo biến
snakepos = [100, 60]
snakebody = [[110, 60], [80, 60], [60, 60]]
foodx = random.randrange(1, 71)
foody = random.randrange(1, 45)
if foodx % 2 != 0: foodx += 1
if foody % 2 != 0: foody += 1
foodpos = [foodx * 10, foody * 10]
foodflat = True
direction = 'RIGHT'
changeto = direction
score = 0

#kiểm soát trạng thái game
game_over_flag = False

# Hàm reset game
def reset_game():
    global snakepos, snakebody, foodx, foody, foodpos, foodflat, direction, changeto, score
    snakepos = [100, 60]
    snakebody = [[100, 60], [80, 60], [60, 60]]
    foodx = random.randrange(1, 71)
    foody = random.randrange(1, 45)
    if foodx % 2 != 0: foodx += 1
    if foody % 2 != 0: foody += 1
    foodpos = [foodx * 10, foody * 10]
    foodflat = True
    direction = 'RIGHT'
    changeto = direction
    score = 0

# Hàm game over
def game_over():
    gfont = pygame.font.SysFont('Monaco', 30)
    gsurf = gfont.render('Game over! Press "enter" to retry.', True, red)
    grect = gsurf.get_rect()
    grect.midtop = (360, 150)
    gameSurface.blit(gsurf, grect)
    show_score(0)
    pygame.display.flip()
    time.sleep(2)

def game_stop():
    gfont = pygame.font.SysFont('Monaco', 30)
    show_score(0)
    pygame.display.flip()
    time.sleep(2)

def show_score(choice=1):
    sfont = pygame.font.SysFont('Monaco', 20)
    ssurf = sfont.render('Score: {0}'.format(score), True, black)
    srect = ssurf.get_rect()
    if choice == 1:
        srect.midtop = (70, 20)
    else:
        srect.midtop = (360, 230)
    gameSurface.blit(ssurf, srect)

# Vòng lặp chính
speed = 100
while True:
    pygame.time.delay(speed)  # Tốc độ chơi
    #keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        # Xử lý phím
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                changeto = 'RIGHT'
            if event.key == pygame.K_LEFT:
                changeto = 'LEFT'
            if event.key == pygame.K_UP:
                changeto = 'UP'
            if event.key == pygame.K_DOWN:
                changeto = 'DOWN'
            if event.key == pygame.K_ESCAPE:
                game_stop()
                sys.exit()
            # Nhấn Enter để chơi lại khi game over
            if game_over_flag and event.key == pygame.K_RETURN:
                game_over_flag = False
                reset_game()

    # Kiểm tra trạng thái game over
    if not game_over_flag:
        # Hướng đi
        if changeto == 'RIGHT' and not direction == 'LEFT':
            direction = 'RIGHT'
        if changeto == 'LEFT' and not direction == 'RIGHT':
            direction = 'LEFT'
        if changeto == 'UP' and not direction == 'DOWN':
            direction = 'UP'
        if changeto == 'DOWN' and not direction == 'UP':
            direction = 'DOWN'

        # Cập nhật vị trí mới
        if direction == 'RIGHT':
            snakepos[0] += m
        if direction == 'LEFT':
            snakepos[0] -= m
        if direction == 'UP':
            snakepos[1] -= m
        if direction == 'DOWN':
            snakepos[1] += m

        # Cơ chế dài ra khi ăn mồi
        snakebody.insert(0, list(snakepos))
        if snakepos[0] == foodpos[0] and snakepos[1] == foodpos[1]:
            score += 1
            foodflat = False
        else:
            snakebody.pop()

        # Sinh mồi ngẫu nhiên
        if foodflat == False:
            foodx = random.randrange(1, 71)
            foody = random.randrange(1, 45)
            if foodx % 2 != 0: foodx += 1
            if foody % 2 != 0: foody += 1
            foodpos = [foodx * 10, foody * 10]
            foodflat = True

        # Update window
        gameSurface.fill(white)
        for pos in snakebody:
            gameSurface.blit(Imgbody, pygame.Rect(pos[0], pos[1], m, m))
        gameSurface.blit(Imghead, pygame.Rect(snakebody[0][0], snakebody[0][1], m, m))
        gameSurface.blit(Imgfood, pygame.Rect(foodpos[0], foodpos[1], m, m))

        # Xử lý va chạm: 4 cạnh biên
        if snakepos[0] > 710 or snakepos[0] < 10:
            game_over_flag = True
        if snakepos[1] > 450 or snakepos[1] < 10:
            game_over_flag = True

        # Xử lý va chạm: chính mình
        for b in snakebody[1:]:
            if snakepos[0] == b[0] and snakepos[1] == b[1]:
                game_over_flag = True

        # Đường viền
        pygame.draw.rect(gameSurface, gray, (10, 10, 715, 455), 2)
        show_score()
    else:
        game_over()

    pygame.display.flip()
