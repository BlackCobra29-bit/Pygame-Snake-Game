import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
cell_size = 20
grid_width = screen_width // cell_size
grid_height = screen_height // cell_size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

def init_snake():
    snake = {
        "length": 1,
        "positions": [((screen_width / 2), (screen_height / 2))],
        "direction": random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)]),
        "color": green
    }
    return snake

def get_head_position(snake):
    return snake["positions"][0]

def turn(snake, point):
    if snake["length"] > 1 and (point[0] * -1, point[1] * -1) == snake["direction"]:
        return snake
    else:
        snake["direction"] = point
    return snake

def move_snake(snake):
    cur = get_head_position(snake)
    x, y = snake["direction"]
    new = (((cur[0] + (x * cell_size)) % screen_width), (cur[1] + (y * cell_size)) % screen_height)

    if len(snake["positions"]) > 2 and new in snake["positions"][2:]:
        return True, snake  # Game over
    else:
        snake["positions"].insert(0, new)
        if len(snake["positions"]) > snake["length"]:
            snake["positions"].pop()
        return False, snake

def reset_snake():
    return init_snake()

def draw_snake(surface, snake):
    for p in snake["positions"]:
        r = pygame.Rect((p[0], p[1]), (cell_size, cell_size))
        pygame.draw.rect(surface, snake["color"], r)
        pygame.draw.rect(surface, black, r, 1)

def handle_keys(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
            elif event.key == pygame.K_UP:
                snake = turn(snake, (0, -1))
            elif event.key == pygame.K_DOWN:
                snake = turn(snake, (0, 1))
            elif event.key == pygame.K_LEFT:
                snake = turn(snake, (-1, 0))
            elif event.key == pygame.K_RIGHT:
                snake = turn(snake, (1, 0))
    return snake

def init_food():
    food = {
        "position": (0, 0),
        "color": red
    }
    return randomize_food_position(food)

def randomize_food_position(food):
    food["position"] = (random.randint(0, grid_width - 1) * cell_size,
                        random.randint(0, grid_height - 1) * cell_size)
    return food

def draw_food(surface, food):
    r = pygame.Rect((food["position"][0], food["position"][1]), (cell_size, cell_size))
    pygame.draw.rect(surface, food["color"], r)
    pygame.draw.rect(surface, black, r, 1)

def display_game_over(score):
    font = pygame.font.SysFont(None, 48)
    game_over_text = font.render("Game Over!", True, white)
    score_text = font.render(f"Your score: {score}", True, white)
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2,
                                 screen_height // 2 - game_over_text.get_height() // 2 - 50))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2,
                             screen_height // 2 - score_text.get_height() // 2 + 50))
    pygame.display.update()
    pygame.time.wait(2000)

def main():
    # Game objects
    snake = init_snake()
    food = init_food()

    clock = pygame.time.Clock()
    score = 0

    while True:
        game_over = False

        screen.fill(black)  # Set background color to black

        # Handle events
        snake = handle_keys(snake)
        game_over, snake = move_snake(snake)

        if game_over:
            display_game_over(score)
            break

        if get_head_position(snake) == food["position"]:
            snake["length"] += 1
            score += 1
            food = randomize_food_position(food)

        draw_snake(screen, snake)
        draw_food(screen, food)

        pygame.display.update()
        clock.tick(10)

if __name__ == "__main__":
    main()
