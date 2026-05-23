import pygame
import random

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
dark_red = (139, 0, 0)
blood_red = (180, 0, 0)
grid_gray = (30, 30, 30)

levels = {
    '1': {'grid_size': 8, 'cell_size': 45, 'speed': 6, 'name': 'Easy'},
    '2': {'grid_size': 12, 'cell_size': 40, 'speed': 8, 'name': 'Medium'},
    '3': {'grid_size': 16, 'cell_size': 35, 'speed': 10, 'name': 'Hard'}
}

font_style = pygame.font.SysFont("bahnschrift", 25)
menu_font = pygame.font.SysFont("bahnschrift", 35)
score_font = pygame.font.SysFont("comicsansm", 35)

def show_menu():
    dis = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Friday 13 - I')

    menu = True
    while menu:
        dis.fill(black)

        title = menu_font.render("Friday 13th", True, dark_red)
        subtitle = font_style.render("Choose:", True, blood_red)
        dis.blit(title, [800 // 2 - title.get_width() // 2, 80])
        dis.blit(subtitle, [800 // 2 - subtitle.get_width() // 2, 140])

        opt1 = font_style.render("1 - Easy (8x8)", True, white)
        opt2 = font_style.render("2 - Medium (12x12)", True, white)
        opt3 = font_style.render("3 - Hard (16x16)", True, white)
        opt4 = font_style.render("ESC - Exit (Выход)", True, blood_red)

        dis.blit(opt1, [400 - opt1.get_width() // 2, 220])
        dis.blit(opt2, [400 - opt2.get_width() // 2, 270])
        dis.blit(opt3, [400 - opt3.get_width() // 2, 320])
        dis.blit(opt4, [400 - opt4.get_width() // 2, 420])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return levels['1']
                elif event.key == pygame.K_2:
                    return levels['2']
                elif event.key == pygame.K_3:
                    return levels['3']
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

def game(level):
    grid_size = level['grid_size']
    cell_size = level['cell_size']
    snake_speed = level['speed']

    dis_width = grid_size * cell_size
    dis_height = grid_size * cell_size

    dis = pygame.display.set_mode((dis_width, dis_height))
    pygame.display.set_caption(f'Friday 13 - I - {level["name"]}')
    clock = pygame.time.Clock()

    snake_block = cell_size

    game_over = False
    game_close = False

    x1 = (dis_width // 2) // cell_size * cell_size
    y1 = (dis_height // 2) // cell_size * cell_size
    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1
    direction = 'RIGHT'

    foodx = random.randint(0, grid_size - 1) * cell_size
    foody = random.randint(0, grid_size - 1) * cell_size

    def score(score):
        value = score_font.render("Victims: " + str(score), True, blood_red)
        dis.blit(value, [10, 0])

    def message(msg, color):
        mesg = font_style.render(msg, True, color)
        text_x = dis_width // 2 - mesg.get_width() // 2
        text_y = dis_height // 2 - mesg.get_height() // 2 - 40
        dis.blit(mesg, [text_x, text_y])

    def tourists(x, y):
        center_x = x + cell_size // 2
        center_y = y + cell_size // 2
        radius = cell_size // 3
        pygame.draw.circle(dis, blood_red, (center_x, center_y), radius)
        pygame.draw.circle(dis, dark_red, (center_x, center_y), radius // 2)
        eye_size = max(2, cell_size // 10)
        pygame.draw.circle(dis, black, (center_x - radius // 2, center_y - radius // 2), eye_size)
        pygame.draw.circle(dis, black, (center_x + radius // 2, center_y - radius // 2), eye_size)

    while not game_over:
        while game_close:
            dis.fill(black)
            message("GAME OVER! ESC - Exit, R - Replay", blood_red)
            score_text = score_font.render("Victims: " + str(length_of_snake - 1), True, blood_red)
            score_x = dis_width // 2 - score_text.get_width() // 2
            score_y = dis_height // 2 + 20
            dis.blit(score_text, [score_x, score_y])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        new_level = show_menu()
                        game(new_level)
                        return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                    direction = "RIGHT"
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                    direction = "UP"
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0
                    direction = "DOWN"
                elif event.key == pygame.K_ESCAPE:
                    new_level = show_menu()
                    game(new_level)
                    return

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        dis.fill(black)

        for x in range(0, dis_width, cell_size):
            pygame.draw.line(dis, grid_gray, (x, 0), (x, dis_height), 1)
        for y in range(0, dis_height, cell_size):
            pygame.draw.line(dis, grid_gray, (0, y), (dis_width, y), 1)

        tourists(foodx, foody)

        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        for i, segment in enumerate(snake_list):
            is_head = (i == len(snake_list) - 1)
            x, y = segment[0], segment[1]

            pygame.draw.rect(dis, white, [x, y, snake_block, snake_block])

            if not is_head:
                line_thickness = max(4, snake_block // 6)
                mid_x = x + snake_block // 2
                mid_y = y + snake_block // 2
                pygame.draw.line(dis, black, (mid_x, y), (mid_x, y + snake_block), line_thickness)
                pygame.draw.line(dis, black, (x, mid_y), (x + snake_block, mid_y), line_thickness)
                spot_size = max(1, snake_block // 10)
                pygame.draw.circle(dis, blood_red, (mid_x - snake_block // 3, mid_y - snake_block // 3), spot_size)
                pygame.draw.circle(dis, blood_red, (mid_x + snake_block // 3, mid_y - snake_block // 3), spot_size)
                pygame.draw.circle(dis, blood_red, (mid_x - snake_block // 3, mid_y + snake_block // 3), spot_size)
                pygame.draw.circle(dis, blood_red, (mid_x + snake_block // 3, mid_y + snake_block // 3), spot_size)


            else:

                # Создаем поверхность для головы

                head_surface = pygame.Surface((snake_block, snake_block), pygame.SRCALPHA)

                head_surface.fill((0, 0, 0, 0))
                
                eye_size = max(3, snake_block // 6)
                
                left_eye = (snake_block // 3, snake_block // 3)
                
                right_eye = (2 * snake_block // 3, snake_block // 3)

                pygame.draw.circle(head_surface, black, left_eye, eye_size)
                pygame.draw.circle(head_surface, black, right_eye, eye_size)
                
                line_thickness = max(2, snake_block // 12)
                
                pygame.draw.line(head_surface, blood_red, (snake_block // 6, snake_block // 2), (snake_block // 3, snake_block // 2), line_thickness)
                pygame.draw.line(head_surface, blood_red, (2 * snake_block // 3, snake_block // 2), (5 * snake_block // 6, snake_block // 2), line_thickness)
                
                pattern_size = max(1, snake_block // 12)
                
                pygame.draw.circle(head_surface, blood_red, (snake_block // 4, 2 * snake_block // 3), pattern_size)
                pygame.draw.circle(head_surface, blood_red, (3 * snake_block // 4, 2 * snake_block // 3), pattern_size)
                pygame.draw.line(head_surface, blood_red, (snake_block // 4, snake_block // 6), (3 * snake_block // 4, snake_block // 6), max(2, snake_block // 10))
                
                if direction == 'RIGHT':
                    rotated = pygame.transform.rotate(head_surface, 270)
                elif direction == 'LEFT':
                    rotated = pygame.transform.rotate(head_surface, 90)
                elif direction == 'UP':
                    rotated = pygame.transform.rotate(head_surface, 0)
                elif direction == 'DOWN':
                    rotated = pygame.transform.rotate(head_surface, 180)
                else:
                    rotated = head_surface

                dis.blit(rotated, (x, y))
        score(length_of_snake - 1)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            while True:
                foodx = random.randint(0, grid_size - 1) * cell_size
                foody = random.randint(0, grid_size - 1) * cell_size
                if [foodx, foody] not in snake_list:
                    break
            length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

selected_level = show_menu()
game(selected_level)
