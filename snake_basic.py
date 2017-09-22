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

font = pygame.font.SysFont(None, 25)
block_size = 10


def disp_snake(loclist, size):
    for location in loclist:
        pygame.draw.rect(gameDisplay, green, (location[0], location[1], size, size))


def disp_mesg(msg, color):
    text = font.render(msg, True, color)
    gameDisplay.blit(text, [display_width/2, display_height/2])


def round_to_10(n):
    return round(n/10.0) * 10.0


def replace_apple():
    x = random.randrange(0, display_width-block_size)
    y = random.randrange(0, display_height-block_size)
    return round_to_10(x), round_to_10(y)


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

        lead_x += lead_x_change
        lead_y += lead_y_change

        if( lead_x >= display_width or lead_x <= 0 or lead_y >= display_height or lead_y <= 0):
            game_over = True

        gameDisplay.fill(white)
        pygame.draw.rect(gameDisplay, red, (ap_x, ap_y, block_size, block_size))

        snake_head = [lead_x, lead_y]
        snake_loc_list.append(snake_head)
        if len(snake_loc_list) > snake_len:
            del snake_loc_list[0]

        # detect collision with self
        for segment in snake_loc_list[:-1]:
            if segment == snake_head:
                game_over = True

        disp_snake(snake_loc_list, block_size)
        pygame.display.update()

        if lead_x == ap_x and lead_y == ap_y:
            ap_x, ap_y = replace_apple()
            snake_len += 1

        clock.tick(FPS)

    pygame.quit()
    quit(0)

game_loop()
