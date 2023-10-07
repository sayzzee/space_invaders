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
player_y = screen_height  - player_height - player_gap


running = True
while running:
    # изменение модели
    # player_x += player_velocity
    player_x += player_dx

    # redraw
    display.blit(bg_img, (0, 0))
    display.blit(player_img, (player_x, player_y))

    pg.display.update()
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


    clock.tick(FPS)

pg.quit()
