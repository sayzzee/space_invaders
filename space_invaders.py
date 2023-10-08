import pygame as pg
import random

pg.init()

screen_width, screen_height = 800, 600

FPS = 60
clock = pg.time.Clock()

pg.mixer.music.load("src/background.wav")
pg.mixer.music.set_volume(0.1)
pg.mixer.music.play(-1)

#изображения
bg_img = pg.image.load(r'src/background.png')
icon_img = pg.image.load(r'src/ufo.png')

display = pg.display.set_mode((screen_width, screen_height))
pg.display.set_icon(icon_img)
pg.display.set_caption('Космическая война')

sys_font = pg.font.SysFont('arial', 32)
font = pg.font.Font('src/04B_19.TTF', 40)
font_big = pg.font.Font('src/04B_19.TTF', 72)

display.blit(bg_img, (0, 0))


#player
player_img = pg.image.load('src/player.png')
player_width, player_height = player_img.get_size()
display.blit(player_img, (screen_width/2, screen_height - player_height))
player_gap = 10
player_velocity = 10
player_dx = 0
player_x = screen_width/2 - player_width/2
player_y = screen_height - player_height - player_gap
player_alive = True

#пуля
bullet_img = pg.image.load('src/bullet.png')
bullet_width, bullet_height = bullet_img.get_size()
bullet_dy = -7
bullet_x = player_x - player_width / 4   #дз - пуля вылетает из середины
bullet_y = player_y - bullet_height
bullet_alive = False
shot = pg.mixer.Sound('src/laser.wav')
shot.set_volume(0.15)

# противник
enemy_img = pg.image.load('src/enemy.png')
enemy_width, enemy_height = enemy_img.get_size()
enemy_dx = 0
enemy_dy = 2
enemy_x = 0
enemy_y = 0

#счет
score = 0
game_over = False
paused = False
pause_img = pg.image.load('src/paused.png')
pause_w, pause_h = pause_img.get_size()

def enemy_create():
    global enemy_y, enemy_x
    enemy_x = random.randint(0, screen_width - enemy_width)
    enemy_y = random.randint(0, 300)
    print(f'CREATE: {enemy_x=} {enemy_y=} ')

def player_model():
    if player_alive == True:
        global player_x
        player_x += player_dx
        if player_x < 0:
            player_x = 0
        elif player_x > screen_width - player_width:
            player_x = screen_width - player_width

def bullet_model():
    global bullet_y, bullet_alive
    bullet_y += bullet_dy
    if bullet_y < 0:
        bullet_alive = False

def enemy_model():
    global enemy_y, enemy_x, bullet_alive, player_alive, score
    if player_alive:
        enemy_x += enemy_dx
        enemy_y += enemy_dy
        if enemy_y > screen_height:
            enemy_create()

    # пересечение с пулей
    if bullet_alive:
        re = pg.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        rb = pg.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
        is_crossed = re.colliderect(rb)
        # попал!
        if is_crossed:
            print('BANG!')
            score += 1
            enemy_create()
            bullet_alive = False

    #пересечение с игроком
    if player_alive:
        per = pg.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        rep = pg.Rect(player_x, player_y, player_width, player_height)
        pereseklis = per.colliderect(rep)
        if pereseklis:
            print('Game over')
            player_alive = False

# изменение модели
def model_update():
    if paused == False:
        player_model()
        bullet_model()
        enemy_model()

def game_over_menu():
    global game_over
    if not player_alive:
        game_over_text = font_big.render('Game over', True, 'red')
        wgo, hgo = game_over_text.get_size()
        display.blit(game_over_text, (screen_width/2 - wgo/2, screen_height/2 - hgo/2))
        pg.mixer.music.pause()
        game_over = True


def score_write():
    score_text = font.render("Score: " + str(score), True, 'white')
    wgs, hgs = score_text.get_size()
    if player_alive:
        display.blit(score_text, (600, 10))
    elif not player_alive:
        display.blit(score_text, (screen_width / 2 - wgs / 2, (screen_height / 2) + hgs * 1.5))

def bullet_create():
    global bullet_y, bullet_x, bullet_alive
    if player_alive:
        bullet_alive = True
        bullet_x = player_x + player_width / 4  #дз - пуля вылетает из середины
        bullet_y = player_y - bullet_height
        shot.play()

    # redraw
def display_redraw():
    if player_alive == True:
        display.blit(bg_img, (0, 0))
        display.blit(player_img, (player_x, player_y))
        display.blit(enemy_img, (enemy_x, enemy_y))
        if bullet_alive:
            display.blit(bullet_img, (bullet_x, bullet_y))
        score_write()
        game_over_menu()
        pg.display.update()
    else:
        display.blit(bg_img, (0, 0))
        game_over_menu()
        score_write()
        pg.display.update()
    if paused == True:
        display.blit(pause_img, (screen_width / 2 - pause_w / 2, screen_height / 2 - pause_h / 2))
        pg.display.update()

def event_processing():
    global player_dx, paused, game_over, player_alive, score
    running = True
    for event in pg.event.get():
        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_q:
            running = False
        if event.type == pg.KEYDOWN and event.key == pg.K_p:
            paused = not paused
        if event.type == pg.KEYDOWN and event.key == pg.K_r:
            game_over = False
            player_alive = True
            score = 0
            pg.mixer.music.play(-1)
            enemy_create()
            running = True
            while running:
                model_update()
                display_redraw()
                running = event_processing()


        # движение игрока
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a or event.key == pg.K_LEFT:
                player_dx = -player_velocity
            if event.key == pg.K_d or event.key == pg.K_RIGHT:
                player_dx = player_velocity
        if event.type == pg.KEYUP:
            player_dx = 0

        #движение пули
        if event.type == pg.MOUSEBUTTONDOWN:
            key = pg.mouse.get_pressed()  # key[0] - left, key[2] - right
            print(f'{key[0]=} {bullet_alive=}')
            if not bullet_alive:
                bullet_create()


    clock.tick(FPS)
    return running


enemy_create()
running = True
while running:
    model_update()
    display_redraw()
    running = event_processing()



pg.quit()