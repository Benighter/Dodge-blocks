import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up the game window
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dodge the Blocks")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player
player_width = 50
player_height = 50
player_x = (width - player_width) // 2
player_y = height - player_height - 10
player_speed = 5  # Player movement speed

# Player movement variables
player_speed_x = 0
player_speed_y = 0

# Blocks
block_width = 50
block_height = 50
block_x = random.randint(0, width - block_width)
block_y = 0
block_speed = 2

# Obstacles
obstacle_width = 50
obstacle_height = 50
obstacle_x = random.randint(0, width - obstacle_width)
obstacle_y = 0
obstacle_speed = 3

# Score
score = 0
highscore = 0
font = pygame.font.Font(None, 36)

# Game over state and restart option
game_over = False
restart_option = False
over_font = pygame.font.Font(None, 72)
restart_font = pygame.font.Font(None, 36)
highscore_font = pygame.font.Font(None, 24)

# Difficulty settings
level = 1
level_threshold = 5  # Increase level every 5 points
block_speed_increment = 0.5  # Increase block speed by 0.5 every level

# Game modes
MODE_TIME_TRIAL = "Time Trial"
MODE_ENDLESS = "Endless"
current_mode = MODE_TIME_TRIAL
time_trial_duration = 30  # Time trial duration in seconds

# Timer
start_time = time.time()

# Game states
STATE_MENU = "Menu"
STATE_GAMEPLAY = "Gameplay"
STATE_GAME_OVER = "Game Over"
game_state = STATE_MENU


