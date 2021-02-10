import pygame
import os
import time
import random
import pygame_menu

#GETTİNG FPS
pygame.init()
pygame.mixer.init()



FPS = 60
VEL = 5

BULLETVEL = 30
RED = (255, 0, 0)
pygame.init()
max_bullets = 40
pygame.display.set_caption("Star Waders!")


PLAYERONE_HIT = pygame.USEREVENT + 1

PLAYERTWO_HIT = pygame.USEREVENT + 2
PLAYBUTTONHIT = pygame.USEREVENT + 3



clock = pygame.time.Clock()
LUKE_IMAGE = pygame.image.load(os.path.join("Assets", "darthmaul.png"))
OBI_WAN_IMAGE = pygame.image.load(os.path.join("Assets", "obi.png"))
LASER_IMAGE = pygame.image.load(os.path.join("Assets", "laser.png"))
maintheme = pygame.mixer.Sound(os.path.join("Assets", "maintheme.wav"))
winning = pygame.mixer.Sound(os.path.join("Assets", "soundeffect.wav"))
maintheme.set_volume(0.1)
winning.set_volume(0.4)


WIDTH, HEIGHT = 1280,720

win = pygame.display.set_mode((WIDTH, HEIGHT))

BLACK = (0, 0, 0)

WHITE= (255, 255, 255 )

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BACKGROUND = pygame.image.load(os.path.join("Assets", "backgroundy.jpg"))
CHARACTER_WIDTH, CHARACTER_HEIGHT = (100, 100)
LUKE = pygame.transform.scale(LUKE_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT))

LASER_WIDTH, LASER_HEIGHT = (32, 32)
OBI_WAN = pygame.transform.rotate(pygame.transform.scale(OBI_WAN_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT)), 0)
BULLET = pygame.transform.rotate(pygame.transform.scale(LASER_IMAGE, (LASER_WIDTH, LASER_HEIGHT)), 180)
ENEMY_IMAGE = pygame.image.load(os.path.join("Assets", "star-wars.png"))
ENEMY_WIDTH, ENEMY_HEIGHT = (64, 64)

ENEMY = pygame.transform.scale(ENEMY_IMAGE, (ENEMY_WIDTH, ENEMY_HEIGHT))

font = pygame.font.SysFont("arial", 30, True, False)
fontofwinner = pygame.font.SysFont("arial", 100, True, False)




def draw_window(playerone, playertwo, playerenemy, playerenemytwo, bullets):
    win.blit(BACKGROUND, [0, 0])
    pygame.draw.rect(win, BLACK, BORDER)
    win.blit(LUKE, (playerone.x, playerone.y))
    win.blit(OBI_WAN, (playertwo.x, playertwo.y))
    win.blit(ENEMY, (playerenemy.x, playerenemy.y))
    win.blit(ENEMY, (playerenemytwo.x, playerenemytwo.y))
    if len(bullets) <= max_bullets:
        for bullet in bullets:
            pygame.draw.rect(win, RED, bullet)

    pygame.display.update()



