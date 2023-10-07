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

# display.fill('blue', (0, 0, screen_width, screen_height))
display.blit(bg_img, (0, 0))

#text_img = sys_font.render('Score 123', True, 'white')
#display.blit(text_img, (37, 37))

# game_over_text = font.render('Game over', True, 'red')
# wgo, hgo = game_over_text.get_size()
#display.blit(game_over_text, (screen_width/2 - wgo/2, screen_height/2 - hgo/2))

#player
player_img = pg.image.load('src/player.png')
player_width, player_height = player_img.get_size()
display.blit(player_img, (screen_width/2, screen_height - player_height))
# text_player_name = font.render('Alexandr', True, 'lightpink')
# wp, hp = text_player_name.get_size()


running = True
while running:
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_q:
            running = False
        # if event.type == pg.KEYDOWN and event.key == pg.K_s:
        #     display.blit(text_player_name, (screen_width / 2 - wp / 2, screen_height / 4 - hp / 2))
        # if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
        #     display.blit(bg_img, (0, 0))
        #     display.blit(text_img, (37, 37))
        #     display.blit(game_over_text, (screen_width / 2 - wgo / 2, screen_height / 2 - hgo / 2))
        #     display.blit(player_img, (screen_width/2, screen_height - player_height))
    clock.tick(FPS)

pg.quit()