class Obstacle:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def move(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.rect(window, BLUE, (self.x, self.y, obstacle_width, obstacle_height))


def player(x, y):
    pygame.draw.rect(window, WHITE, (x, y, player_width, player_height))


def block(x, y):
    pygame.draw.rect(window, RED, (x, y, block_width, block_height))


def collision(player_x, player_y, block_x, block_y):
    if (
        player_x < block_x + block_width
        and player_x + player_width > block_x
        and player_y < block_y + block_height
        and player_y + player_height > block_y
    ):
        return True
    return False


def obstacle_collision(player_x, player_y, obstacle_x, obstacle_y):
    if (
        player_x < obstacle_x + obstacle_width
        and player_x + player_width > obstacle_x
        and player_y < obstacle_y + obstacle_height
        and player_y + player_height > obstacle_y
    ):
        return True
    return False


def show_score():
    score_text = font.render("Score: " + str(score), True, WHITE)
    window.blit(score_text, (10, 10))


def show_highscore():
    highscore_text = highscore_font.render("Highscore: " + str(highscore), True, WHITE)
    window.blit(highscore_text, (10, 40))


def show_level():
    level_text = font.render("Level: " + str(level), True, WHITE)
    window.blit(level_text, (width - level_text.get_width() - 10, 10))


def show_time_remaining():
    elapsed_time = int(time.time() - start_time)
    time_remaining = max(0, time_trial_duration - elapsed_time)
    time_text = font.render("Time: " + str(time_remaining), True, WHITE)
    window.blit(time_text, (width - time_text.get_width() - 10, 40))


def draw_menu():
    if game_state != STATE_MENU:
        return

    title_font = pygame.font.Font(None, 72)
    title_text = title_font.render("Dodge the Blocks", True, WHITE)
    window.blit(
        title_text,
        (width // 2 - title_text.get_width() // 2, height // 2 - title_text.get_height() - 50),
    )

    mode_font = pygame.font.Font(None, 36)
    mode_text1 = mode_font.render("1 - Time Trial Mode", True, WHITE)
    mode_text2 = mode_font.render("2 - Endless Mode", True, WHITE)
    window.blit(
        mode_text1,
        (width // 2 - mode_text1.get_width() // 2, height // 2 - mode_text1.get_height() + 50),
    )
    window.blit(
        mode_text2,
        (width // 2 - mode_text2.get_width() // 2, height // 2 - mode_text2.get_height() + 100),
    )


def return_to_menu():
    global game_state, restart_option, score, level, block_speed, player_x, player_y, block_x, block_y, obstacle_x, obstacle_y, start_time
    game_state = STATE_MENU
    restart_option = False
    score = 0
    level = 1
    block_speed = 2
    player_x = (width - player_width) // 2
    player_y = height - player_height - 10
    block_x = random.randint(0, width - block_width)
    block_y = 0
    obstacle_x = random.randint(0, width - obstacle_width)
    obstacle_y = 0
    start_time = time.time()


def reset_game():
    return_to_menu()


# Game loop
running = True
while running:
    window.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_speed_x = -player_speed
            if event.key == pygame.K_RIGHT:
                player_speed_x = player_speed
            if event.key == pygame.K_UP:
                player_speed_y = -player_speed
            if event.key == pygame.K_DOWN:
                player_speed_y = player_speed

            if game_state == STATE_MENU:
                if event.key == pygame.K_1:
                    current_mode = MODE_TIME_TRIAL
                    game_state = STATE_GAMEPLAY
                    start_time = time.time()
                elif event.key == pygame.K_2:
                    current_mode = MODE_ENDLESS
                    game_state = STATE_GAMEPLAY

            if game_state == STATE_GAME_OVER:
                if event.key == pygame.K_r:
                    restart_option = True
                elif event.key == pygame.K_m:
                    return_to_menu()

        if event.type == pygame.KEYUP:
            if (
                event.key == pygame.K_LEFT
                or event.key == pygame.K_RIGHT
                or event.key == pygame.K_UP
                or event.key == pygame.K_DOWN
            ):
                player_speed_x = 0
                player_speed_y = 0

    if game_state == STATE_GAMEPLAY:
        player_x += player_speed_x
        player_y += player_speed_y

        if player_x < 0:
            player_x = 0
        elif player_x > width - player_width:
            player_x = width - player_width

        if player_y < 0:
            player_y = 0
        elif player_y > height - player_height:
            player_y = height - player_height

        block_y += block_speed
        obstacle_y += obstacle_speed

        if block_y > height:
            block_x = random.randint(0, width - block_width)
            block_y = 0
            score += 1

            if current_mode == MODE_ENDLESS and score % level_threshold == 0:
                level += 1
                block_speed += block_speed_increment

        if obstacle_y > height:
            obstacle_x = random.randint(0, width - obstacle_width)
            obstacle_y = 0
            score += 1

            if current_mode == MODE_ENDLESS and score % level_threshold == 0:
                level += 1
                block_speed += block_speed_increment

        if collision(player_x, player_y, block_x, block_y) or obstacle_collision(
            player_x, player_y, obstacle_x, obstacle_y
        ):
            game_state = STATE_GAME_OVER
            if score > highscore:
                highscore = score

        window.fill((0, 0, 0))
        player(player_x, player_y)
        block(block_x, block_y)
        obstacle = Obstacle(obstacle_x, obstacle_y, obstacle_speed)
        obstacle.move()
        obstacle.draw()
        show_score()
        show_level()

        if current_mode == MODE_TIME_TRIAL:
            show_time_remaining()
            elapsed_time = int(time.time() - start_time)
            if elapsed_time >= time_trial_duration:
                game_state = STATE_GAME_OVER
                if score > highscore:
                    highscore = score

    elif game_state == STATE_GAME_OVER:
        if score > highscore:
            highscore = score

        over_text = over_font.render("Game Over", True, WHITE)
        restart_text = restart_font.render("Press 'R' to Restart", True, WHITE)
        menu_text = restart_font.render("Press 'M' for Menu", True, WHITE)
        score_text = font.render("Score: " + str(score), True, WHITE)
        highscore_text = font.render("Highscore: " + str(highscore), True, WHITE)

        window.blit(
            over_text,
            (width // 2 - over_text.get_width() // 2, height // 2 - over_text.get_height() - 50),
        )
        window.blit(
            restart_text,
            (width // 2 - restart_text.get_width() // 2, height // 2 - restart_text.get_height() + 50),
        )
        window.blit(
            menu_text,
            (width // 2 - menu_text.get_width() // 2, height // 2 - menu_text.get_height() + 100),
        )
        window.blit(
            score_text,
            (width // 2 - score_text.get_width() // 2, height // 2 - score_text.get_height() + 150),
        )
        window.blit(
            highscore_text,
            (width // 2 - highscore_text.get_width() // 2, height // 2 - highscore_text.get_height() + 200),
        )

        if restart_option:
            reset_game()

    draw_menu()
    pygame.display.update()

# Quit the game
pygame.quit()
