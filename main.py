import pygame
import random

pygame.init()
clock = pygame.time.Clock() #for fps
FPS = 10

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0, 0)

display_width, display_height = 800, 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Slither')

font = pygame.font.SysFont("comicsansms", 40)
small_font = pygame.font.SysFont(None, 20)
block_size = 20
ap_size = 30

sn_img = pygame.image.load('snake20.jpg')
ap_img = pygame.image.load('apple.png')


def disp_snake(loclist, size):
    gameDisplay.blit(sn_img, (loclist[-1][0], loclist[-1][1]))
    for location in loclist[:-1]:
        pygame.draw.rect(gameDisplay, green, (location[0], location[1], size, size))


def disp_mesg(msg, color):
    text = font.render(msg, True, color)
    textRect = text.get_rect()
    textRect.center = [display_width/2, display_height/2]
    gameDisplay.blit(text, textRect)


def show_score(score):
    text = small_font.render("Score: "+str(score), True, black)
    gameDisplay.blit(text, (0,0))
    text = small_font.render("Press P to Pause: ", True, black)
    gameDisplay.blit(text, (0,20))


def round_to_10(n):
    return round(n/10.0) * 10.0


def replace_apple():
    x = random.randrange(0, display_width-block_size)
    y = random.randrange(0, display_height-block_size)
    return round_to_10(x), round_to_10(y)

def pause():
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c or event.key == pygame.K_p:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        disp_mesg("Paused. 'c' or 'p' to continue. q to quit", black)
        pygame.display.update()
        clock.tick(5)


def game_loop():
    game_over = False
    game_exit = False
    lead_x = display_width/2
    lead_y = display_height/2
    lead_x_change = 0
    lead_y_change = 0

    snake_loc_list = []
    snake_head = []
    snake_len = 1

    ap_x, ap_y = replace_apple()

    while not game_exit:

        while game_over:
            gameDisplay.fill(white)
            disp_mesg("Game Over. 'C' to continue, 'Q' to quit", red)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        game_loop()
                    elif event.key == pygame.K_q:
                        game_exit = True
                        game_over = False

        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    lead_y_change += block_size
                    lead_x_change = 0
                elif event.key == pygame.K_UP:
                    lead_y_change -= block_size
                    lead_x_change = 0
                elif event.key == pygame.K_RIGHT:
                    lead_x_change += block_size
                    lead_y_change = 0
                elif event.key == pygame.K_LEFT:
                    lead_x_change -= block_size
                    lead_y_change = 0
                elif event.key == pygame.K_p:
                    pause()

        lead_x += lead_x_change
        lead_y += lead_y_change

        if( lead_x >= display_width or lead_x <= 0 or lead_y >= display_height or lead_y <= 0):
            game_over = True

        gameDisplay.fill(white)
        #pygame.draw.rect(gameDisplay, red, (ap_x, ap_y, ap_size, ap_size))
        gameDisplay.blit(ap_img, (ap_x, ap_y))

        snake_head = [lead_x, lead_y]
        snake_loc_list.append(snake_head)
        if len(snake_loc_list) > snake_len:
            del snake_loc_list[0]

        # detect collision with self
        for segment in snake_loc_list[:-1]:
            if segment == snake_head:
                game_over = True

        disp_snake(snake_loc_list, block_size)
        show_score(snake_len-1)
        pygame.display.update()

        # detect collision with apple
        if (lead_x > ap_x and lead_x < ap_x + ap_size or lead_x + block_size > ap_x and lead_x + block_size < ap_x + ap_size)\
                and (lead_y > ap_y and lead_y < ap_y + ap_size or lead_y + block_size > ap_y and lead_y + block_size < ap_y + ap_size):
            ap_x, ap_y = replace_apple()
            snake_len += 1

        clock.tick(FPS)

    pygame.quit()
    quit(0)

game_loop()
