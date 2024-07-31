import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)  # Black
WHITE = (255, 255, 255)
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 20
PADDLE_SPEED = 1
PADDLE_ACC = 3.5
PADDLE_ACC2 = 3.5
PADDLE_ACCM = 15
BALL_SPEED_X, BALL_SPEED_Y = 6, 6
WINNING_SCORE = 5

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro Pong")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Paddles and Ball
lp = pygame.Rect(30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
rp = pygame.Rect(WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Scores
left_score = 0
right_score = 0

# Font for score and game over text
font = pygame.font.Font(None, 74)
game_over_font = pygame.font.Font(None, 100)

# Ball reset time
ball_reset_time = 0
ball_active = False

# Game state
game_over = False
winner = None

def render():
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, WHITE, lp)
    pygame.draw.rect(screen, WHITE, rp)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    
    scoreOne = font.render(str(left_score), True, WHITE)
    screen.blit(scoreOne, (WIDTH // 4 - scoreOne.get_width() // 2, 20))
    
    scoreTwo = font.render(str(right_score), True, WHITE)
    screen.blit(scoreTwo, (WIDTH * 3 // 4 - scoreTwo.get_width() // 2, 20))

def render_game_over():
    screen.fill(BACKGROUND_COLOR)
    if winner == "left":
        text = game_over_font.render("Left Paddle Wins!", True, WHITE)
    else:
        text = game_over_font.render("Right Paddle Wins!", True, WHITE)
    
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

def updatePaddle():
    global PADDLE_ACC, PADDLE_ACC2
    keys = pygame.key.get_pressed()

    # Left paddle acceleration
    if keys[pygame.K_w] and lp.top > 0:
        lp.y -= PADDLE_SPEED + PADDLE_ACC
        PADDLE_ACC = min(PADDLE_ACC + 1, PADDLE_ACCM)
    elif keys[pygame.K_s] and lp.bottom < HEIGHT:
        lp.y += PADDLE_SPEED + PADDLE_ACC
        PADDLE_ACC = min(PADDLE_ACC + 1, PADDLE_ACCM)
    else:
        PADDLE_ACC = max(PADDLE_ACC - 2, 3)

    # Right paddle acceleration
    if keys[pygame.K_UP] and rp.top > 0:
        rp.y -= PADDLE_SPEED + PADDLE_ACC2
        PADDLE_ACC2 = min(PADDLE_ACC2 + 1, PADDLE_ACCM)
    elif keys[pygame.K_DOWN] and rp.bottom < HEIGHT:
        rp.y += PADDLE_SPEED + PADDLE_ACC2
        PADDLE_ACC2 = min(PADDLE_ACC2 + 1, PADDLE_ACCM)
    else:
        PADDLE_ACC2 = max(PADDLE_ACC2 - 2, 3)

def updateBall():
    global BALL_SPEED_X, BALL_SPEED_Y, left_score, right_score, ball_active, game_over, winner

    if ball_active:
        ball.x += BALL_SPEED_X
        ball.y += BALL_SPEED_Y

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            BALL_SPEED_Y = -BALL_SPEED_Y
        if ball.colliderect(lp) or ball.colliderect(rp):
            BALL_SPEED_X = -BALL_SPEED_X

        if ball.left <= lp.right - 10:
            right_score += 1
            reset_ball()
        if ball.right >= rp.left + 10:
            left_score += 1
            reset_ball()

        if left_score >= WINNING_SCORE:
            game_over = True
            winner = "left"
        if right_score >= WINNING_SCORE:
            game_over = True
            winner = "right"
    else:
        current_time = pygame.time.get_ticks()
        if current_time - ball_reset_time >= 2000:
            ball_active = True

def reset_ball():
    global ball_reset_time, ball_active
    ball.x = WIDTH // 2 - BALL_SIZE // 2
    ball.y = HEIGHT // 2 - BALL_SIZE // 2
    ball_active = False
    ball_reset_time = pygame.time.get_ticks()
    global BALL_SPEED_X, BALL_SPEED_Y
    BALL_SPEED_X = -BALL_SPEED_X

def main():
    global running, game_over
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            updatePaddle()
            updateBall()
            render()
        else:
            render_game_over()
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

