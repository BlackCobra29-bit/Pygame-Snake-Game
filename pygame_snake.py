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

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((screen_width / 2), (screen_height / 2))]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])  # Directions are stored as tuples
        self.color = green

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction  # Now it's safe to unpack direction
        new = (((cur[0] + (x * cell_size)) % screen_width), (cur[1] + (y * cell_size)) % screen_height)
        if len(self.positions) > 2 and new in self.positions[2:]:
            return True  # Game over
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((screen_width / 2), (screen_height / 2))]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])  # Reset direction randomly

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (cell_size, cell_size))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, black, r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                elif event.key == pygame.K_UP:
                    self.turn((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.turn((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.turn((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.turn((1, 0))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = red
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, grid_width-1) * cell_size, random.randint(0, grid_height-1) * cell_size)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (cell_size, cell_size))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, black, r, 1)


def display_game_over(score):
    font = pygame.font.SysFont(None, 48)
    game_over_text = font.render("Game Over!", True, white)
    score_text = font.render(f"Your score: {score}", True, white)
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2 - 50))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 - score_text.get_height() // 2 + 50))
    pygame.display.update()
    pygame.time.wait(2000)

def main():
    # Game objects
    snake = Snake()
    food = Food()

    clock = pygame.time.Clock()
    score = 0

    while True:
        game_over = False

        screen.fill(black)  # Set background color to black

        # Handle events
        snake.handle_keys()
        game_over = snake.move()

        if game_over:
            display_game_over(score)
            break

        if snake.get_head_position() == food.position:
            snake.length += 1
            score += 1
            food.randomize_position()

        snake.draw(screen)
        food.draw(screen)

        pygame.display.update()
        clock.tick(10)

if __name__ == "__main__":
    main()