def enemy(playerone, playertwo, playerenemy, playerenemytwo, bullets, bullet, EVEL, EVELTWO):
    global MAX_BULLETS

    global SCORE
    global SCORESECOND


    if playerenemy.y + EVEL + playerenemy.height < HEIGHT:
        playerenemy.y += EVEL
        bullet = pygame.Rect(playerenemy.x + 27, playerenemy.y + playerenemy.height//2 - 2, 10, 5)
        bullets.append(bullet)
        bullets.append(bullet)
    else:
        playerenemy.y = 0
        playerenemy.x = random.randint(0 + ENEMY_WIDTH, WIDTH/2 - ENEMY_WIDTH)





    if playerenemytwo.y + EVELTWO + playerenemytwo.height < HEIGHT:
        playerenemytwo.y += EVELTWO
        bullet = pygame.Rect(playerenemytwo.x + 27, playerenemytwo.y + playerenemytwo.height // 2 - 2, 10, 5)
        bullets.append(bullet)
        bullets.append(bullet)

    else:
        playerenemytwo.y = 0
        playerenemytwo.x = random.randint(WIDTH/2 + ENEMY_WIDTH, WIDTH - ENEMY_WIDTH)





def redrawwindow(HEALTH, HEALTHTWO, SCORE, SCORESECOND):
    # This should go inside the redrawGameWindow function
    text = font.render("Score: " + str(SCORE), True, (BLACK))  # Arguments are: text, anti-aliasing, color

    texttwo = font.render(str(SCORESECOND) + " :Score", True, (BLACK))

    healthtext = font.render("Health: " + str(HEALTH), True, (RED))  # Arguments are: text, anti-aliasing, color
    healthtexttwo = font.render("Health: " + str(HEALTHTWO), True, (RED))  # Arguments are: text, anti-aliasing, color
    win.blit(healthtext, (100, 10))
    win.blit(healthtexttwo, (1070, 10))
    win.blit(text, (300, 10))
    win.blit(texttwo, (870, 10))

    pygame.display.update()



def playerone_movement(keys_pressed, playerone):
    if keys_pressed[pygame.K_a] and playerone.x - VEL > 0:  # left going luke
        playerone.x -= VEL
    if keys_pressed[pygame.K_d] and playerone.x + VEL + playerone.width < BORDER.x:  # right going luke
        playerone.x += VEL
    if keys_pressed[pygame.K_w] and playerone.y - VEL > 0:  # up going luke
        playerone.y -= VEL
    if keys_pressed[pygame.K_s] and playerone.y + VEL + playerone.height < HEIGHT:  # down going luke
        playerone.y += VEL

def playertwo_movement(keys_pressed, playertwo):
    if keys_pressed[pygame.K_LEFT] and playertwo.x - VEL > BORDER.x + BORDER.width:  # left going obi
        playertwo.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and playertwo.x + VEL + playertwo.width < WIDTH:  # right going obi
        playertwo.x += VEL
    if keys_pressed[pygame.K_UP] and playertwo.y - VEL > 0:  # up going obi
        playertwo.y -= VEL
    if keys_pressed[pygame.K_DOWN] and playertwo.y + VEL + playertwo.height < HEIGHT:  # down going obi
        playertwo.y += VEL

def handle_bullets(bullets, playerenemy, playerenemytwo, playerone, playertwo):

    for bullet in bullets:
        bullet.y += BULLETVEL
        if playerone.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PLAYERONE_HIT))

            bullets.remove(bullet)
        elif bullet.y > HEIGHT:
            bullets.remove(bullet)

    for bullet in bullets:
        if playerone.colliderect(playerenemy):
            pygame.event.post(pygame.event.Event(PLAYERONE_HIT))
        if playertwo.colliderect(playerenemytwo):
            pygame.event.post(pygame.event.Event(PLAYERTWO_HIT))
        bullet.y += BULLETVEL
        if playertwo.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PLAYERTWO_HIT))

            bullets.remove(bullet)
        elif bullet.y > HEIGHT:
            bullets.remove(bullet)



def draw_winner(text):
    draw_text = font.render(text, 1, RED)
    win.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(23000)







def main():
    global event

    playerone = pygame.Rect(320, 100, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    playertwo = pygame.Rect(960, 100, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    playerenemy = pygame.Rect(160, 17, ENEMY_WIDTH, ENEMY_HEIGHT)
    playerenemytwo = pygame.Rect(1120, 17, ENEMY_WIDTH, ENEMY_HEIGHT)
    bullet = pygame.Rect(119, 81 // 2 - 2, 10, 5)
    bullets = []
    HEALTH = 100
    HEALTHTWO = 100
    EVEL = round(5)
    EVELTWO = round(5)
    SCORE = 0
    SCORESECOND = 0






    run = True
    while run:
        pygame.mixer.Sound.play(maintheme)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        if event.type == PLAYERONE_HIT:
            HEALTH -= 1
        else:
            EVEL += 0.0050
            SCORE += 1



        if event.type == PLAYERTWO_HIT:
            HEALTHTWO -= 1
        else:
            EVELTWO += 0.0050
            SCORESECOND += 1



        winner_text = ""
        if HEALTH <= 0:
            winner_text = "Obi Wan Wins, The Game Will Be Restarted In 25 Seconds!!"
            pygame.mixer.Sound.stop(maintheme)
            pygame.mixer.Sound.play(winning)
        if HEALTHTWO <= 0:
            winner_text = "Darth Maul Wins, The Game Will Be Restarted In 25 Seconds!!"
            pygame.mixer.Sound.stop(maintheme)
            pygame.mixer.Sound.play(winning)
        if winner_text != "":
            draw_winner(winner_text)
            break









        keys_pressed = pygame.key.get_pressed()


        playerone_movement(keys_pressed, playerone)


        playertwo_movement(keys_pressed, playertwo)

        handle_bullets(bullets, playerenemy, playerenemytwo, playerone, playertwo)

        enemy(playerone, playertwo, playerenemy, playerenemytwo, bullets, bullet, EVEL, EVELTWO)


        draw_window(playerone, playertwo, playerenemy, playerenemytwo, bullets)

        redrawwindow(HEALTH, HEALTHTWO, SCORE, SCORESECOND)





    main()


if __name__ == "__main__":
    main()

