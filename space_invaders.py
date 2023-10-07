import pygame as pg

pg.init()

screen_width, screen_height = 800, 600

FPS = 60
clock = pg.time.Clock()

#изображения
bg_img = pg.image.load(r'src/background.png')
icon_img = pg.image.load(r'src/ufo.png')

display = pg.display.set_mode((screen_width, screen_height))
pg.display.set_icon(icon_img)
pg.display.set_caption('Космическая война')

sys_font = pg.font.SysFont('arial', 32)
font = pg.font.Font('src/04B_19.TTF', 48)

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


bullet_img = pg.image.load('src/bullet.png')
bullet_width, bullet_height = bullet_img.get_size()
bullet_dy = -5
bullet_x = player_x    #дз - пуля вылетает из середины
bullet_y = player_y - bullet_height
bullet_alive = False


# изменение модели
def model_update():
    player_model()
    bullet_model()

def player_model():
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

def bullet_create():
    global bullet_y, bullet_x, bullet_alive
    bullet_alive = True
    bullet_x = player_x + player_width / 4  #дз - пуля вылетает из середины
    bullet_y = player_y - bullet_height

    # redraw
def display_redraw():
    display.blit(bg_img, (0, 0))
    display.blit(player_img, (player_x, player_y))
    pg.display.update()
    if bullet_alive:
        display.blit(bullet_img, (bullet_x, bullet_y))
    pg.display.update()

def event_processing():
    global player_dx
    running = True
    for event in pg.event.get():
        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_q:
            running = False

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


running = True
while running:
    model_update()
    display_redraw()
    running = event_processing()

pg.quit()